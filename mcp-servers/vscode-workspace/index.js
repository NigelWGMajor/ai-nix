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
import { existsSync } from 'fs';
import { join, resolve } from 'path';
import { homedir, platform } from 'os';

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
