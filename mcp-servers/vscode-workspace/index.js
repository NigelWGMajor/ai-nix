#!/usr/bin/env node
/**
 * VSCode Workspace MCP Server
 *
 * Provides workspace root and git repository information to Claude Code skills.
 * Resolves the actual VSCode workspace root independent of terminal CWD.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import { existsSync, readdirSync, readFileSync, statSync } from 'fs';
import { delimiter, dirname, join, resolve } from 'path';
import { homedir, platform } from 'os';
import { fileURLToPath } from 'url';

const execAsync = promisify(exec);

/**
 * Get OS-specific fallback path for non-git workspaces
 */
function getFallbackPath() {
  switch (platform()) {
    case 'win32':
      return 'C:\\.data';
    case 'darwin':
      return join(homedir(), 'Library', 'Application Support', 'claude-skills');
    default:
      return join(homedir(), '.local', 'share', 'claude-skills');
  }
}

/**
 * Try to find git root from a starting directory
 */
async function findGitRoot(startPath) {
  try {
    const { stdout } = await execAsync('git rev-parse --show-toplevel', {
      cwd: startPath,
      encoding: 'utf-8'
    });
    return stdout.trim().replace(/\n/g, '');
  } catch {
    return null;
  }
}

/**
 * Check if a directory is a git repository
 */
function isGitRepository(path) {
  return existsSync(join(path, '.git'));
}

/**
 * Walk up the directory tree looking for .git
 */
function findGitRootSync(startPath) {
  let current = resolve(startPath);
  const root = resolve('/');

  while (current !== root) {
    if (isGitRepository(current)) {
      return current;
    }
    const parent = resolve(current, '..');
    if (parent === current) break;
    current = parent;
  }

  return null;
}

function splitWorkspaceFolderValue(value) {
  if (!value?.trim()) return [];

  const trimmed = value.trim();
  if (trimmed.startsWith('[')) {
    try {
      const parsed = JSON.parse(trimmed);
      if (Array.isArray(parsed) && parsed.every((item) => typeof item === 'string')) return parsed;
    } catch {
      // Fall through to platform-delimited paths.
    }
  }

  return trimmed.split(delimiter).map((item) => item.trim()).filter(Boolean);
}

function parseJsonc(content) {
  let withoutComments = '';
  let inString = false;
  let escaping = false;

  for (let index = 0; index < content.length; index += 1) {
    const character = content[index];
    const next = content[index + 1];

    if (inString) {
      withoutComments += character;
      if (escaping) escaping = false;
      else if (character === '\\') escaping = true;
      else if (character === '"') inString = false;
      continue;
    }

    if (character === '"') {
      inString = true;
      withoutComments += character;
      continue;
    }
    if (character === '/' && next === '/') {
      index = content.indexOf('\n', index);
      if (index === -1) break;
      withoutComments += '\n';
      continue;
    }
    if (character === '/' && next === '*') {
      const end = content.indexOf('*/', index + 2);
      index = end === -1 ? content.length : end + 1;
      continue;
    }
    withoutComments += character;
  }

  let withoutTrailingCommas = '';
  inString = false;
  escaping = false;
  for (let index = 0; index < withoutComments.length; index += 1) {
    const character = withoutComments[index];
    if (inString) {
      withoutTrailingCommas += character;
      if (escaping) escaping = false;
      else if (character === '\\') escaping = true;
      else if (character === '"') inString = false;
      continue;
    }
    if (character === '"') {
      inString = true;
      withoutTrailingCommas += character;
      continue;
    }
    if (character === ',') {
      const nextContent = withoutComments.slice(index + 1);
      if (/^\s*[}\]]/.test(nextContent)) continue;
    }
    withoutTrailingCommas += character;
  }

  return JSON.parse(withoutTrailingCommas);
}
function readWorkspaceFileFolders(workspaceFile) {
  try {
    const absoluteFile = resolve(workspaceFile);
    const workspace = parseJsonc(readFileSync(absoluteFile, 'utf-8'));
    if (!Array.isArray(workspace.folders)) {
      return { folders: [], warning: `Workspace file has no folders array: ${absoluteFile}` };
    }

    const folders = workspace.folders
      .map((entry) => typeof entry === 'string' ? entry : entry?.path)
      .filter((entry) => typeof entry === 'string' && entry.length > 0)
      .map((entry) => resolve(dirname(absoluteFile), entry));

    return { folders, warning: null };
  } catch (error) {
    return { folders: [], warning: `Could not read VS Code workspace file ${workspaceFile}: ${error.message}` };
  }
}

