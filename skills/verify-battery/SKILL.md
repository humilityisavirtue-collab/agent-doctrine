---
name: verify-battery
description: "Two-population verification battery. Before certifying that a reimplementation, transform, quantization, or pipeline is 'correct', measure how far a FAITHFUL version deviates and how far KNOWN-BROKEN versions deviate — the threshold lives in the gap. Usage - /verify-battery <artifact>"
---

# /verify-battery — Prove the Checker Before You Trust the Check

You're about to write *"X is a correct replacement for Y"* — a rewritten kernel, a
quantized model, a ported pipeline, a new grader. Any threshold you quote is a guess
until you've measured **two populations**: what correct looks like, and what broken
looks like.

Every rule below cost a real mistake once.

---

## The shape (always the same five pieces)

1. **LOWER population — the faithful distribution.** Run the CORRECT artifact across a
   varied input battery. Its worst deviation is the ceiling. **Not** the same-code
   noise floor — a faithful *reimplementation* legitimately deviates more than
   same-code jitter does. Calibrating on jitter makes every honest rewrite read RED.
2. **UPPER population — injected known-breaks.** A grid: several break *classes* ×
   several *sites* (layers, stages). In-memory only; the original artifact stays
   byte-untouched. Include both **data** breaks (corrupted weights/values) and
   **construction** breaks (wrong wiring) — they fail differently.
3. **Threshold** sits in the gap between the populations (geometric midpoint, with
   guard bands). **The author never freezes it.** Propose it; someone else ratifies it.
4. **Gap-collapse watch.** Any break class that lands at or below the faithful ceiling
   is a **finding**: deviation-gating structurally *cannot* catch that class, so it
   needs a different check (usually a build-time invariant assert). **Withhold** the
   threshold when a class collapses. Never quietly tighten it until the collapse
   disappears.
5. **Checkpoint every leg** — atomic writes, resumable. Long grids die to external
   kills; a battery that can't resume is a battery you'll finish 0.8 times.

## The control laws (every one fired in a real run)

- **A control must provably perturb THE OUTPUT, not an intermediate.** Perturbations
  can cancel downstream:
  - Casting bf16 → bf16 on weights that were already bf16 is the identity.
  - A *uniform* RoPE position shift cancels in every q·k product (relative encoding)
    and matched the faithful run to floating-point jitter. The version that actually
    fires is the *mismatched* break: shift k, not q.

  **If a break's deviation matches the faithful run, the control is theater.** Find out
  why before you trust anything else the battery says.
- **Reference precision sets the floor.** Check what your reference actually computes.
  (Triton's `tl.dot` silently runs TF32 on fp32 inputs; a bf16 reference makes an exact
  kernel read RED.) A verdict thinner than your measurement noise is an artifact. Put
  the reference dtype in the receipt.
- **Multiple seeds / inputs, or it's luck.** One input is not a population. Widening
  the battery should **widen** the gap if the separation is real. In one run, the
  subtlest break's deviation rose 0.0044 → 0.0115 with five more prompts while the
  faithful ceiling held still. That's the signature you want.
- **Injections are in-memory clones only.** Any mtime change on the original = abort.

## Build checklist

- [ ] Varied input battery (≥5, mixed kinds), references cached and keyed on
      **artifact state AND input hash** (a stale cache is a silent false green)
- [ ] ≥4 break classes × ≥3 sites, parameterized as `class@site`
- [ ] Each break class verified potent **at the output** before the grid runs
- [ ] Per-leg checkpoint file, resumable, atomic writes
- [ ] Analysis: per-class min/max table, the ceiling, the collapse list, the
      proposal (withheld on collapse) — as a machine-readable JSON receipt
- [ ] Someone other than the author ratifies the threshold. You report; you don't stamp.

## When to invoke

Any time the sentence *"X is a correct replacement for Y"* is about to be written:
rewritten kernels, model surgery, quantized serving paths, LLM-output graders,
format converters.

**No upper population → the gate is a rubber stamp.
No faithful population → the threshold is a guess.**
