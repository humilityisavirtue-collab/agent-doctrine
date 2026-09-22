---
name: lean
description: "Lean dispatch for subagents and multi-agent workflows. The cost of an agent is mostly its NUMBER OF REQUESTS, not its dispatch — so scope each agent tightly, spawn fewer, use the cheapest model that fits, and prefer forks when the parent context is small. Use before spawning agents or designing a fan-out."
---

# /lean — Scope the Agent, Not Just the Count

This skill has been wrong twice, publicly, and it's better for it. Both corrections
are kept below, because **the lesson is the correction.**

---

## What was measured

Across **109 real subagent transcripts** from one Claude Code setup (medians, rows
deduplicated by `message.id`):

| what | median |
|------|--------|
| **first request** (the dispatch cost) | **~25k tokens** |
| **whole-agent lifetime input** | **~444k tokens** |
| **requests per agent** | **10** |

**An agent's lifetime costs ~18× its dispatch.** Dispatch is the *small* term.

These are one setup's numbers — your system prompt, tools, and task mix will move
them. Re-measure yours (method at the bottom). The *shape* is what transfers.

### Correction 1: "file reads are the big leak" — wrong
The first version of this skill assumed reads were ~90% of dispatch cost. Measured: a
file read adds roughly **1k tokens** to the request that makes it. (Context added early
*is* re-read by every later request, but at cache-read rates.)

### Correction 2: "~59k per-agent floor" — right number, wrong noun
An early measurement found ~59k tokens per agent and called it a floor. It was the
**entire life** of six very short agents (~2 requests each), not a minimum. Real agents
run ~10 requests; the floor framing was 2.4× too high on dispatch and 7.5× too low on
lifetime.

---

## The levers, in order of real impact

1. **SCOPE THE TASK. Requests per agent is the cost.** An agent that answers in 3
   requests is far cheaper than one that grinds through 30 — and **that gap dwarfs how
   many agents you spawn.** One deliverable, a clear done-condition, and enough inline
   context that it doesn't go exploring.
2. **Fewer agents.** Still worth asking every time — don't fan out to four what one can
   do, and never spawn an agent to check a single thing you could read yourself. Just
   know you're optimizing the ~25k term, not the ~444k one.
3. **Cheapest model + effort that fits.** Authoring, editing, transforming → a smaller
   model at low effort. Save the top model and high effort for real synthesis or
   judgement. (Check current per-token pricing; the ratios between tiers are large.)
4. **Prefer a fork when the parent context is small.** In Claude Code, a forked agent
   reads the parent's **cached** prefix instead of paying fresh prefill (measured ≥97%
   cache reads, 14/14 forks). Above roughly 200–250k tokens of parent context, a fresh
   agent wins. A fork isn't free — it runs its own requests, and that's where its cost
   lives.
5. **Smaller toolset / inline context.** Real but second-order. Its actual payoff is
   stopping agents from wandering — which cuts *requests*.

---

## Writing a lean dispatch

- **Ask first: can ONE agent do this instead of three?**
- Pick the cheapest model + effort that fits.
- Inline the context. State **one** deliverable. Give it a check that **can fail**.
- End with *"return ONLY X"* — so the return value is the payoff, not a travelogue.
- Reserve the expensive tier for the single stage doing real reasoning.

## When a fan-out IS worth it

- **Genuine exploration** of an unknown codebase — discovery *is* the task, and
  inlining a guess wastes more than it saves.
- **Judgement on raw material** (code review, security audit) — a parent's summary can
  hide the very bug the agent is supposed to find. Let it see the source.
- **Genuinely parallel work** where each shard buys real wall-clock or coverage. Then
  fan out deliberately — and put the effort into scoping each shard tightly rather
  than shaving the count.

---

## Re-measuring on your own setup

Claude Code writes subagent transcripts as JSONL. Sum `usage` input tokens
(`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`) per request.

**Deduplicate by `message.id` — never by a usage signature.** One response is written
as one row *per content block*, and the usage fields repeat across those rows; keying
on the usage values instead of the id missed most multi-row messages and inflated every
total by ~1.8×. (This holds where message ids are server-assigned. Some local-model
backends reuse ids — check before trusting the dedupe.)

---

## The meta-lesson

We measured this skill's premise with the tooling it was meant to govern, and the
premise was wrong — twice. **Verify the number before you build a rule on it,**
especially when the pattern feels obvious.
