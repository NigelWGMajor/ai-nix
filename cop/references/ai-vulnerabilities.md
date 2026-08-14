# AI-Specific Vulnerability Patterns

Catalog of failure modes common in AI-assisted code generation. Use this as the primary checklist when reviewing AI-generated or AI-modified code. Update this file as new patterns emerge from real reviews.

## Unwarranted assumptions

AI assistants routinely treat plausible guesses as established facts. Flag any code that depends on details not proven by supplied evidence.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Schema invention | Database columns, table names, or relationships inferred from naming conventions rather than inspected from the actual schema | High |
| API contract guessing | Request/response fields, status codes, authentication flows, or error shapes assumed from similar-looking APIs | High |
| Configuration fabrication | Environment variables, connection strings, feature flags, or paths that were never supplied or verified | High |
| Business rule inference | Domain logic derived from variable names or comments rather than requirements or observed behavior | Medium |
| Infrastructure assumptions | Queue names, service endpoints, file system layouts, container configurations, or cloud resource names that were not supplied | Medium |
| Behavioral assumptions | Assumptions about concurrency, ordering, idempotency, transaction isolation, or retry behavior without evidence | High |

**Review action:** For each assumption, require the evidence that supports it. Mark unsupported assumptions as `MISSING EVIDENCE`. Do not accept "it's a reasonable assumption" as justification.

## Incorrect naming

AI assistants frequently name things based on pattern-matching rather than domain understanding. Incorrect names create persistent confusion.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Domain term misuse | Using a business term with a subtly different meaning than the domain intends | Medium |
| Inconsistent vocabulary | Introducing a new name for a concept that already has a canonical name in the codebase | Medium |
| Misleading abstraction names | Names like `Manager`, `Helper`, `Service`, `Handler`, `Utils` that obscure what the unit actually does | Low |
| Case and convention violations | Naming that ignores the project's established conventions (casing, prefixes, suffixes, namespaces) | Low |
| Semantic drift | Renaming existing concepts during implementation without updating all consumers and documentation | High |

**Review action:** Check every new name against existing vocabulary in the codebase. Grep for the canonical term before accepting a new one.

## Unsubstantiated schemas

AI assistants often generate code that references database objects, API contracts, or data structures that do not exist or differ materially from reality.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Phantom columns | Referencing columns that don't exist in the actual table, or using incorrect types or nullability | Critical |
| Invented relationships | Foreign keys, joins, or navigation properties that don't exist in the schema | Critical |
| Wrong table or view | Using a plausible-sounding table name that doesn't match the actual database object | Critical |
| Stored procedure signature mismatch | Wrong parameter names, types, ordering, or return shapes | Critical |
| Migration/schema drift | Generating code for a schema version that doesn't exist yet (or no longer exists) | High |
| API field mismatch | Request or response fields that don't match the actual contract, OpenAPI spec, or observed behavior | High |

**Review action:** Every schema reference must be traceable to a verified source (migration, schema dump, OpenAPI spec, or observed runtime output). Reject code that depends on unverified schema details.

## Gratuitous refactoring

AI assistants have a strong bias toward restructuring existing code, even when the task doesn't call for it. This introduces risk without value.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Scope creep refactoring | Restructuring code adjacent to the change that was not part of the task | Medium |
| Abstraction escalation | Introducing interfaces, base classes, factories, or strategy patterns for code with one implementation | Medium |
| Unnecessary wrapper layers | Wrapping existing APIs, services, or libraries with thin delegation layers that add no behavior | Medium |
| Premature generalization | Making code "flexible" for hypothetical future requirements that were not requested | Medium |
| Style-driven rewriting | Rewriting working code to match a preferred style without functional improvement | Low |
| Comment and documentation churn | Adding verbose docstrings, multi-line comments, or README sections that restate what the code already says | Low |

**Review action:** For any change that is not directly required by the task, demand: (1) what existing problem does this solve, (2) what is the measurable improvement, (3) what is the risk of the change. Without all three, reject the refactoring.

## Hallucinated behavior

AI assistants sometimes describe behavior as if it were already implemented, or generate code that looks correct but does not do what it claims.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Phantom test assertions | Tests that appear to verify behavior but actually test trivially true conditions or mock their own assertions | Critical |
| Error handling theater | Try/catch blocks that swallow exceptions, log generic messages, or re-throw without useful context | High |
| Dead code paths | Generated branches, methods, or classes that are never called or reachable | Medium |
| Copy-paste drift | Copied code blocks modified just enough to compile but not enough to be correct for the new context | High |
| Confident incorrectness | Code accompanied by explanatory comments that describe what the code should do but doesn't actually do | High |

**Review action:** Trace each claimed behavior from entry point to observable outcome. Run or mentally execute the code. Do not trust comments or explanations as evidence of correctness.

## Overengineering

AI assistants default to more structure, more abstraction, and more infrastructure than the problem requires.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Framework introduction | Plugin systems, event buses, middleware pipelines, or dependency injection containers without proven need | High |
| Design pattern forcing | Applying patterns (observer, mediator, command, repository) because they "fit" rather than because the problem requires them | Medium |
| Premature optimization | Caching, connection pooling, batching, or parallelism added before profiling identifies a bottleneck | Medium |
| Configuration over convention | Making hard-coded values configurable when there is no requirement for runtime flexibility | Low |
| Microservice thinking | Splitting or proposing to split a bounded change into multiple services, queues, or independent deployments | High |
| Generic type parameters | Adding type parameters or generics to types that will only ever have one concrete instantiation | Low |

**Review action:** Apply the "tired engineer at 2 AM" test. If removing the abstraction makes the code shorter and the behavior identical, remove it. Require proof of necessity for any framework or pattern introduction.

## Implementation drift

AI assistants can gradually shift the implementation away from the stated requirements during a multi-step conversation.

| Pattern | What to look for | Severity |
| --- | --- | --- |
| Feature accretion | Each conversation turn adds a small feature or capability that was never requested | Medium |
| Scope expansion | The implementation grows to handle cases that are explicitly out of scope | Medium |
| Architecture escalation | Starting with a simple approach and progressively replacing it with more complex infrastructure | High |
| Requirement reinterpretation | Subtly redefining what the requirement means to justify a preferred implementation approach | High |
| Gold-plating | Adding polish, error messages, logging, metrics, or documentation beyond what was asked for | Low |

**Review action:** Compare the current implementation against the original requirement at every review pass. Flag any capability that cannot be traced to an explicit requirement.
