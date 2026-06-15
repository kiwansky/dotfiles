---
name: debug
description: Systematic root-cause debugging — reproduce, isolate, hypothesize, fix, verify. Use when the user reports a bug, unexpected behavior, a failing test, or asks to "debug" or "figure out why" something happens.
---

# Debug

Find the root cause before changing code. No guess-and-patch.

## Steps

1. **Reproduce.** Get a reliable reproduction first — ideally as a failing automated test, otherwise a command or minimal script. If you can't reproduce it, gather more information (exact input, environment, logs) before touching code.
2. **Gather evidence.** Read the error message and stack trace fully. Check logs, recent changes (`git log` on the affected files), and the state at the failure point. Add temporary logging or use a debugger where needed — and remove temporary instrumentation afterwards.
3. **Isolate.** Narrow the failure: binary-search the input, the code path, or the commit range (`git bisect` when a regression). State what is ruled out as you go.
4. **Hypothesize, then verify the hypothesis** against the evidence before fixing. If the evidence contradicts the hypothesis, form a new one — don't pile fixes onto a guess.
5. **Fix the root cause**, not the symptom. If only a workaround is feasible, label it as such and explain what the real fix would require.
6. **Verify.** The reproduction from step 1 must now pass, and the project's test suite and lint/build must stay green. Keep the reproduction as a permanent regression test where practical.
7. **Summarize**: root cause, why it manifested as the observed symptom, and what the fix changes.

## Rules

- Never claim a bug is fixed without having seen the reproduction fail before and pass after the change.
- If the root cause lies outside the requested scope (dependency, infrastructure, other module), report it rather than patching around it silently.
- If debugging stalls, present the evidence collected and the hypotheses ruled out, then ask for input — don't loop on random changes.
