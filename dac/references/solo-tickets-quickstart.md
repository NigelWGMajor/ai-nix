# Solo Tickets Quick Start

Solo tickets bring DAC's structured management to individual work items without requiring artificial parent coordination. They live in `.dac/<workstream>/solo/` alongside portions and use the same authority model and branch tracking.

## Use Cases

- Adopt existing tickets into DAC management
- Ensure proper acceptance criteria on standalone tickets
- Track branch sync for individual work items
- Bridge informal work into structured delivery
- Manage related tickets with common ancestor

## Quick Commands

### Adopt an existing ticket

```bash
python scripts/dac.py solo adopt \
  --workspace .dac/ABC-123 \
  --ticket-id ABC-456 \
  --title "Fix authentication bug" \
  --outcome "Users can log in reliably" \
  --ac "- [ ] Login succeeds for valid credentials
- [ ] Error message shown for invalid credentials" \
  --jira-url "https://jira.example.com/browse/ABC-456"
```

### Create envelope for new ticket

```bash
python scripts/dac.py solo create \
  --workspace .dac/ABC-123 \
  --ticket-id ABC-789 \
  --title "Add request logging" \
  --outcome "All API requests are logged" \
  --executor direct
```

### Check solo ticket status

```bash
python scripts/dac.py solo status --workspace .dac/ABC-123
```

Output:
```
Solo tickets in ABC-123:

Ticket   Status     Branch                    Executor  Last Updated
ABC-456  adopted    feature/ABC-456-auth-fix  direct    2026-08-28T14:30:00
ABC-789  executing  feature/ABC-789-logging   direct    2026-08-28T15:00:00
```

### Transition state

```bash
python scripts/dac.py solo transition \
  --workspace .dac/ABC-123 \
  --ticket-id ABC-456 \
  --to executing \
  --by "Developer Name"
```

Valid state transitions:
- `assessed` → `adopted`, `superseded`
- `adopted` → `executing`, `blocked`, `superseded`
- `executing` → `blocked`, `pr_open`, `complete`, `superseded`
- `blocked` → `executing`, `superseded`
- `pr_open` → `blocked`, `integrated`, `superseded`
- `integrated` → `complete`

### Branch sync

```bash
python scripts/dac.py sync --workspace .dac/ABC-123
```

Shows both portions (P:) and solo tickets (S:):
```
Legend: P:portion S:solo

Item         Status      Branch                Behind  Ahead  Remote      Action
P:P-001      executing   feature/P-001-api     0       3      unpushed    PUSH
S:ABC-456    executing   feature/ABC-456-auth  2       1      in sync     MERGE PARENT
```

## Folder Structure

```
.dac/<workstream>/
  00-control.md           # Coordination control
  portions/               # Coordinated portions
    P-001.md
  solo/                   # Standalone tickets (NEW)
    ABC-456.md
    ABC-789.md
  results/
    P-001.md              # Portion results
    ABC-456-result.md     # Solo results (NEW)
```

## Solo Envelope Structure

Each solo ticket has an envelope at `solo/<ticket-id>.md`:

```yaml
---
artifact: solo
workstream: ABC-123
ticket_id: ABC-456
stage: solo
status: adopted
executor: direct
jira_url: https://jira.example.com/browse/ABC-456
branch: feature/ABC-456-auth-fix
---

# Solo Ticket: Fix authentication bug

## Outcome and boundaries
- Outcome: Users can log in reliably
- Included: Auth validation, error handling
- Excluded: Password reset flow

## Acceptance Criteria
- [ ] Login succeeds for valid credentials
- [ ] Error message shown for invalid credentials
- [ ] Session cookie set correctly

## Scope
What's in, what's out

## Test obligations
- Unit tests for validation
- Integration test for login flow
- Manual verification across browsers

## Authority envelope
- W1: .dac/ABC-123/solo/
- C3: auth/ directory, tests/
- V2: run test suite
- R4: Jira updates, PR creation

## State log
Tracks all transitions with timestamp and reason
```

