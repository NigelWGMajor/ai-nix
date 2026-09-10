# /pro - Pull Requests Open

| Capability | Support | Alternative |
|---|---|---|
| Existing broad PR analysis | yes | wiz |
| Reconstruct child PR stack | yes | dac for planned work |
| Review child stack | gap | wiz |
| Automatic Git/remote mutation | approval required | |

Use /pro on a branch whose existing PR has become too broad to review. It analyses the source PR and branch, proposes disciplined and dependency-aware child PRs, then reconstructs an equivalent new parent only after explicit approval.

The source branch stays unchanged. Child PRs target the new feature-master, and one final feature-master PR targets the original PR base. /pro never assumes that base is main.

/pro ? describes this workflow without inspecting a branch.
