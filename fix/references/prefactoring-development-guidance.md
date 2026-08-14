# Prefactoring-Inspired Development Guidance

## Purpose

This document defines foundational guidance for designing, implementing, and reviewing code. It is inspired by the ideas in Ken Pugh's *Prefactoring*: apply lessons learned from previous development and refactoring work before new code hardens around avoidable design problems.

This is an original, practical interpretation for this codebase. It is not a substitute for the book, and it does not override more specific architecture, security, database, or team standards.

The goal is not to predict every future requirement. The goal is to make today's code understandable, testable, and inexpensive to change.

## Core principles

Use three lenses when making design decisions:

1. **Abstraction:** expose the concept a caller needs without leaking incidental implementation details.
2. **Separation:** keep responsibilities that change for different reasons in distinct, composable units.
3. **Readability:** make intent, business rules, and failure behavior apparent to the next reader.

These lenses are deliberately strong. Apply judgment rather than maximizing indirection. An abstraction that has no clear purpose, a separation that fragments a simple operation, or readability achieved through excessive ceremony does not improve the design.

## The development loop

### 1. Start with the user's language

Identify the terms used by product owners, users, APIs, and source files. Use those terms consistently in requirements, tests, contracts, and policy-level code.

- Give one business concept one preferred name.
- Do not reuse the same term for different concepts.
- Translate external vocabulary to canonical internal vocabulary at an explicit boundary.
- Record unavoidable aliases and legacy names at that boundary.
- Avoid names based only on technical shape, such as `data`, `item`, `helper`, or `manager`, when a domain name is available.

If the business says "skill level," policy-level code should not require readers to infer that it means `RatingScaleLevelKey`.

### 2. Define the contract before the implementation

For every public interface, endpoint, message, stored procedure, or reusable component, state:

- accepted inputs and their meanings;
- required and optional values;
- preconditions and invariants;
- successful outputs and observable side effects;
- error outcomes and retry behavior;
- transaction, consistency, and idempotency expectations;
- compatibility requirements.

Represent important contracts in executable tests whenever practical. Documentation describes the agreement; tests detect when the implementation stops honoring it.

### 3. Identify boundaries and reasons to change

Before adding classes or methods, identify the distinct decisions involved. Common boundaries include:

- external format versus internal model;
- validation versus persistence;
- business policy versus technical mechanism;
- orchestration versus individual operations;
- reads versus writes;
- domain decisions versus transport, serialization, or database concerns;
- current behavior versus compatibility adapters for legacy behavior.

Separate responsibilities when they have different owners, failure modes, release cadence, or reasons to change. Keep them together when splitting would only add navigation and ceremony.

### 4. Implement the smallest end-to-end path

Build a thin, working path through the real boundaries before adding refinements. The first slice should prove the contract and integration points, not merely compile isolated scaffolding.

- Prefer the simplest implementation that satisfies the current contract.
- Defer optional generalization until a second concrete use case clarifies the variation.
- Capture deferred improvements explicitly rather than mixing speculative flexibility into the first slice.
- Preserve a runnable, testable state after each meaningful change.

### 5. Review what the implementation teaches

After the first path works, reconsider the design using evidence from the code:

- Did two responsibilities become entangled?
- Did a boundary leak external names or types into the domain?
- Is a repeated decision asking for one authoritative policy?
- Did error handling or transaction behavior become unclear?
- Is an abstraction helping callers, or only moving code?

Refactoring remains expected. Prefactoring reduces predictable rework; it does not eliminate learning.

## Design guidance

### Make code communicate intent

Policy-level code should read as a sequence of domain decisions. Move mechanical detail behind names that explain why the operation exists.

Prefer:

```csharp
if (skillTranslation.IsValidFor(primaryOntology))
{
    await staging.UpsertAsync(skillTranslation, cancellationToken);
}
```

over policy obscured by inline parsing, lookup, persistence, and error-code construction.

Use comments for constraints, tradeoffs, and non-obvious reasons. Do not use comments to compensate for names that hide intent.

### Separate policy from mechanism