## Authority Model

Solo tickets follow the same authority model as portions:

| Class | Scope | Default |
|---|---|---|
| R0 | Read Jira, code, Git metadata | allowed |
| W1 | Write `.dac/<workstream>/solo/` | explicit approval |
| V2 | Run tests, builds | explicit approval |
| C3 | Change source, tests, branches | explicit approval |
| R4 | Update Jira, create PR, merge | explicit approval |

## Integration with Main DAC Commands

- `dac status` - Shows all artifacts including solo tickets
- `dac sync` - Tracks branches for both portions and solo tickets
- `dac validate` - Validates workspace including solo directory

## Workflow

1. **Adopt or Create** - Bring ticket under DAC management
2. **Review Envelope** - Ensure acceptance criteria, scope, tests clear
3. **Create Branch** - Follow branch naming from envelope
4. **Execute** - Implement with authority model
5. **Track Progress** - Use `transition` for state updates
6. **Sync Branch** - Keep up to date with parent branch
7. **Record Result** - Create result artifact on completion

## Promoting to Portions

When a solo ticket becomes part of larger coordination:

1. Create/identify parent Epic/Feature
2. Initialize DAC coordination for parent
3. Convert solo envelope to portion envelope
4. Add to portion plan and integration plan
5. Move from `solo/` to `portions/`

Preserves all work and audit trail while integrating into full DAC coordination.

## Differences from Portions

| Aspect | Portion | Solo Ticket |
|--------|---------|-------------|
| Parent | Required | Optional (workstream only) |
| Dependencies | Tracked, enforced | None |
| Decisions | Inherits from parent | Self-contained |
| Integration plan | Coordinated with siblings | Independent |
| Use case | Part of larger outcome | Standalone work |

## Examples

### Simple bug fix

```bash
# Adopt existing bug ticket
python scripts/dac.py solo adopt \
  --workspace .dac/PROJ-100 \
  --ticket-id PROJ-456 \
  --title "Fix null pointer in payment processor" \
  --outcome "Payment processing handles null customer gracefully" \
  --ac "- [ ] Null customer returns proper error
- [ ] Error logged with context
- [ ] Existing tests still pass"

# Transition to executing
python scripts/dac.py solo transition \
  --workspace .dac/PROJ-100 \
  --ticket-id PROJ-456 \
  --to executing

# Later: check sync
python scripts/dac.py sync --workspace .dac/PROJ-100
```

### New feature work

```bash
# Create envelope for new ticket
python scripts/dac.py solo create \
  --workspace .dac/PROJ-100 \
  --ticket-id PROJ-789 \
  --title "Add rate limiting middleware" \
  --outcome "API protected from excessive requests" \
  --executor direct

# Edit envelope to add details
# ... implement ...

# Transition through states
python scripts/dac.py solo transition --workspace .dac/PROJ-100 --ticket-id PROJ-789 --to executing
python scripts/dac.py solo transition --workspace .dac/PROJ-100 --ticket-id PROJ-789 --to pr_open
python scripts/dac.py solo transition --workspace .dac/PROJ-100 --ticket-id PROJ-789 --to integrated
python scripts/dac.py solo transition --workspace .dac/PROJ-100 --ticket-id PROJ-789 --to complete
```

## FAQ

**Q: When should I use solo tickets vs. portions?**
A: Use solo when work is independent and doesn't require parent coordination. Use portions when work is part of larger outcome with dependencies.

**Q: Can I have both portions and solo tickets in same workspace?**
A: Yes! Use portions for coordinated work, solo tickets for related but independent work.

**Q: Can I promote a solo ticket to a portion later?**
A: Yes. Create parent coordination, convert envelope, add to portion plan.

**Q: Do solo tickets support dependencies?**
A: No. If you need dependencies, use portions under a parent.

**Q: What happens to solo tickets during DAC completion?**
A: They're independent. Complete them on their own timeline. They can outlive the parent coordination.
