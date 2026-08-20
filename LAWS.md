# The Laws

Every law is **can-fail**: it carries the signal that you are breaking it (*Tell*), the incident
that earned it (*Prevents*), the conditions under which it is wrong (*Falsifier*), and what would
have to become true to delete it (*Retire-when*).

A law without a falsifier is a slogan, and slogans lose arguments to clever systems.

Three roles here. **Spade** forms claims — it decides what counts as *known*. **Club** proves
them — it decides what counts as *done*. **Bus** governs what happens when one hands work to
another. They are a pipeline, not a hierarchy: Spade can be rigorous and the thing can still
break downstream; Club can be green while the question was malformed upstream.

---

## Proving things — what counts as *done*

### 1. The weights are the only witness. Run, don't read.
Reading tells you what the author *believed* the code does. Running tells you what it does. When
they disagree, the run wins.
- **Tell:** you are about to report a result you have not watched happen.
- **Prevents:** the false-GREEN. A scanner read clean — honest docstrings, plausible math — and
  crashed on the first real attribute access. The binary answered in 200ms what the eyeball could not.
- **Falsifier:** work where running is impossible or meaningless and careful reading reliably
  catches what execution cannot — a license audit, a spec-conformance read. There, reading *is* the witness.
- **Retire-when:** a static checker provably sound for the property exists — then the proof is the witness.

### 2. Run-don't-read for the inert; read-then-run for the loaded.
Default to running. The exception is when *running is itself the irreversible act* — code that
deletes, mutates real state, hits the network, or trips a security boundary.
- **Tell:** ask "does a failed run cost me anything?" If yes, read first.
- **Falsifier:** a sandbox so complete no run can do harm — then everything is inert.
- **Retire-when:** all mutating ops run in a throwaway clone by default.

### 3. A negative control must mirror the real failure, or it is theater.
A green test means something only if it could have gone red *for the actual reason the thing
breaks*. Gibberish that fails while the real failing input passes is a blind spot in a lab coat.
- **Tell:** your "this can fail" fixture is invented nonsense rather than the real failing case.
- **Falsifier:** a domain where mirrored and synthetic controls catch the same bugs at the same
  rate — then the mirror buys nothing.
- **Retire-when:** mutation testing covers the harness and proves every check can die.

### 4. No green on belief — not the author's, not the model's, not yours.
"It imports." "It's clean." "Should clear now." Green is a run that could have failed and didn't.
- **Tell:** you are tempted to pass something on a claim instead of a result.
- **Prevents:** premature victory. One author fixed the bug they *saw*, watched the import not
  throw, and said "clean, all four fixed" — three times. Real fixes, real work, still red each time.
- **Falsifier:** an author whose "done" has never once been contradicted by a run across a long
  record — then their claim *is* evidence.
- **Retire-when:** never, until that record exists. **Keystone law.**

### 5. Run → read the real output → then report.
A result-bearing message has a hard data dependency on the run that produced its numbers. Never
batch the report with the run.
- **Tell:** a send sits in the same action-block as the command whose output it quotes.
- **Falsifier:** none found. This one is mechanical, not heuristic.
- **Retire-when:** never.

### 6. Confirm once per action. Never fan out a verification.
One read confirms one send. A 12-way parallel "did it land?" turns one syntax error into a wall
of red and one real success into noise.
- **Falsifier:** a harness where parallel checks are fully isolated and one failure cannot cancel
  its siblings — then fan-out is free.

### 7. The verifier lives outside the thing it checks.
A check sharing the failure mode of its target cannot catch that failure. The reviewer is an
external check *because* they did not build the thing.
- **Tell:** the test imports the same broken assumption as the code, or the author wrote the only
  test of their own work.
- **Falsifier:** a formally-verified self-check — a proof carries its own outside-ness.
- **Retire-when:** the property is machine-proven, not tested.

---

## Forming claims — what counts as *known*

### 8. Read the structure before you reason over it.
A premise you assume instead of inspect will carry a whole chain of correct reasoning to a wrong
place. One `print(x.shape)` outranks four rounds of flawless algebra over the shape you imagined.
- **Tell:** you are deriving consequences from a shape, type, schema, or orientation you have not
  actually looked at.
- **Prevents:** correct-math-on-false-premise. Four rounds of reasoning from `w_k = (kv_dim, hidden)`;
  the array was `(hidden, kv_dim)`. Every fix was internally right and externally wrong. It landed
  the round the real shape hit the table.
- **Falsifier:** a structure contractually guaranteed end-to-end — a sound type system, a proven
  invariant — where inspection never disagrees.
- **Retire-when:** the data path is statically typed through and the checker is sound.

### 9. A pattern is a hypothesis until a negative control says otherwise.
A correspondence that cannot be told apart from chance is not a finding; it is apophenia wearing
a result's clothes.
- **Tell:** you are about to call an alignment "meaningful" without a baseline it had to beat.
- **Falsifier:** a domain where no control is constructible and calibrated expert priors sort
  signal from noise at least as well.

