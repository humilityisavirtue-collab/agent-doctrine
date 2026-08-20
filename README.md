# Agent Doctrine

**Operating laws for AI agents that have to be trusted. Every law carries the evidence that would prove it wrong.**

Your agent said "done, tests pass." The tests did pass. The fix was real. It still didn't work.

If you have shipped anything with an LLM agent in the loop, you know this failure. It is not
a hallucination and it is not incompetence — the agent read the code, reasoned correctly, and
reported honestly on a check that could never have failed in the first place.

This repository is the doctrine a working 8-agent system uses to make that harder. It is not a
framework and there is nothing to install. It is the set of rules the agents are held to, in
the format that makes rules survive contact with a smart system that wants to agree with itself.

---

## The 60-second version

```bash
git clone https://github.com/humilityisavirtue-collab/agent-doctrine
cd agent-doctrine/example
python vacuous_gate.py
```

No dependencies. It prints two safety checks. Both pass their tests. One of them has never
been capable of failing, and the pass counts make the broken one look *better*:

```
gate_vacuous
    n=7  passed=7  rejected=0
    confidence values the source can emit: [0.0, 0.25, 0.75, 1.0]
    CAN THIS GATE EVER RETURN FALSE?  NO -- IT IS VACUOUS

gate_real
    n=7  passed=2  rejected=5
    CAN THIS GATE EVER RETURN FALSE?  YES
```

Then `python vacuous_gate.py --mutants` proves the vacuity checker itself has teeth, because a
checker that never catches anything is the same defect one layer up.

---

## The format, and why it is the actual contribution

Anyone can write "always verify your work." That advice has never once stopped a confident
agent, because it has no failure condition — it cannot be checked, only agreed with.

Every law here is **can-fail**. It carries four things:

| field | what it does |
|---|---|
| **Tell** | the observable signal that you are breaking it *right now* |
| **Prevents** | the specific, dated incident that cost us something |
| **Falsifier** | the conditions under which this law is **wrong** and you should ignore it |
| **Retire-when** | what would have to become true for this law to be deleted |

A law without a falsifier is a slogan. Slogans lose arguments to a sufficiently clever agent —
including the clever agent that is *you*, at 2am, wanting to be finished.

---

## Four laws that carry most of the weight

**No green on belief — not the author's, not the model's, not your own.**
"It imports." "It's clean." "Should clear now." None of those are green. Green is a run that
could have failed and didn't. Whose mouth the claim comes from changes nothing.
*Falsifier: an author whose "done" has never once been contradicted by a run, across a long
record — then their claim is evidence. Retire-when: never, until that record exists.*

**A negative control must mirror the real failure, or it is theater.**
A green test means something only if it could have gone red *for the reason the thing actually
breaks*. Gibberish input that fails while the real failing input passes is a blind spot wearing
a lab coat.

**Run → read the real output → then report.**
A message carrying numbers has a hard data dependency on the run that produced them. Batching
the report with the run is pasting numbers before they exist. This one is mechanical, not
heuristic — we have never found a falsifier for it.

**Carry the evidence, not the conclusion.**
Ship the raw output that made you conclude — the actual value, the literal error, the real
shape — not your paraphrase. A correct diagnosis the receiver can re-interpret is still a
belief handoff, and belief drifts. *Three rounds of an accurate "the matrix is transposed"
didn't land. The literal `w_k.shape = (3584, 512)` landed in one.*

Full set in [LAWS.md](LAWS.md). Role-specific cards in [doctrine/](doctrine/).

---

## Where this comes from

These were not designed. Every one of them is scar tissue from a specific failure in a running
multi-agent system, and the cards keep the incident attached because the incident is what makes
the law survive an argument.

The system they govern is private. The scale, counted rather than estimated — **with the predicate
beside each number, so a re-run settles the claim instead of forking it:**

| measured | count | predicate |
|---|---|---|
| verification gates | **136** | `ls cell/verify/gate_*.py` — **146 repo-wide**, 10 live outside that tree |
| …naming a negative control | **27** | regex `neg(ative)?[ _-]?control`, case-insensitive |
| …carrying a named mutant table | **24** | literal token `MUTANTS` |
| …carrying **both** | **5** | both of the above |
| role cards / laws / falsifier clauses | 12 / 36 / 45 | `^### ` and `falsifier` in `cell/doctrine/*.md` |
| private memory cards / recording a falsifier | 398 / 40 | `*.md` count; `falsif` text match |

**Read those middle rows again: most gates carry neither, and only 5 of 136 carry both.** That is
the honest fraction. The discipline is real and it is nowhere near universal.

Two warnings about the numbers themselves, which matter more than the numbers:

**The scope is stated because an unstated one is unfalsifiable.** "136 gates" without naming the
surface invites a reader to re-derive it repo-wide, get **146**, and conclude the front page is
wrong. Same number, different population, no way to tell which was meant. Ship the command.

**These are text matches, not audits.** A gate can implement a negative control perfectly without
using the phrase, and an AST pass looking for a *code identifier* named `neg_control` finds
**zero** of 136 — the discipline lives in prose and ad-hoc asserts, not in a named construct
anyone could grep for reliably. Treat every count here as a lower bound on a loose proxy.

That paragraph originally read "143 of them carrying negative controls" — a number larger than
the population it claimed to be a subset of, produced by silently swapping two different
populations, sitting on the front page of a repo about exactly that error. It survived being
written, reviewed, and published. It was caught by re-running the count, which is the only thing
that ever catches it. Law 11 and Law 13, demonstrated at our own expense; the original wording is
in the git history.

The doctrine is the transferable part, so it is the part that is public.

The agents are named by suit — Spade forms claims, Club proves them, and the pair is a
pipeline rather than a hierarchy. You do not need that structure for the laws to apply. Rename
them to "author" and "reviewer" and nothing changes.

---

## What this is not

- **Not a framework.** Nothing to install, no runtime, no dependency on our stack.
- **Not benchmarked.** We have not run a controlled study showing these laws improve agent
  reliability by X%. They are field-tested, not measured, and saying otherwise would break
  the first law in the file.
- **Not finished.** Several cards have laws whose retire-when has partly arrived. Those are
  marked in place rather than quietly rewritten.

If a law here is wrong, its falsifier tells you exactly what evidence would prove it. Bring
that evidence — that is the whole point of writing them this way.

---

MIT. Use them, fork them, argue with them.
