# Cross-workspace code discovery

Use this reference when the task requires code investigation, review, diagnosis, planning, status reconstruction, or validation. Its purpose is to keep a primary checkout from becoming an accidental boundary when a front-end client or prototype materially affects the question.

## Establish a bounded source set

1. Call the VS Code Workspace MCP `get_workspace_context` first. Its `workspaceFolders` and bounded `repositories` list define the candidate source set for this run; pass the active `.code-workspace` file when it is not available through the environment. If the MCP is unavailable, record that limitation before falling back to explicit paths and repository guidance.
2. Resolve the **primary source root** from the explicit path, active workspace, review target, or repository guidance. Record its branch/ref when that matters.
3. Before drawing a code conclusion, consider the remaining VS Code workspace repositories alongside roots named by the request, ticket, PR, repository guidance, solution/package workspace metadata, build or deployment definitions, or references in the primary source.
4. Expand beyond the primary root when the question involves a user interaction, rendered state, client/server payload or route, authentication or session behavior, feature flag/configuration exposure, telemetry, shared terminology, or another explicitly cross-boundary contract. Treat directories such as `fe-workspace`, `frontend`, `web`, `ui`, `client`, and `prototype` as candidates to verify, never as proof that they are relevant.

Do not recursively scan arbitrary parent directories, drives, or unrelated repositories. Limit discovery to explicitly named roots, configured workspace roots, and directly evidenced companion repositories. If several plausible roots remain and choosing one could change the result, ask one concise scoping question.

## Inspect each confirmed repository independently

## Select repositories before scanning

When two or more candidate repositories are available and the request has not already named the exact source set, show the user the candidate list and ask which repositories to include. Accept `all`, numbered entries, or explicit paths. Do not start a multi-repository code scan or create a Standard/Deep instance until the selection is resolved. An explicit request to scan all configured repositories selects all of them.

The root selected to host the output instance is an output-location decision, not implicit approval to scan only that repository. Keep the selected source set fixed for the run; newly discovered repositories are candidates to present to the user, never silent additions.

Record every discovered candidate, the user's include/exclude selection and reason, source root, ref/freshness when known, and what was or was not inspected in `00-control.md` and the working evidence.

If a selected root cannot be found or accessed, report it as **Unknown / not inspected** and explain the impact on the conclusion. Cross-workspace discovery remains read-only and does not authorize edits, branch switching, installation, deployment, or other mutation in an additional repository.


Code indexes and graphs are normally repository-scoped. Query or index each confirmed source root separately, with its own working directory/project argument when the tool supports it. Do not infer that a graph search in the backend also searched the FE workspace, or that a missing graph result proves absence from another repository.

Use the graph/index for structural code discovery in that repository and use targeted text or file inspection for configuration, generated artifacts, package metadata, workspace manifests, and string contracts. Preserve the root and ref for each claim; do not combine evidence from differently checked-out branches without saying so.

## Include prototypes deliberately

Inspect a prototype when it is named by the task or evidence, demonstrates a behavior or contract under investigation, is referenced by a production source, or is the only available client representation. A prototype is evidence of intent or behavior, not automatically the production source of truth. State its authority and whether its currentness or deployment status is unknown.

## Report the boundary

For a materially cross-boundary question, keep a compact source-boundary record in the result or working evidence: source root, why it was included or excluded, ref/freshness when known, and what was or was not inspected. If an expected FE or prototype root cannot be found or accessed, report it as **Unknown / not inspected** and describe the effect on the conclusion. Cross-workspace discovery is read-only and does not authorize edits, branch switching, installation, deployment, or other mutation in an additional repository.

Stop expanding once the available evidence answers the question, or once uninspected candidates have no evidenced connection to the subject. Do not turn a bounded backend question into a workspace-wide audit merely because companion repositories exist.
