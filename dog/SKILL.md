---
name: dog
description: 'Use when investigating Degreed runtime behavior or verifying a deploy in staging/beta/production — observability questions answered by Datadog logs and custom metrics: errors, regressions, "is this happening in prod", "did my change take effect", "why is X failing in staging".'
---

# Degreed in Datadog

Datadog is the source of truth for deployed-environment logs and custom metrics — reach for it proactively when investigating runtime behavior in staging/beta/production or verifying a deploy.

> **Scope caveat (important):** Everything below describes **application logs and custom metrics**. **Traces and infrastructure/Kubernetes logs+metrics use related-but-inconsistent tags** — do not assume these conventions hold there (customer isolation via `@seid` may not exist in traces at all; discover trace tags via the `datadog/traces` guide). Query via the MCP in **UTC** — results come back as `…Z` and relative windows (`now-7d`) are simplest. (The Datadog web UI shows each user's *configured* timezone, which may be local, so confirm the zone of any wall-clock time you're given before converting.)
>
> For Datadog query *syntax*, load the MCP's own guides (`datadog/logs`, `datadog/metrics`, `datadog/traces`, `datadog/visualizations`). This skill covers only the Degreed-specific conventions.

## Environments (`env`)

| `env` | What | Lane | Facing |
|---|---|---|---|
| `staging` | closely tracks `main` | staging | internal (US) |
| `release` | next `release/*` to be promoted | release | internal (US) |
| `beta` / `europebeta` | runs the next-to-prod `release/*` | beta | customer (US / EU) |
| `production` / `europe` / `canada` | current production `release/*` | production | customer (US / EU / CA) |

Quirks: US has no region suffix; there is **no Canada beta**; there is **no `dev` env** in Datadog (intentional — devs run components locally).

**Choosing `env`:** anything tied to `main` or a just-merged change → use `staging` automatically. For any customer/production question, **ask first which environment** ("US production, Europe, or Canada?") — never guess the region.

## Components (`source`)

Filter components with `source:<app>`, where `<app>` is the `App` enum **lowercased** (source of truth: `trunk/Degreed.Core.Standard/Infrastructure/Enums.cs`). Common values: `vnext`, `appevents`, `integrationsrunner`, `sqlwatcher`, `eventhubimport`, `dataimport`, `organizationinbound`, `lowprioritybackgroundevents`.

`source` identifies an **app, not a feature** — a feature like learning search runs *inside* an app (`appevents`/`vnext`), so narrow to it with `@logger.name` (class/namespace), not a dedicated source.

> **Gotcha:** `source:elasticsearch` is the SQL→ES bulk-sync webjob (`trunk/WebJob.Elasticsearch`, often called "bulk sync"; ServiceBus-triggered), **not** the Elasticsearch cluster.

> Logs are tagged `source` only; custom metrics carry both `source` and `service`. **Use `source:` everywhere.** (A future move to `service:` is planned but stalled.)

## Service Environments (`@seid`)

A "service environment" (really a **data context**) is a data-isolation unit. Each holds its own SQL, Elasticsearch, and Snowflake; compute and everything else is shared. **Every organization belongs to exactly one service environment**; a service environment may host many orgs.

- `@seid` values look like `dgscu-default`, `dggwc-siemens`, `dgcacca-default`, `dggwceu-prodse05`.
- An id is unique **within a lane**, but the same id can exist in multiple lanes (e.g. `dgscu-default` exists in every lane). So always pair it with the env/lane: `env:europe @seid:<id>`.
- To isolate one customer's data/behavior inside a shared env, filter by `@seid`. A shared SE hosts **many** orgs, so to narrow to a single org also filter `@orgid` or `@orgcode` — neither is consistently present, so try whichever is on the logs in question.
- **Resolve org/domain → `seid`** via two Datadog reference tables (searchable in the Datadog UI). The MCP has **no reference-table tool**, so an agent can't query them directly — ask the user to look the org/domain up there (or to supply the `seid`):
  - **`org_directory`** — org → `seid`/`env`/`lane`, by org id, `orgcode`, or `*.degreed.app` domain. Org id is unique only within a lane, so when you know the lane but not the region, look up by `lane` + `orgid` — that pair is unique, so it returns one row and tells you the region.
  - **`service_environments`** — the service-environment catalog, keyed by the globally-unique `*.degreed.com` default domain → `seid`/`env`/`lane`/region.
- **Domains pin a service environment.** All Degreed domains are globally unique: a `*.degreed.com` default domain identifies the env + service environment; a `*.degreed.app` org domain also identifies the org. A customer-specific URL is a strong starting point for scoping a query.

## Reliable log attributes

| Attribute | Notes |
|---|---|
| `status` | standard `error` / `warn` / `info`, used reliably |
| `@logger.name` | `Full.Namespace.ClassName` — fully consistent; often the best filter |
| `@host` | pod/instance host; use to tell instances apart |
| `@seid` | service environment (see above) |
| `@userkey` | maps to `UserProfileKey` (sometimes present) |
| `@orgid` | maps to `OrganizationId` — sometimes present |
| `@orgcode` | maps to org `Code` — sometimes present |

## Key custom metrics

Prefix `degreed.*`; tagged with the same `env` + `source` as logs. **Not tagged with org** (`orgid`/`orgcode`) due to cardinality limits — you can't scope a metric to one organization; org-level analysis is logs-only.

**Sign-of-life / heartbeats:**
- `degreed.config.time` — accidental but reliable heartbeat. Instance count across k8s *and* app services (swap `source:vnext` for the component you're checking): `count(sum:degreed.config.time{source:vnext} by {host}, { * })`.
- `degreed.webjob.status` — intentional webjob heartbeat.

**Big 3 data sources:**
- **SQL:** `degreed.sqlclient.connections_active`
- **Elasticsearch:** `degreed.request.elastic.success` / `degreed.request.elastic.failure` — `.failure` increments when the .NET Elasticsearch client's error handler fires (4xx, 5xx, and transport errors; exact triggers depend on the client library)
- **Redis:** `degreed.redis.request.count`

**ServiceBus (webjobs):** `degreed.servicebus.consumed` / `degreed.servicebus.sent`.

## "Did my change deploy yet?" (before verifying a fix)

`staging` closely tracks `main`, and the staging deploy pipeline (`Degreed.Platform.Dev`) usually **starts at the top of the hour**. To confirm a specific commit is in the deployed build, use the `az` CLI: `az pipelines build show --id <id> ...` for the build's `sourceVersion`, then check your commit is in its git ancestry. **Don't manually enqueue** a build — staging deploys are long; wait for the next top-of-hour run.

## Verifying a fix

Query the relevant logs (e.g. `env:staging source:vnext "<error text>"`) and confirm the count drops after the deploy. **Check across all components, not just where you first saw it** — one root cause often surfaces in several (`source`)s (web, webjobs, health checks); a single-`source` filter can read as "all clear" while the error continues elsewhere.