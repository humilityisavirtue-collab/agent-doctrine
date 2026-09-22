---
name: preregister
description: "Scaffold a pre-registered experiment protocol before spending compute — gates that block spend, CI + effect-size floors, mechanism-matched controls, paired seeds, staged authorization, a falsifier table. Use before designing any eval/training run or before ANY GPU or paid-compute spend. Usage - /preregister <experiment name>"
---

# /preregister — Decide What Would Prove You Wrong Before You Spend

Distilled from an architecture experiment where this shape saved 25–50 GPU-hours
across two runs that would otherwise have been wasted, and turned an ambiguous null
into a cheap, decisive answer. Every section below earned its place by catching a
real mistake.

## Produce a protocol doc with these sections

1. **Thesis + confound ladder.** State the claim, then list everything ELSE that could
   produce a positive. The decisive comparison is treatment vs. **the control that
   isolates the thesis** — often *not* treatment vs. baseline.
   *(Example: B-vs-A said "the extra heads help." B-vs-C said "the **semantics** of the
   heads help." Only the second was the thesis.)*
2. **Oracle.** One verifiable number, no LLM judge. Declare the read-out rule: paired
   deltas, what cancels, and what is explicitly NOT the metric.
3. **Gates that BLOCK spend.** Cheap CPU checks that must pass before any expensive
   run counts — ordered so an upstream failure can't masquerade as a thesis verdict.
   ("The classifier was broken" ≠ "the idea failed.") **Every gate must be able to
   fail;** show that it can.
4. **Floors, both kinds.** Significance (bootstrap 95% CI clears the null) **and**
   effect size (a pre-registered materiality threshold). At large n a trivial effect is
   significant — significance is not materiality.
5. **Mechanism-matched controls.** The control shares the treatment's *mechanical*
   structure and destroys only the *meaning*.
   *(Example: shuffling address labels also broke the overlap between context windows,
   which inflated every "lift." The honest control re-addressed shuffled tokens. Ask:
   **what does my shuffle destroy besides meaning?**)*
6. **Paired seeds, fixed budget, no early stopping.** n ≥ 5 seeds; each seed governs
   init AND data order identically across variants; judge the final checkpoint at a
   fixed token/step budget.
7. **Declared freedoms.** Any direction choice, sign freedom, or extrapolation beyond
   the measured evidence gets written down **before run 1**.
8. **Staged authorization.** Cheapest-first spending plan with named review points:
   floor check → primary comparison → attribution variants **only on a win**.
   Pre-commit the stop rule: *"no win at n=5 → stop, report the null as a result."*
9. **Falsifier table.** Rows = observable outcome patterns; column = the verdict each
   one forces. Include rows for **"mis-instrumented," "the data can't carry the
   structure,"** and **"capacity-limited, result void."**

## Review

Have someone who is not the author read the protocol **before** the first paid run —
a person, or a fresh agent session with no memory of writing it. That review is the
single highest-value line in the whole protocol. Don't skip it because the design
"feels obvious"; that feeling is what the protocol exists to check.
