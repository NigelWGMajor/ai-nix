# Skill to trace history

## starting context

The starting point is a git branch or repo. This could be one of several cases:
- This is the main branch and we are interested in the recent history of revisions
- this is a /dac generated set, and could be the parent or any sub-branch
- this could be part of a speckit set without /dac support
- this could be a ticket-controlled task which may have related tickets

## Process

On initial launch, the skill quickly traiges to determine what the immediately-obvious structure is.
Evidence:
- git 
  - branch
  - parent branch / depth to main
    - sibling branches
  - recent commits
    - mine
    - others
  - related tickets
    - status

## ideal findings

- structure
  - intent
  - responsibilities
  - status
- navigation
  - participants
  - sequence
  - links

## output

- markdown document with absolute links - 100% compatible with the Upstream document format (will be provided)
- structure by:
  - intent
    - contributors (components or classes)
    - participants (members)
    - sequence (call chain)
- identify
  - status
  - upstream/downstream linking

## why

- From a PR I can establish the branch.
- If i know the branch, I can look at the recent history
  - if there is not enough I can sak for more/deeper
- I can discern the intent, possibly with the help of related jira information
- I can discern the current state of completion
- I can discern what is still needed, possibly jira or interactively discovered
- I can identify where the contibuting work is in the codebase, and what its role/status is
- I can identify what the next steps are and whre they belong
- I can navigate using the output links

Each contribution is either in place, partial or needed. The first two shuold have in-code evidence, which is locatable: the needed stuff shlould have refences too.
