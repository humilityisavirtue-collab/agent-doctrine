---
name: turn
description: "Run one task as four phases in sequence — READ the premise, BUILD, RUN the check, REPORT with coverage — where every phase hands the next an artifact, never a claim. Use for any multi-step task where a confident wrong answer costs more than a slow right one: debugging, migrations, gates. Usage - /turn <task>"
---

# /turn — Four Phases, One Turn

One agent, one task, four phases. It borrows the separation of a multi-agent review
setup and collapses it into a single context — **under one condition, stated in the
law below.** A /turn that ignores the law was measured at zero.

---

## THE LAW — this is the whole skill; the phases are scaffolding

Measured across 9 consecutive defects in a multi-agent setup:

| self-review of… | caught the defect? | why |
|---|---|---|
| your own **prose / summary** | **0 of 9** | you re-read what you *meant*, not what you wrote |
| your own **raw rows** (files, output, data) | **2 of 2** | rows have no memory of your intention |

> **The thing that works is the ACT of opening the artifact — not having a second
> reviewer.** "Get a second reader" is satisfied by someone skimming your summary,
> and that failed every time.

**So every phase boundary hands over an ARTIFACT, never a claim.** A phase that reads
the previous phase's *description* of its work has done nothing. A phase that opens
the file, runs the command, or reads the rows is doing the job.

If you catch yourself writing *"as established above,"* stop — go re-open the thing
that was actually read.

---

## THE FOUR PHASES

### 1. READ — restate, then inspect the premise
Restate the task in your own words *first*, so a misread surfaces before it costs
anything. Then **open the structure you're about to reason over**: the schema, the
config, the tensor shape, the actual file. Don't reason from a premise you haven't
looked at in this session.

- **Output:** the restated task + the literal thing you read, with `file:line`.
- **Fails when:** you derive consequences from a shape you imagined. *(Four rounds of
  correct algebra once died on an unread `w_k.shape`.)*
- **Cheap win:** does this already exist? `ls` before you build.

### 2. BUILD — make the change
Smallest thing that could work. On a shared tree, touch explicit paths only.

- **Output:** the diff, the file, the command actually run.
- **Fails when:** you build against the READ phase's *summary* instead of what it read.
- If the READ phase turns out wrong, go back. A correct fix on the wrong premise lands
  on the wrong thing.

### 3. RUN — execute it; don't re-read it
Paste the raw output and the exit code. A green on belief is not a green.

- **Output:** command + literal output + exit code. Never "looks right."
- **Fails when:** it turns into re-reading the BUILD phase's work — the 0-of-9 case.
- **Anti-vacuous:** what would this check do if the thing were BROKEN? If you can't
  name the input that turns it red, it isn't a check. Prefer a second instrument that
  fails *differently* — and then name the axis the two instruments **share**, because
  two checks can be independent on the axis you picked and identical on the one you
  never named.
- Don't pipe: `cmd | tail` masks the exit code. Run bare, or `; echo "EXIT=$?"`.

### 4. REPORT — tell the human
Lead with the verdict. Then the evidence. Then the coverage line.

- **Output:** verdict → evidence → **what you did NOT check**.
- **Fails when:** an unqualified "done / clean / verified" implies coverage that a
  sampled check never had.
- **Never** report a result you haven't read. If the run failed, say so, with output.

---

## WHAT THIS BUYS, AND WHAT IT DOESN'T

**Buys:** four contacts with something external in one turn, where the default is
one. Most agent failure isn't bad reasoning — it's *correct reasoning over an unread
premise*, and a phase whose whole job is reading kills that class before it starts.

**Doesn't buy:** immunity. One agent running four phases still has one summary in its
head. A true non-author is more reliable exactly because they have no summary to read
the rows *through* — so **a real second reviewer stays the default for anything
load-bearing.** /turn raises the floor of a solo turn; it doesn't reach the ceiling
of a second pair of eyes.

**The phase most likely to rot is RUN,** because "I just wrote this, it's fine" is
most tempting there and cheapest to act on. If you skip exactly one phase, it'll be
that one — and it's the one carrying the measurement.

---

## FALSIFIER

If a /turn produces a RUN phase whose output couldn't have differed had the build been
broken, the structure did nothing that turn. Log it as a miss, not a pass.

**Retire this skill when** tooling refuses any REPORT that has no RUN output attached
— then the habit is no longer load-bearing.