Policy answers what should happen. Mechanism answers how it is performed.

Examples:

- Policy: only skills in the primary ontology may be imported.
- Mechanism: join `Tags` to `TagsMetadata_Staging` using organization and ontology identifiers.
- Policy: translations omitted from an upload remain unchanged.
- Mechanism: use merge semantics without a "not matched by source" deletion.

Keep policy visible in orchestration and tests. Encapsulate mechanism so it can change without rewriting the policy.

### Give each unit one coherent job

A method, class, procedure, or module should have a concise purpose that does not require "and then" to explain.

Warning signs include:

- validating, translating, persisting, publishing, and notifying in one unit;
- many boolean parameters selecting unrelated behavior;
- duplicated conditionals encoding the same business decision;
- changes to one rule requiring edits in several layers;
- a unit whose name is broader than the responsibility it actually owns.

Small units are useful when they create meaningful seams. Splitting sequential statements into many pass-through methods without isolating a decision is not meaningful separation.

### Abstract consistently

An abstraction should remain at one conceptual level.

- Do not expose database identifiers from an interface expressed in user-facing terms unless the identifier is part of the contract.
- Do not mix orchestration with low-level serialization or SQL construction.
- Do not wrap an implementation while still requiring callers to understand its internals.
- If a lower-level detail must surface, make that dependency explicit rather than leaking it accidentally.

Prefer complete, narrow abstractions over broad interfaces with optional or partially supported operations.

### Split at boundaries before data becomes ambiguous

Convert data once at each boundary and use a canonical representation within that boundary.

For an upload pipeline, prefer:

```text
File headers
    -> parsed upload row
    -> validated canonical command
    -> resolved persistence model
    -> database records
```

Each transition should have one named mapper or query and contract tests for the mapping. Avoid allowing file-header names, JSON names, DTO property names, and database column names to drift independently.

Example mapping:

| Upload concept | Canonical command | Persistence value |
|---|---|---|
| Skill name | `SkillName` | resolved `TagId` |
| Skill level | `SkillLevel` | resolved `RatingScaleLevelKey` |
| Language code | `LanguageCode` | normalized `LocaleId` |
| Reset/archive instruction | `IsArchived` | archive state or localization removal |

When names differ intentionally, document the reason beside the mapping and test both sides of the boundary.

### Model state and transitions explicitly

When behavior depends on state, define valid states and transitions rather than distributing state checks throughout the code.

- Reject invalid transitions at the boundary closest to the rule.
- Prefer meaningful state names over combinations of loosely related flags.
- Define what repeated commands do.
- Test transition tables, including invalid and idempotent transitions.
- Preserve invariants inside a transaction when multiple records represent one logical state.

### Prefer composition and focused interfaces

Use inheritance only when implementations are behaviorally substitutable through a stable contract. Prefer composition when behavior is assembled from policies or services that vary independently.

Interfaces should represent capabilities needed by callers. Avoid extracting an interface solely because a class exists or because a test framework can mock it.

### Make failures visible and actionable

Never silently discard an unexpected state or failed operation.

- Validate at boundaries and return errors in the caller's vocabulary.
- Preserve the original exception and relevant identifiers when adding context.
- Distinguish validation failures, conflicts, transient failures, and programmer errors.
- Define partial-success and rollback behavior before implementing bulk operations.
- Log once at the layer that can add operational context or make a recovery decision.
- Do not log secrets, personal data, access tokens, or full sensitive payloads.

### Optimize after establishing direction

Choose data structures and algorithms appropriate for expected scale, but measure before introducing complexity for performance.

- Establish a representative baseline.
- Identify the actual bottleneck.
- Record the workload and metric used to justify an optimization.
- Preserve behavior with tests before changing the implementation.
- Prefer structural improvements over fragile micro-optimizations.

## Testing guidance

Tests should clarify the contract, not mirror private implementation steps.

### Test from the outside inward

Use the smallest test level that proves the behavior:

- unit tests for isolated policies and mappings;
- contract tests for schemas, messages, and interfaces;
- integration tests for database, queue, filesystem, and service boundaries;
- end-to-end tests for critical user workflows.

