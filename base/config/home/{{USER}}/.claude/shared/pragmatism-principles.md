# Pragmatism Principles

Clean Code (`clean-code-principles.md`) tells you *how* to write good code. Pragmatism tells you *when not to* — when a "clean" solution is the wrong solution because it's premature, speculative, or expensive.

These two sets of principles are in deliberate tension. Resolve the tension by leaning **pragmatic when uncertainty is high** (early product, MVP, exploration) and **clean when uncertainty is low** (mature system, well-understood domain, code that will be touched many times).

## Core Principles

### YAGNI — You Aren't Gonna Need It
- Build what is needed now, not what *might* be needed later.
- Three similar lines is better than a premature abstraction. Wait for the *third* duplicate before extracting.
- Don't add configuration flags, plugin systems, or extension points until a real second use case exists.
- An unused abstraction has zero value and non-zero maintenance cost.

### Worse Is Better (Gabriel)
- Simplicity of implementation beats simplicity of interface.
- 80% solutions that ship beat 100% solutions that don't.
- Correctness, simplicity, completeness — pick what matters in *this* context. They aren't all equal.

### Reversible vs. Irreversible
Decisions split sharply by reversibility:
- **Reversible** (file structure, naming, internal interfaces): move fast, fix later.
- **Irreversible** (public API, data schema, external contracts, dependency choices): slow down, gather evidence, write it down.

Treat them differently. Most teams over-deliberate on reversible decisions and under-deliberate on irreversible ones.

### Fit Complexity to Stakes
- A throwaway script doesn't need tests, error handling, or DI.
- A payments path needs all three — and probably more.
- Match rigor to consequence. Cargo-culting "best practices" onto every change is its own anti-pattern.

### Prefer Deletion to Abstraction
- Code you delete cannot have bugs.
- The best abstraction is often "just don't have this code."
- When in doubt: inline, don't extract.

## When Clean Code Wins (apply strict)

- The code is on a hot path touched by many engineers
- The system is mature, the domain is stable, the patterns are repeated
- The cost of change is high (database schemas, public contracts, security boundaries)
- A test is hard to write because the structure is wrong → fix the structure

## When Pragmatism Wins (apply loose)

- MVP, prototype, spike, exploration
- Code with uncertain lifespan or unknown second user
- Performance-critical paths where abstraction has measurable cost
- One-off scripts, migrations, or glue code
- Three or fewer similar instances — wait for the pattern to clarify

## Decision Heuristic

Before adding any abstraction, ask:

1. **Is the second use case real, or hypothetical?** Hypothetical → don't.
2. **Could a future engineer read the inline version in under 60 seconds?** Yes → keep inline.
3. **What would I delete if I were wrong about the future need?** If the answer is "a lot," push back.
4. **Is this abstraction earning its complexity in *every* call site, or just one?** If just one → inline.

## Red Flags (pragmatism-specific)

- "We might need this someday" → no.
- "Let's make it configurable" → only if a real second config exists.
- A single-implementation interface introduced "for testing" → use a real fake or test double, not an interface.
- Adapter / wrapper / facade layers that exist because "clean architecture says so" but pass data through unchanged.
- Generics or type parameters used for one concrete type.
- "Future-proofing" justifications without a named, dated future requirement.

## Tension Resolution

When clean-code rules and pragmatism rules conflict in a specific situation:

| Situation | Default |
|-----------|---------|
| Early-stage product, exploring problem space | Pragmatism |
| Mature product, known patterns | Clean Code |
| Internal-only code, one team | Pragmatism, with discipline |
| Public API or library | Clean Code, with rigor |
| Performance-critical path | Pragmatism (then measure) |
| Security-sensitive path | Clean Code (no shortcuts on validation, secrets, crypto) |
| Throwaway script | Pragmatism, full stop |
| Migration scaffolding | Pragmatism (it deletes itself) |

**When in doubt, favor the simpler option and add complexity only when forced.** It is far cheaper to add abstraction later than to remove it.