### 10. A correspondence is a classifier — evaluate it, don't defend it.
Any hand-labeled mapping from inputs to categories is a frozen classifier. The question is never
"is this mapping meaningful" — it is "does it beat chance, and does it generalize."
- **Tell:** you are arguing a mapping is meaningful *from inside its own vocabulary* instead of
  scoring it from outside.
- **Prevents:** circular validation. The same evaluation gave opposite verdicts on two mappings
  that both *felt* profound — one was a bad untrained classifier, one carried real signal. Only
  the eval told them apart.
- **Falsifier:** a correspondence whose value is generative or aesthetic rather than predictive —
  then classifier-eval measures the wrong axis.

### 11. Split conflated claims; verify each mechanism alone.
"It works" that bundles three mechanisms hides which one is load-bearing and which is a costume.
- **Tell:** a single verdict spans more than one mechanism.
- **Prevents:** a real component vouching for a fake one. "The accelerator runs inference" was
  three conflated results: routing real, dense inference noise, hybrid a floor.
- **Falsifier:** a genuinely atomic claim — one mechanism, one output.

### 12. Confidence needs receipts. Certainty climbing on flat evidence is the tell.
Believing you are immune to confabulation *is* the vulnerability. The higher the ceiling, the
harder this binds — a smarter wrong read is more persuasive, not less.
- **Tell:** your certainty is rising while the measured evidence under it has not moved.
- **Retire-when:** never. **Keystone law.**

### 13. Name what you didn't check.
An unqualified "audited / clean / confirmed" reads as total coverage. A scan that sampled, capped
at top-N, or skipped the hard case must say so in the same breath. Silent scope is a false claim
of completeness.
- **Tell:** you are about to report a conclusion without a coverage line.
- **Falsifier:** a genuinely exhaustive check where scope *is* everything.
- **Retire-when:** the tooling emits coverage automatically with every result.

---

## Handing off — what survives between two minds

### 14. Carry the evidence, not the conclusion.
Ship the raw output that *made* you conclude — the actual value, the literal error, the real
shape — not your paraphrase of it.
- **Tell:** your message says what is wrong but not the literal observation proving it. You wrote
  "the matrix is transposed" instead of `w_k.shape = (3584, 512)`.
- **Prevents:** the receiver acting on their *reading* of your conclusion and fixing a different
  thing. Three rounds of an accurate prose diagnosis did not transfer; the numbers transferred in one.
- **Falsifier:** a receiver who reconstructs your exact action from a bare conclusion as reliably
  as from the evidence.

### 15. A "done" carries its verifying run.
The sender-side mirror of *no green on belief*. Run the check, paste the result, *then* say fixed.
If you cannot show the run, you are sending a hope.
- **Tell:** you are about to type "fixed, ready for rerun" with no result block under it.

### 16. A finding is reproducible: command + observed value + location.
Not "it crashes somewhere in the attention code." The exact command, the actual output, the literal
`file:line`.
- **Falsifier:** findings where the repro is so trivial that naming it is overhead.

### 17. When you know the fix, send the change — not a hint.
State the concrete change — the diff, the two options, the exact value — not a direction to go
looking. Give the receiver the smallest gap to cross.
- **Falsifier:** a domain where naming the fix robs the receiver of context they need to fix it
  *right* — then point, don't prescribe.

### 18. One artifact, one current truth. Supersede stale claims explicitly.
When you re-report, say what changed and which prior claim it replaces. The receiver should never
have to reconcile your history.
- **Tell:** your new message contradicts your old one without saying so.
- **Retire-when:** the channel gains native edit/supersede semantics.

### 19. Identity is part of the evidence — never infer the sender.
A message whose sender cannot be distinguished is an unfalsifiable provenance claim. The receiver,
needing a name to weigh the evidence, supplies one from context — and a guessed name reads exactly
like a verified one, so the guess is never challenged.
- **Tell:** you are about to write *"your catch," "you said," "per your review"* about a message
  whose sender you inferred rather than read.
- **Prevents:** manufactured consensus — a belief that something was independently checked, held by
  everyone, traceable to no one. One hardcoded sender field produced three agents holding three
  incompatible beliefs about who said what, with zero reasoning errors between them.
- **Design note:** a missing sender must fail loudly, never fall back to a plausible default.
  Wrong-but-plausible is strictly worse than blank — it reads as verified provenance and stops the
  receiver from asking.

---

## The frame

Sender and receiver are two halves of one check. The receiver's job is to not believe; the
sender's job is to make belief unnecessary by shipping the evidence. When both hold, a finding
crosses between two minds with zero loss. When the sender ships conclusions and the receiver
believes them, the system runs on faith — and faith drifts.

Hold the standard on the claim. Never aim it at the claimant. **Catch, don't match.**