Do not replace a required integration test with mocks that can only prove the assumptions made by the test author.

### Test decisions and boundaries

Prioritize:

- nominal behavior;
- boundary values;
- missing and malformed inputs;
- duplicate and repeated operations;
- state transitions;
- transaction rollback and partial-failure behavior;
- legacy aliases and normalization;
- serialization and field-name mappings;
- authorization and tenant boundaries;
- cancellation, timeout, and retry behavior.

For rules with several conditions, use a decision table before writing individual examples.

### Keep test intent readable

A test should make the rule and expected outcome clear without requiring the reader to reverse-engineer setup noise.

- Name the behavior and condition.
- Keep irrelevant values in builders or fixtures.
- Assert meaningful outcomes, including the absence of unintended side effects.
- Avoid coupling tests to call order or private structure unless order is part of the contract.

## Database and data-pipeline guidance

- Treat schemas, messages, file layouts, stored-procedure parameters, and result sets as versioned contracts.
- Parse external data into a typed staging shape before resolving identifiers or writing target tables.
- Keep user-facing values in validation errors even when persistence uses internal keys.
- Resolve names to identifiers in one authoritative place.
- Make normalization rules explicit, centralized, and covered by examples.
- Use set-based operations for bulk work unless measured evidence requires otherwise.
- State merge semantics explicitly: insert, update, preserve, archive, and delete are different decisions.
- Define transaction scope and behavior for mixed valid/invalid batches.
- Avoid reserved words and ambiguous names in schemas and intermediate shapes.
- Verify that documentation, tests, producers, and consumers use the same field names.

## Change and compatibility guidance

Before changing an existing contract:

1. Find all producers and consumers.
2. Decide whether the change is additive, compatible, or breaking.
3. Prefer an additive transition when independently deployed components are involved.
4. If renaming, support and test the transition period or coordinate an atomic deployment.
5. Update schema documentation, examples, tests, telemetry, and error messages together.
6. Define how old persisted messages or files will be handled.

A rename is incomplete until every producer, consumer, test, and document agrees on the new name.

## Working checklists

### Before coding

- [ ] The user-visible outcome and non-goals are clear.
- [ ] Domain terms and canonical names are identified.
- [ ] Inputs, outputs, invariants, errors, and side effects are defined.
- [ ] Existing implementations and conventions have been inspected.
- [ ] External-to-internal mappings are explicit.
- [ ] Transaction, authorization, tenant, and compatibility boundaries are understood.
- [ ] The smallest end-to-end slice is identified.
- [ ] The test approach covers the riskiest decisions and integrations.

### While coding

- [ ] Policy remains visible and separate from mechanism.
- [ ] Each unit has one coherent responsibility.
- [ ] Abstractions do not leak lower-level details.
- [ ] Names match the domain vocabulary.
- [ ] Mapping and normalization occur once per boundary.
- [ ] Failures are explicit and contain actionable context.
- [ ] Cancellation, transactions, and idempotency are preserved where applicable.
- [ ] Tests are added with the behavior, not deferred until the end.

### During review

- [ ] The change can be explained from contract to persistence.
- [ ] A reader can identify what the code does and why.
- [ ] No business rule is duplicated across layers.
- [ ] New abstractions have a concrete caller and purpose.
- [ ] All contract names agree across code, tests, examples, and documentation.
- [ ] Error and rollback behavior are tested.
- [ ] Security, privacy, and tenant isolation were considered.
- [ ] Performance claims are supported by a representative measurement.
- [ ] Unrelated cleanup is separated from the functional change.

## Resolving tradeoffs

These guidelines may pull in different directions. Resolve conflicts in this order:

1. Preserve correctness, security, privacy, and data integrity.
2. Honor the externally visible contract.
3. Make the business policy understandable.
4. Keep likely changes local.
5. Minimize accidental complexity.
6. Optimize measured hot paths.

When a material tradeoff is not obvious, record the decision and its context in the pull request, design note, or architecture decision record.

