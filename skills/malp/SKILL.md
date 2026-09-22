---
name: malp
description: "Map · Altitude · Learn · Plan — recon before anything expensive or hard to reverse (a migration, a destructive fix, killing processes, a big fan-out, a claim to a human). Produces a GO/NO-GO and the name of the instrument that would prove you wrong. Does NOT act. Usage - /malp <what you are about to do>"
---

# /malp — Map · Altitude · Learn · Plan (recon only)

Get into position and decide **whether** to act. This skill stops before execution.

**The product is a POSITION and a GO/NO-GO — not work.** If you finish holding a diff,
you ran the wrong skill.

---

## THE ALTITUDE LAW — this is the whole skill; the phases are scaffolding

> ### You may not climb on your own report.
> "Altitude" — the confidence to act — is decided against an artifact **you did not
> author**: telemetry, a gate's exit code, a file's actual bytes, a human's answer.
> Your summary of what you saw is not an instrument.
>
> ### Can't name the instrument that would tell you you're WRONG? Then you aren't at altitude — you're just high. **BLIND = NO-GO.**

- **The tell:** proceeding on *"nothing is running," "that's stale," "it already
  landed," "nobody depends on this"* — where the thing that told you so was a command
  you wrote, read once, and never checked for blind spots.
- **A real near-miss:** an agent scanned for running processes **by window title**,
  got **0**, and was one command from migrating a message bus out from under **12 live
  processes**. Background PowerShell has no window title. A command-line scan found
  all 12. The same night, another agent's process scan matched **its own pipeline**,
  twice.
- **Falsifier:** a domain where your own reading is the only instrument *and* a long
  record shows your unbacked calls were never contradicted. Then your judgement is the
  instrument. Until that record exists, it isn't.

**Corollary — a zero is the most dangerous reading on the board.** "0 results," "0
processes," "0 matches" look exactly like "my filter was wrong." Before acting on a
zero, prove the instrument *can* return non-zero.

---

## THE FOUR PHASES

**🗺 MAP — scout, don't solve.** Name what you'll touch, what it connects to, and what
you'd break. Read the actual file / config / process list — not your memory of it.
→ *the blast radius, written down.*

**⛰ ALTITUDE — step up, then run the gate.** Go to where the decision lives, not where
the work lives. Name the instrument, name what a wrong answer would look like, and
prove the instrument can produce one. Human present → ask them for go/no-go. Unattended
→ telemetry-verified only. Blind → **no-go**, always.
→ *GO or NO-GO, plus the instrument's name.*

**🔍 LEARN — gather against the gaps ALTITUDE exposed.** Parallel reads are free;
serialize anything that writes. Prefer a second **independent** instrument over a
second look at the first one (self-review of your own prose catches ~nothing; re-reading
raw rows catches real defects).
→ *evidence, with coverage stated: what you sampled, what you couldn't reach.*

**📐 PLAN — synthesize, and name the owner.** State the change concretely enough that
whoever executes doesn't have to re-solve it. Include a rollback, and an acceptance
test **asserted at the destination, not by an exit code**.
→ *a plan someone else can run, and a name.*

---

## OUTPUT CONTRACT

```
GO      instrument: <what you checked, and what a wrong answer would have looked like>
        owner:      <who executes>
        plan:       <concrete change>   rollback: <exact undo>
        acceptance: <asserted at the destination>

NO-GO   blocked on:      <the missing instrument or unanswered question>
        who unblocks:    <person or system>
        what would change the answer: <the specific measurement>
```

**If every run returns GO, this has become a ritual.** Keep your no-gos. A no-go is a
result, the way a red test is a result.

---

## WHAT THIS IS NOT

| you want | use |
|---|---|
| do a multi-step task carefully, end to end | `/turn` — it **executes** |
| scope a multi-agent fan-out before paying for it | `/lean` |
| prove a check can fail before trusting it | `/gate`, `/verify-battery` |
| pre-commit an experiment before spending compute | `/preregister` |
| **get into position and decide whether to act at all** | **`/malp`** |

`/turn` runs to completion. MALP's whole product may be *not proceeding.*

---

*Reposition until the strike is inevitable. Then let the right hand throw it.*
