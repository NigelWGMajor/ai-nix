# ai-nix skill orientation

Choose by the outcome you need, not by the skill name. Start with **UMM** when the route is unclear; most workflows are read-only until you explicitly approve a change.

## Quick routes

- `UMM → NIX → ACT`: route an unclear request, understand it, then produce a useful brief, ticket, or handoff.
- `FIX → ACT`: diagnose an unexplained symptom before deciding what to change.
- `WIZ → COP`: assess a concrete PR, branch, or ticket, then apply an independent check. Add **GAP** for a recorded DAC or Pro hierarchy.
- `DAC → WIZ/GAP → ACT`: coordinate large Jira-backed delivery; use **DAC Help** when allocation is unclear.
- `LIT → PIX` explains and presents source material; choose **TUT** for a hands-on walkthrough. `KIT → MAP` recovers and resumes interrupted work.

Use `VAL` for test strategy, `PRO` to split and track an oversized PR through a feature-master, and `MEM` to find notes. Use `MAP → PRO` to resume a recorded reconstruction, then `GAP` for an independent hierarchy review. **DORA** is separate: use it for persistent codebase discovery and tracing, not as a delivery pipeline.

<div style="break-before: page; page-break-before: always;"></div>

## Start-point routing flowchart

```mermaid

flowchart TB
    QUERY((Query))
    NEW((New))
    WIP((WIP))
    REV((Review))

    QUERY -.-> L
    QUERY -.-> T
    QUERY -.-> B
    QUERY -.-> U
    NEW -.-> E
    NEW -.-> L
    NEW -.-> T
    WIP -.-> S
    WIP -.-> M
    WIP -.-> B
    REV -.-> P
    REV -.-> F

    E[Epic or large story] --> D[🧩 DAC]
    S[Single branch in progress] --> W[🪄 WIZ]
    M[Multi-branch work in progress] -->|coordinate delivery| D[🧩 DAC]
    M -->|cross-branch review| G[🔗 GAP]
    P[Large PR in review] --> R[🪜 PRO]
    L[Large set of related documents] --> I[📚 LIT]
    T[Technical process to understand] --> I
    F[Focused PR in review] --> W
    B[Unknown bug or unexpected behavior] --> X[🛠️ FIX]
    U[Unclear starting point] --> Q[🔮 UMM]
    Q --> N[🦄 NIX]

    D --> H[Partition and coordinate delivery]
    H --> W
    R --> C[Reconstruct focused child PRs]
    C --> W
    G --> V[Cross-branch integration view]
    W -->|independent check| O[👮 COP]
    X --> A[🎬 ACT: package the next action]
    I --> J[🎓 TUT]
    J --> Y[🖼️ PIX]
    N --> A
```

<div style="break-before: page; page-break-before: always;"></div>

## New work

Use this route to turn a new Epic, large story, or bounded story into work that can enter the WIP flow.

```mermaid
---
config:
  flowchart:
    curve: monotoneY
---
flowchart TD
      E((Epic or <br>large story)) --> D[[🧩 DAC]]
    D --> |Preview<br>Portions|P[[🧩 DAC]]
    P --> |Create child issues|M[[🧩 DAC]]
    S((Small story)) --> B[Create one branch]
    BB((Bug or Issue)) --> B[Create one branch]
    M -->|switch<br>between<br> branches| W((Continue<br>as WIP))
    B --> W
```

<div style="break-before: page; page-break-before: always;"></div>

## Work in progress

Use this route when implementation is already under way.

```mermaid
flowchart TD
    X((Branches<br> from DAC)) --> D[[🧩 DAC]]
    S((Single<br>branch)) --> W[[🪄 WIZ]]
    S --->|If Speckit|K[[📃KIT]] --> M
    D -->|cross-branch review| G[[🔗 GAP]]
    W --> O[[👮 COP]]
    G -->|Merged to parent| M[Single Branch] 
    M -.->|if complex| PRO[[🪜PRO]] 
    O --> M
    X -->|individually|W
    PRO-->MM[Multiple branches]
    MM -->Z
    M -->Z((Continue <br>Review))
K -.-> |Summarize|A[🎬 ACT]
O -.-> |Summarize|A[🎬 ACT]
G -.-> |Summarize|A[🎬 ACT]
W -.-> |Summarize|A[🎬 ACT]




```




<div style="break-before: page; page-break-before: always;"></div>

## Review

Use this route once the question is whether the change is ready, not how to build it.

```mermaid
flowchart TD
    S((Single PR)) --> W
    M((Multiple PRs)) --> W
    W[🪄 WIZ]
  

    M --> G[🔗 GAP]
    G -.->|uses|O
    W --> O[👮 COP]
    O
    G --> X[[🛠️ FIX]]
    O --> X[[🛠️ FIX]] 
    O --> W
    X --> O
```

<div style="break-before: page; page-break-before: always;"></div>

## Bug / Issue

Use this route for investigating behavior

```mermaid
flowchart TD
    O((Issue)) --> X[[🛠️ FIX]]
    O((Issue)) --> N[[🦄 NIX]]
    X --> |new ticket|A[🎬 ACT]
    N --> |new ticket|A[🎬 ACT]

```



## Information

Use this route for questions that do not begin with new work, implementation in progress, or review.

```mermaid
---
config:
  flowchart:
    curve: monotoneY
---
flowchart TD
    L((Documentation)) --> I[📚 LIT]
    T((Technical query)) --> I
    I --> U[🎓 TUT]
    U --> P[🖼️ PIX]
    K --> |Summarize|A[🎬 ACT]
    I --> |Summarize|A[🎬 ACT]
    X((General Query)) --> M[🔮 UMM]
    M --> K[🦄 NIX]

```