function enumerateWorkspaceRepositories(root, maxDepth) {
  const repositories = [];
  const queue = [{ path: resolve(root), depth: 0 }];
  const seen = new Set();
  const ignoredDirectories = new Set(['.git', '.data', 'build', 'coverage', 'dist', 'node_modules', 'out']);

  while (queue.length > 0) {
    const current = queue.shift();
    const key = platform() === 'win32' ? current.path.toLowerCase() : current.path;
    if (seen.has(key) || !existsSync(current.path)) continue;
    seen.add(key);

    try {
      if (!statSync(current.path).isDirectory()) continue;
      if (isGitRepository(current.path)) {
        repositories.push(current.path);
        continue;
      }

      if (current.depth >= maxDepth) continue;
      for (const entry of readdirSync(current.path, { withFileTypes: true })) {
        if (!entry.isDirectory() || ignoredDirectories.has(entry.name)) continue;
        queue.push({ path: join(current.path, entry.name), depth: current.depth + 1 });
      }
    } catch {
      // An unreadable workspace child is reported through the root, not treated as absent.
    }
  }

  return repositories;
}

async function getActiveVSCodeWorkspaceTargets() {
  try {
    const { stdout } = await execAsync('code --status', {
      encoding: 'utf-8',
      timeout: 10000,
      windowsHide: true,
    });
    const processArgv = stdout.match(/^Process Argv:\s+(.+)$/m)?.[1] || '';
    const targets = [];
    for (const match of processArgv.matchAll(/--(file|folder)-uri\s+(\S+)/g)) {
      try {
        targets.push({ kind: match[1], path: fileURLToPath(match[2]) });
      } catch {
        // Ignore a non-file URI; it cannot be inspected by this local MCP.
      }
    }
    return targets;
  } catch {
    return [];
  }
}
async function getWorkspaceContext({ hint, workspaceFile, maxDepth } = {}) {
  const folders = [];
  const warnings = [];
  const addFolder = (path, source) => {
    if (!path) return;
    const absolutePath = resolve(path);
    if (!folders.some((folder) => folder.path === absolutePath)) {
      folders.push({ path: absolutePath, source, exists: existsSync(absolutePath) });
    }
  };

  for (const file of [workspaceFile, process.env.VSCODE_WORKSPACE_FILE].filter(Boolean)) {
    const parsed = readWorkspaceFileFolders(file);
    parsed.folders.forEach((folder) => addFolder(folder, 'workspace-file'));
    if (parsed.warning) warnings.push(parsed.warning);
  }

  const environmentFolders = splitWorkspaceFolderValue(process.env.VSCODE_WORKSPACE_FOLDERS || process.env.VSCODE_WORKSPACE_FOLDER);
  environmentFolders.forEach((folder) => addFolder(folder, 'vscode-environment'));

  if (folders.length === 0) {
    for (const target of await getActiveVSCodeWorkspaceTargets()) {
      if (target.kind === 'file') {
        const parsed = readWorkspaceFileFolders(target.path);
        parsed.folders.forEach((folder) => addFolder(folder, 'vscode-code-status'));
        if (parsed.warning) warnings.push(parsed.warning);
      } else {
        addFolder(target.path, 'vscode-code-status');
      }
    }
  }

  if (folders.length === 0) {
    const resolved = await resolveWorkspaceRoot(hint);
    addFolder(resolved.workspaceRoot, resolved.resolvedFrom);
    if (resolved.warning) warnings.push(resolved.warning);
  }

  const boundedDepth = Number.isInteger(maxDepth) ? Math.max(0, Math.min(maxDepth, 4)) : 2;
  const repositoryMap = new Map();
  for (const folder of folders) {
    for (const repository of enumerateWorkspaceRepositories(folder.path, boundedDepth)) {
      const key = platform() === 'win32' ? repository.toLowerCase() : repository;
      if (!repositoryMap.has(key)) repositoryMap.set(key, { path: repository, discoveredFrom: folder.path });
    }
  }

  return { workspaceFolders: folders, repositories: [...repositoryMap.values()], warnings };
}
/**
 * Resolve workspace root with multiple strategies
 */
