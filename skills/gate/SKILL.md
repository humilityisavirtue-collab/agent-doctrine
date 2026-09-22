---
name: gate
description: "Run-don't-read test gate. Before anyone writes 'X works', make the machine prove it: find the test surface, run it for real, check the negative control could actually fail, and report GREEN / RED / AMBER with the evidence attached. Usage - /gate <file or claim>"
---

# /gate — Run, Don't Read

Someone (another agent, a teammate, you ten minutes ago) **claims** something works.
This skill makes the machine **prove** it, and reports a verdict that carries the
evidence — never the belief.

---

## The loop (always the same five steps)

1. **Find the test surface.** In priority order: an explicit `--selftest` / `--test`
   flag → an `if __name__ == "__main__"` block → a sibling `test_*.py` / `*_test.py` →
   a callable the file exposes that you drive directly. If there is NO surface, that
   is itself the finding: *"no runnable check — can't gate, only read."* Say so. Don't
   fake a pass.
2. **Classify before you run.** Pure / deterministic code → run first, read later.
   Anything that loads weights, writes files, or touches a network or GPU → **read the
   entry point first** so you know what it will touch, then run.
3. **RUN IT. Real execution, real output.** Capture the exit code and the actual
   stdout/stderr. Don't pipe through `| tail` — that makes `$?` the pipe's, and a dead
   check prints `exit=0`. Run bare, or append `; echo "EXIT=$?"`.
4. **Check the negative control mirrors real failure.** A selftest that only asserts
   "output is non-empty" passes on an *error string*. Ask: **would this check turn RED
   if the thing it guards were actually broken?** If you can't name the input that
   turns it red, the green is vacuous — that's AMBER, not a pass.
5. **Report with the evidence embedded.** The verdict carries the run that earned it:
   exit code, counts (`17/17`), timings, and for RED/AMBER the `file:line` plus the
   failing line of output. **Never report a result you haven't read back from the run.**

## The verdict vocabulary

| Verdict | Means | Carries |
|---------|-------|---------|
| **GREEN** | ran clean, the control is sound, output matches the claim | exit=0, the counts, one line of proof |
| **RED** | ran and failed, or the claim is false | the failing assertion + `file:line` |
| **AMBER** | ran green, BUT the check is weak / a real failure could hide under it / a path wasn't exercised | exactly what the green does NOT cover |

**AMBER is the valuable one.** It's a green that a run could still falsify. The
canonical case: a crash-log analyzer whose selftest was 4/4 GREEN while the analyzer
was dead on the exact crash it existed for — because check #4 only tested that the
output was non-empty, and the error message was non-empty.

## The laws in one breath

1. **Run, don't read.**
2. **Read, then run** — for anything that loads, writes, or reaches the network.
3. **The negative control must mirror real failure.**
4. **No green on belief.**
5. **Run → read → report.** A message carrying numbers depends on the run that makes
   them. Never send them in the same breath as the command.
6. **Confirm once; don't fan out verification.** One read confirms one action. A
   12-way parallel "did it land?" turns one typo into a wall of red.
7. **The verifier lives outside the thing it checks.** A check that imports the code
   under test can inherit its bug.
8. **The oracle stays blind to the generator.** If the same process writes the answer
   and the answer key, you are grading the generator against itself.

## Reporting

- One line: `GREEN|RED|AMBER <target> — <evidence>`.
- **On RED:** name the exact seam (`file:line` + failing output). Don't silently patch
  someone else's code inside a gate — the gate's job is the verdict.
- **On AMBER:** report "the check is weak" separately from "the code is broken." They
  are different fixes, often for different people.
- **Supersede stale claims explicitly.** If an earlier GREEN is now falsified, say so
  and point at the run that overturned it.

## When to invoke

Any time you're about to write *"<thing> works."* Before ratifying a transform,
pipeline, or gate as correct — and for the population-level version of this, use
`/verify-battery`. `/gate` is the single-artifact smoke test; `/verify-battery` is
the proof.

**If there's no run, there's no gate — only a read.**
