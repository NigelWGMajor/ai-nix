# 🔗 GAP reviews a branch or recorded delivery hierarchy

| Capability | Support | Alternative |
|---|---|---|
| Single-branch skeptical review | yes | cop |
| DAC or Pro hierarchy review | yes | wiz for one implementation |
| Cross-branch integration verdict | yes | dac for delivery coordination |
| Automatic Git or remote mutation | no | explicit approval required |

Use `/gap` for an independent COP-style review of one branch or a recorded DAC or Pro hierarchy. It produces per-node verdicts and a cross-branch integration roll-up, but does not coordinate delivery, switch branches, or make source and remote changes.

GAP reads the recorded hierarchy and verifies dependency claims against the recorded baseline and sibling evidence. If a remote state, baseline, or build-time dependency cannot be checked, it remains Unknown or Blocked rather than being reported as missing.
