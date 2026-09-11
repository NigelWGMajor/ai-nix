# /pro - Pull Requests Open

| Capability | Support | Alternative |
|---|---|---|
| Existing broad PR analysis | yes | wiz |
| Reconstruct and track child PR stack | yes | dac for planned work |
| Review child stack | gap | wiz |
| Automatic Git/remote mutation | approval required | |

Use /pro on a branch whose existing PR has become too broad to review. It analyses the source PR and branch, proposes disciplined and dependency-aware child PRs, then reconstructs an equivalent new parent only after explicit approval.

The source branch stays unchanged. Child PRs target the new feature-master and cross-reference their siblings. After at least one child is remotely verified merged, `/pro` can offer a draft parent PR; it becomes ready for review only when every required child is remotely verified merged and the convergence gate passes. The parent PR targets the original PR base, which `/pro` never assumes is `main`.

On a recorded Pro branch, `/pro` resumes with a compact branch list and an observed child/parent PR status report. It marks remote state Unknown when it cannot verify it.

/pro ? describes this workflow without inspecting a branch.