async function resolveWorkspaceRoot(hint) {
  const startPath = hint || process.cwd();

  // Strategy 1: Try git from hint/cwd
  const gitRoot = await findGitRoot(startPath);
  if (gitRoot) {
    return {
      workspaceRoot: gitRoot,
      resolvedFrom: 'git-command',
      isGitRepository: true,
      gitRoot: gitRoot
    };
  }

  // Strategy 2: Try VSCode environment variables if available
  const vscodeWorkspace = process.env.VSCODE_WORKSPACE_FOLDER || process.env.VSCODE_CWD;
  if (vscodeWorkspace) {
    const vscodeGitRoot = await findGitRoot(vscodeWorkspace);
    return {
      workspaceRoot: vscodeGitRoot || vscodeWorkspace,
      resolvedFrom: 'vscode-env',
      isGitRepository: !!vscodeGitRoot,
      gitRoot: vscodeGitRoot
    };
  }

  // Strategy 3: Fallback path
  const fallback = getFallbackPath();
  return {
    workspaceRoot: fallback,
    resolvedFrom: 'fallback',
    isGitRepository: false,
    gitRoot: null,
    warning: `No git repository found. Using fallback: ${fallback}`
  };
}

/**
 * Create and configure the MCP server
 */
const server = new Server(
  {
    name: 'vscode-workspace',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'get_workspace_root',
      description: 'Get the VSCode workspace root path, git repository root, and fallback information. Returns the actual workspace root independent of terminal CWD.',
      inputSchema: {
        type: 'object',
        properties: {
          hint: {
            type: 'string',
            description: 'Optional path hint to start searching from (defaults to current working directory)',
          },
        },
      },
    },
    {
      name: 'get_workspace_context',
      description: 'List every configured VSCode workspace folder and the Git repositories found within each bounded workspace folder. Use this before code discovery that may cross repositories.',
      inputSchema: {
        type: 'object',
        properties: {
          hint: {
            type: 'string',
            description: 'Optional path hint when VSCode workspace metadata is unavailable',
          },
          workspaceFile: {
            type: 'string',
            description: 'Optional absolute or relative .code-workspace file to parse for multi-root folders',
          },
          maxDepth: {
            type: 'integer',
            minimum: 0,
            maximum: 4,
            description: 'Maximum directory depth for repository discovery inside each workspace folder (defaults to 2)',
          },
        },
      },
    },
    {
      name: 'check_git_repository',
      description: 'Check if a given path is inside a git repository and return repository information',
      inputSchema: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'Path to check for git repository',
          },
        },
        required: ['path'],
      },
    },
  ],
}));

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'get_workspace_root') {
      const result = await resolveWorkspaceRoot(args?.hint);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    }
    if (name === 'get_workspace_context') {
      const result = await getWorkspaceContext({
        hint: args?.hint,
        workspaceFile: args?.workspaceFile,
        maxDepth: args?.maxDepth,
      });

      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
      };
    }

    if (name === 'check_git_repository') {
      const targetPath = args.path;
      const gitRoot = findGitRootSync(targetPath);

      const result = {
        path: targetPath,
        isGitRepository: !!gitRoot,
        gitRoot: gitRoot,
        exists: existsSync(targetPath),
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            error: error.message,
            stack: error.stack,
          }),
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Log to stderr so it doesn't interfere with MCP protocol on stdout
  console.error('VSCode Workspace MCP Server running on stdio');
  console.error(`Fallback path: ${getFallbackPath()}`);
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
