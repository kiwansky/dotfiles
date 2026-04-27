# Observability Standards

Practical guidance for instrumenting, logging, tracing, and alerting. Used by `software-engineer`, `software-architect`, and the dedicated `sre` agent.

The goal of observability is to answer **"what is the system doing right now, and why?"** — fast enough to ship, debug, and respond to incidents without grinding through code.

## The Three Pillars

### 1. Logs — what happened
Discrete, timestamped events. Best for debugging individual requests and post-hoc forensics.

- **Structured (JSON) only.** Free-text logs are unsearchable at scale.
- Mandatory fields: `timestamp`, `level`, `service`, `message`, `correlation_id`, `user_id` (if applicable, hashed/pseudonymized).
- Levels: `DEBUG` (off in prod), `INFO` (state changes), `WARN` (recoverable), `ERROR` (failed operation), `FATAL` (process-level).
- **Never log secrets, PII, full request bodies, or auth tokens.** Redact at the logger, not at the call site.
- Sample high-volume info logs in prod; keep all errors and warns.

### 2. Metrics — how often / how much / how fast
Aggregated, low-cardinality numerical data. Best for dashboards, SLOs, and alerts.

- **RED method** for services: **R**ate (req/s), **E**rrors (% failed), **D**uration (latency distribution, especially p50/p95/p99).
- **USE method** for resources: **U**tilization, **S**aturation, **E**rrors.
- Keep cardinality low: do not include user IDs, request IDs, or unbounded values as labels.
- Histograms over averages — averages hide tail latency.
- Standardize unit suffixes: `_seconds`, `_bytes`, `_total` (counters).

### 3. Traces — where did the time go
Distributed context across services. Best for cross-service debugging and latency analysis.

- Use OpenTelemetry. Avoid vendor-specific SDKs at the edge.
- Propagate `traceparent` / `tracestate` headers across every service hop.
- Sample intelligently: 100% of errors, ~1–10% of successes, plus head-based sampling for long traces.
- Tag spans with `service.name`, `http.method`, `http.route`, `db.statement` (sanitized), `error=true` on failure.

## Correlation IDs

Every request gets a correlation ID (often `X-Request-ID` or the OTel trace ID). Propagate it through:
- Logs (every log line carries it)
- Outgoing HTTP / gRPC / queue messages
- Background jobs spawned from a request

Without correlation, logs are noise. With it, you can reconstruct any request's full journey in seconds.

## SLOs & Alerts

- **SLI** (indicator) — a measurable signal: "99% of requests under 500ms".
- **SLO** (objective) — the target: "99.9% over 30 days".
- **Error budget** — what's left of the SLO this period. When it depletes, slow rollouts.
- **Alert on symptoms users notice**, not on causes. "Error rate > 1% for 5 min" is a symptom; "CPU > 80%" is rarely worth a page.
- **Page on actionable alerts only.** If there's no specific action a human can take, it's not a page — it's a dashboard.

## Tracing Anti-Patterns

- Logging the same fact at multiple log levels "just in case"
- Putting full request/response bodies in logs
- Metrics with user-ID-level cardinality
- Trace sampling that drops error traces
- Alerts that page without a runbook
- Dashboards with 50+ panels — nobody scans them

## Instrumentation Checklist

For any new service or significant feature:

- [ ] Structured logging with correlation IDs
- [ ] RED metrics emitted for every external endpoint
- [ ] Healthcheck endpoint (separate from readiness)
- [ ] Readiness endpoint that fails when downstream deps are unreachable
- [ ] OpenTelemetry tracing with parent context propagation
- [ ] No secrets, no PII, no full bodies in logs
- [ ] At least one SLO defined (latency or availability)
- [ ] At least one alert wired to oncall, with a runbook link
- [ ] Dashboard exists and is linked from the service README

## Runbook Standards

Every paging alert links to a runbook. A good runbook has:

1. **What this alert means** — in plain language, not just the metric query.
2. **Likely causes** — top 3, most common first.
3. **Diagnostic steps** — concrete commands and dashboards, not "investigate the system".
4. **Mitigation options** — including the "do nothing, wait" option if applicable.
5. **Escalation path** — who to call if you can't resolve.
6. **Last incident link** — for context on past occurrences.

## Postmortem Practice

Every incident producing customer impact gets a postmortem in `/docs/postmortems/`. See `/postmortem` command for the orchestrated workflow. Postmortems are **blameless** and focused on systems, not individuals.
