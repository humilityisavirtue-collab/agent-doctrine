"""
The shortest honest demonstration of why a green test can mean nothing.

    python vacuous_gate.py            # run the demo
    python vacuous_gate.py --mutants  # prove the fixed gate can actually die

No dependencies. Python 3.8+. Runs anywhere, offline, in about a second.

THE PROBLEM
-----------
An agent says "I added a safety check, tests pass." The tests do pass. The
check is real code, it runs, it returns True. And it has never once been
capable of returning False.

This is not a hypothetical. It is the single most common way a verification
step lies, because every surface signal is correct: the code exists, the test
is green, the author is honest and believes it works.

The only thing that catches it is asking a question the test cannot ask about
itself: **could this have failed?**
"""

import sys

# --------------------------------------------------------------------------
# The subject under test: a filter that is supposed to reject low-confidence
# predictions before they reach a user.
# --------------------------------------------------------------------------

def classify(text):
    """A toy classifier. Note the confidence values it can actually emit."""
    words = text.lower().split()
    hits = sum(1 for w in words if w in {"urgent", "now", "help", "asap"})
    if not words:
        return {"label": "unknown", "confidence": 0.0}
    # Real systems quantize more than their docs admit. This one emits only
    # multiples of 0.25 -- never anything between, and never below 0.0.
    # That floor is the whole story; see gate_vacuous.
    conf = round(hits / len(words) * 4) / 4
    return {"label": "urgent" if hits else "routine", "confidence": conf}


# --------------------------------------------------------------------------
# THE VACUOUS GATE -- this is the bug, and it looks completely fine
# --------------------------------------------------------------------------

def gate_vacuous(result):
    """Reject predictions below the confidence floor.

    Looks like a safety mechanism. Is not one. See below.
    """
    THRESHOLD = 0.0
    return result["confidence"] >= THRESHOLD


# --------------------------------------------------------------------------
# THE FIXED GATE
# --------------------------------------------------------------------------

def gate_real(result):
    """Same shape, but the threshold sits INSIDE the range the source emits."""
    THRESHOLD = 0.5
    return result["confidence"] >= THRESHOLD


# --------------------------------------------------------------------------
# The check that catches it. This is the whole point of the file.
# --------------------------------------------------------------------------

CORPUS = [
    "urgent help needed now",
    "can you help me",
    "asap",
    "please send the quarterly report when convenient",
    "",
    "is this urgent or can it wait",
    "the meeting is scheduled for tuesday afternoon",
]


def probe(gate, corpus=CORPUS):
    """Return (passed, rejected) counts AND the emitted confidence range.

    Printing the range is not decoration. A gate whose threshold sits at or
    below the minimum its source can emit never rejects anything -- and you
    cannot see that from the pass count alone, because a pass count of N/N
    is exactly what a working gate looks like on clean input.
    """
    confs = [classify(t)["confidence"] for t in corpus]
    verdicts = [gate({"confidence": c}) for c in confs]
    return {
        "n": len(corpus),
        "passed": sum(verdicts),
        "rejected": len(verdicts) - sum(verdicts),
        "conf_min": min(confs),
        "conf_max": max(confs),
        "distinct_conf": sorted(set(confs)),
    }


def can_this_gate_ever_fail(gate):
    """The question a test cannot ask about itself.

    We do not ask 'did it pass?'. We ask whether ANY input the source is
    capable of producing would make it say no.
    """
    reachable = sorted({classify(t)["confidence"] for t in CORPUS})
    return any(not gate({"confidence": c}) for c in reachable)


def main():
    print("=" * 68)
    print("BOTH GATES PASS THEIR TESTS. ONE OF THEM IS DECORATION.")
    print("=" * 68)

    for name, gate in (("gate_vacuous", gate_vacuous), ("gate_real", gate_real)):
        r = probe(gate)
        alive = can_this_gate_ever_fail(gate)
        print(f"\n{name}")
        print(f"    n={r['n']}  passed={r['passed']}  rejected={r['rejected']}")
        print(f"    confidence values the source can emit: {r['distinct_conf']}")
        print(f"    CAN THIS GATE EVER RETURN FALSE?  {'YES' if alive else 'NO -- IT IS VACUOUS'}")

    print("\n" + "-" * 68)
    print("""
Read the pass counts alone and gate_vacuous looks like the better gate --
it rejected nothing, so nothing was wrongly blocked. That reading is exactly
backwards, and no amount of staring at the green will reveal it.

The tell is not in the output. It is in the relationship between the
threshold and the range the SOURCE can produce. gate_vacuous's threshold of
0.0 sits at or below the floor of a function that cannot emit a negative
number, so its comparison is a tautology wearing a safety mechanism's clothes.

  RULE: check the source's floor, not the filter's presence.

This is why every gate in a system worth trusting ships with a negative
control -- a case that MUST make it fail. If you cannot construct one, you
have not written a check. You have written a comment that costs CPU.
""".strip())
    return 0


# --------------------------------------------------------------------------
# MUTATION TESTING -- a negative control for the negative control
# --------------------------------------------------------------------------

MUTANTS = [
    ("threshold to 0.0  (the original bug)", lambda r: r["confidence"] >= 0.0),
    ("always true       (check deleted)",     lambda r: True),
    ("threshold below floor (-1)",            lambda r: r["confidence"] >= -1),
]


def mutants():
    """Prove `can_this_gate_ever_fail` actually detects vacuity.

    A checker that never catches anything is the same defect one layer up --
    so the checker needs its own control. Every mutant here is a gate that
    SHOULD be flagged vacuous. A surviving mutant is a hole in the checker.
    """
    print("=" * 68)
    print("MUTATION TEST -- does the vacuity checker actually have teeth?")
    print("=" * 68)
    print(f"\n  BASELINE  gate_real flagged vacuous? "
          f"{'yes -- BUG' if not can_this_gate_ever_fail(gate_real) else 'no (correct)'}")
    survivors = []
    for name, mutant in MUTANTS:
        caught = not can_this_gate_ever_fail(mutant)
        print(f"  [{'CAUGHT ' if caught else 'SURVIVED'}] {name}")
        if not caught:
            survivors.append(name)
    print()
    if survivors:
        print(f"  {len(survivors)} SURVIVOR(S) -- the checker has a blind spot:")
        for s in survivors:
            print(f"     {s}")
        return 1
    print(f"  {len(MUTANTS)} mutants, 0 survivors -- the checker can catch what it claims to.")
    print("  Note this proves the checker has TEETH. It does not prove the")
    print("  teeth are pointed at the right population -- see LAWS.md, law 3.")
    return 0


if __name__ == "__main__":
    sys.exit(mutants() if "--mutants" in sys.argv else main())
