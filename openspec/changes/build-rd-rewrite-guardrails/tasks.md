## 1. Bootstrap and policy

- [x] 1.1 Record G0 read-only evidence, confirm Change A and Change B are absent, and verify all planned target paths are initially absent.
- [x] 1.2 Create proposal, delta spec and design that lock the approved CLI, exact write scope, result/exit semantics, fixtures, acceptance, rollback and G1 human gate.
- [x] 1.3 Run pre-implementation OpenSpec strict validation and status; stop if validation is nonzero.
- [x] 1.4 Create the tooling bootstrap manifest, machine policy, project-map registration, planned run-state, approvals structure and truthful current status without advancing G1.

## 2. Baseline and scope TDD

- [x] 2.1 RED: add baseline tests for unchanged/changed sources, G0 dirty content, dry-run zero-write, deterministic hashing and manifest overwrite rejection; run and record expected failures.
- [x] 2.2 GREEN: implement `model.py`, `baseline.py` and the minimum `baseline-create`/`baseline-verify` CLI behavior; rerun focused and regression tests.
- [x] 2.3 RED: add scope tests for exact tooling whitelist, preserved G0 changes, unauthorized writes and protected-source deltas; run and record expected failures.
- [x] 2.4 GREEN: implement `scope.py` and `scope-check --phase tooling`; rerun focused and regression tests.

## 3. Record and draft checks TDD

- [x] 3.1 RED: add inventory, segment and atomic-rule tests for valid records, missing fields, duplicate IDs, invalid lines, line gaps/overlaps and missing rule-bearing references.
- [x] 3.2 GREEN: implement `records.py` inventory, segment and rule checks; rerun focused and regression tests.
- [x] 3.3 RED: add classification and rewrite tests for absent/duplicate primary owner, invalid secondary references, missing targets, per-rule retirement reasons, exact copy blocking and similarity review.
- [x] 3.4 GREEN: implement classification, rewrite and `coverage.py` checks; rerun focused and regression tests.
- [x] 3.5 RED: add principle and draft tests for missing supports, multi-item category coverage, tool-term review, four categories, eleven items, required sections and canonical references.
- [x] 3.6 GREEN: implement `principles.py` and `drafts.py`; rerun focused and regression tests.

## 4. Gate, status and report TDD

- [x] 4.1 RED: add gate tests for ordered transitions, stale/missing evidence, missing G1 approval, illegal jumps, exception safety and interrupted-run recovery.
- [x] 4.2 GREEN: implement `gates.py`, atomic state persistence, `gate` and `status` while keeping the real state at `planned` until user G1 approval.
- [x] 4.3 RED: add report tests for fact traceability, deterministic output, missing inputs, warning/review disclosure and dry-run zero-write.
- [x] 4.4 GREEN: implement `report.py`, `report-build`, `verify-all` and the remaining CLI command surface without forbidden automation commands.

## 5. Fixture and acceptance verification

- [x] 5.1 Build the plan-defined `valid`, `source_changed`, `line_gap`, `duplicate_owner`, `unsupported_principle` and `unauthorized_write` synthetic fixtures with explicit expected results.
- [x] 5.2 Prove every deterministic hard-failure class has a failing counterexample, REVIEW_REQUIRED is distinct from BLOCKED, repeated inputs are deterministic, and interrupted state is recoverable.
- [x] 5.3 Run `python -m unittest discover -s tools -p "test_rd_rebuild_*.py" -v` and record exact counts and exit code.
- [x] 5.4 Run real W0–W9 `baseline-create --dry-run`, tooling `scope-check`, and source hash verification; confirm no protected-source or unauthorized-path delta.
- [x] 5.5 Run `python tools/verify_rd_standards.py .` and `python tools/verify_workflow_index.py .`; record the actual evidence level and any unrelated pre-existing failures.
- [x] 5.6 Run final `openspec validate build-rd-rewrite-guardrails --strict --no-interactive` and `openspec status --change build-rd-rewrite-guardrails`.

## 6. G1 handoff and stop

- [ ] 6.1 Complete producer self-check against proposal, spec, design, tests, diff scope and source protection; do not label Codex self-review as independent review.
- [ ] 6.2 Build the G1 fact report with commands, exit codes, evidence paths, limitations, OpenSpec status, last trustworthy gate and next action.
- [ ] 6.3 Leave G1 approval pending, stop all writes, and request the user's explicit review; do not create or continue `rewrite-rd-standards-content`.

## Execution Evidence

- G0 Git status: 638 entries; aggregate SHA-256 `ea1b402e2464f8d4003821d2f7434a0149dcd3aca4da4d3d945f3e592cd0f5b7`.
- G0 W0–W9 sources: 40 files; aggregate SHA-256 `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`.
- OpenSpec CLI: 1.2.0; no active changes before Change A creation.
- G0 authority: user explicitly approved the sole execution plan and instructed execution to begin.
- Pre-implementation OpenSpec strict validation: exit 0, `Change 'build-rd-rewrite-guardrails' is valid`; status 4/4 artifacts complete.
- Task 1.4 initially stopped when bootstrap verification exited 1. Root cause was inconsistent Windows path separators in the manifest, not a source change; a focused regression test failed before the fix and passed afterward. Reverification returned exit 0 with 0 scope mismatches and the original G0 source digest.

## Resolved Stop Record

- Gate remained G0 / `planned`; no state advancement occurred.
- Root cause: `protected_sources[].path` used Windows `\` separators while the G0 digest contract used repository-relative `/` separators.
- Regression evidence: `python tools/test_rd_rebuild_baseline.py -v` failed on the separator assertion before the fix and passed afterward.
- Recovery evidence: bootstrap verifier exit 0, 639 existing files with 0 mismatches, 40 protected sources matching G0 digest `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`.
- Baseline/scope RED: 8 expected failures because `rd_rebuild_core` was absent; the existing bootstrap regression test remained green.
- Baseline/scope GREEN: 9/9 unit tests passed; real `baseline-verify` and `scope-check --phase tooling` both exited 0 with 40 protected sources and 639 preserved workspace files.
- Records RED: 6 expected failures because `rd_rebuild_core.records` was absent.
- Records GREEN: focused 6/6 and full 15/15 unit tests passed; real baseline and tooling scope checks remained exit 0.
- Classification/rewrite RED: 7 expected failures because classification and coverage APIs were absent; prior record tests remained green.
- Classification/rewrite GREEN: focused 13/13 and full 22/22 unit tests passed; real baseline and tooling scope checks remained exit 0.
- Principle/draft RED: 6 expected failures because principle and draft APIs were absent; all prior record checks remained green.
- Principle/draft GREEN: focused 19/19 and full 28/28 unit tests passed; real baseline and tooling scope checks remained exit 0.
- Gate/report RED: 5 gate and 3 report tests failed as expected because both APIs were absent.
- Gate/report GREEN: focused gate 5/5, report 3/3 and full 36/36 unit tests passed; real baseline and tooling scope checks remained exit 0.
- Final Change A regression: 62/62 unit tests passed; all six named fixture families passed; baseline dry-run, baseline verification and tooling scope verification exited 0; 40 protected sources, 639 preserved workspace files and 638 preserved Git status entries matched.
- Repository verification: `python tools/verify_workflow_index.py .` exited 0. `python tools/verify_rd_standards.py .` exited 1 because the 2026-07-10 review snapshot expected 403 files while the current tree has 441, its review packet is not bound to the current snapshot, and independent review/pilot remain pending. These review artifacts are outside Change A's authorized write scope.
- Final OpenSpec evidence: strict validation exited 0 and status reported 4/4 artifacts complete.

## Current Stop Record

- Stopped after task 5.6 under the plan's nonzero-tool rule; G1 remains pending and `run-state.json` remains `planned` / G0.
- Failure evidence: `governance/rd-standards-rebuild/reports/2026-07-16-repository-verifier-blocked.json`.
- No W0–W9 file, formal entry point, migration artifact or Change B was created or modified.
- Recovery requires explicit user direction because the failing review snapshot and review packet are outside the exact Change A whitelist.

## User Resolution

- On 2026-07-16 the user explicitly directed Codex to continue the overall standards rewrite and not treat the repository-wide legacy verifier as relevant to that goal.
- The exit-1 verifier evidence remains recorded without being relabeled PASS; the user resolution removes it as a G1 blocker for this change only.
- G1 approval is recorded against scope `761119503592150159985ff14f93d21950589af0e1858ab5c4819a73f7b0e962`; Change B may begin only after the real gate command advances `run-state.json` to `tooling_ready`.

## 7. G2 post-freeze tool recovery

- [x] 7.1 Record the G8 OpenSpec launcher failure, the user-authorized fixed recovery scope, the pre-recovery protected aggregate and the distinction between implementation authorization and renewed G1 acceptance; strict-validate Change A before code changes.
- [x] 7.2 RED: add launcher tests for resolved Windows `.CMD`/`.BAT`, direct executables, missing launchers and nonzero strict validation without shell-string execution.
- [x] 7.3 RED: add recovery-scope tests proving an absent, pending, expanded, unapproved or digest-mismatched recovery blocks; prove an exact approved chain passes while the original baseline remains unchanged.
- [x] 7.4 GREEN: minimally implement the cross-platform launcher and append-only recovery validator only in `gates.py` and `scope.py`; rerun focused regressions.
- [x] 7.5 Run the full unit/fixture suite, real source baseline, pre-recovery protected aggregate, standalone and internal OpenSpec strict checks, Change A strict validation/status and all plan-required G1 verification; record exact results without relabeling failures.
- [x] 7.6 Complete producer self-check and obtain a new independent read-only review of the recovery diff, tests, evidence and fixed scope.
- [ ] 7.7 Present the candidate replacement digest and complete evidence to the user, stop writes, and request explicit renewed G1 acceptance; the existing recovery-protocol approval is not acceptance of the candidate.
- [ ] 7.8 Only after renewed user acceptance, append the bound approval and approved recovery manifest, update the tool manifest, verify the recovery chain/content scope/full checks, then resume the previously blocked G8 transition.

## Tool Recovery Authorization Evidence

- G8 dry-run failed without state mutation: `openspec-strict` returned `TOOL_ERROR`; standalone `openspec validate rewrite-rd-standards-content --strict --no-interactive` returned exit 0.
- Root cause: Windows resolves the npm CLI to `openspec.CMD`, while the frozen implementation called unresolved `openspec` through `subprocess.run(..., shell=False)` and received `[WinError 2]`.
- Failure report: `governance/rd-standards-rebuild/reports/2026-07-19-g8-openspec-launcher-tool-error.json`.
- User explicitly approved the fixed tool-recovery protocol on 2026-07-19. Approval event `G1R-2026-07-19-user-approved-tool-recovery-protocol` authorizes implementation/verification only, not renewed G1 acceptance or G8/G9.
- Pre-recovery protection report: `governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-bootstrap.json`; 697 paths with digest `de7409e94875354b1570a3f8ca40b4db34111217b1dd1b97c6896dba99148569`, 696 Git status entries with digest `54f4fc6b3b5878e527553d9a7b41ea00ac403267cb316e9f191f32ef84228a64`, report SHA-256 `d72b427eb1a17a7390abe02b8b7c33b865d0cd1d7140b3a169a27a4a89ec28e6`.
- Recovery specification validation before production-code changes: protected aggregate PASS with the same counts/digests; source baseline PASS for 40 files; `openspec validate build-rd-rewrite-guardrails --strict --no-interactive` exit 0; OpenSpec status 4/4 artifacts complete.
- Launcher RED: the isolated four-test run exited 1 with five expected assertion failures, proving the frozen implementation did not resolve the executable, route `.CMD`/`.BAT` through `COMSPEC`, or distinguish a missing launcher before process start. Earlier sandbox-temp errors were excluded from this evidence.
- Recovery-chain RED: the isolated five-test run exited 1 with five expected failures and no environment errors, proving the frozen content scope did not recognize the fixed recovery contract. A later Git-status symmetry test separately exited 1 with the expected stale baseline entry for `tools/rd_rebuild_core/gates.py`.
- GREEN: launcher focused tests 4/4 PASS; recovery focused tests 7/7 PASS; Git-status symmetry test PASS; full suite 73/73 PASS. Production changes remain limited to `gates.py` and `scope.py`, with their two test files.
- Security-evidence RED/GREEN: four negative subcases first proved that missing producer self-check, a mismatched failure-report digest, an incomplete verification set and an independent review bound to the wrong candidate were incorrectly accepted; after the minimal validator extension the focused test passed and full regression remained green. These fields are now included in the renewed-approval scope digest.
- Candidate tool verification: all original 23 tool paths verify in memory with replacement digest `1a30bddc6dca4ad7f7797189240c43d1db0c35d4447d7153c596e506c50344eb`; exactly `gates.py`, `scope.py`, `test_rd_rebuild_gates.py` and `test_rd_rebuild_scope.py` differ from the frozen tool manifest. The formal manifest remains unchanged pending renewed G1 acceptance.
- Real launcher verification: the recovered internal OpenSpec check resolved and validated `rewrite-rd-standards-content` with exit 0 and PASS; standalone strict validation also exited 0.
- Final recovery verification before review: full suite 73/73 PASS; the six named fixture families plus the status-distinction test 7/7 PASS; source baseline PASS for 40 files at `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`; protected recovery aggregate PASS at 697 paths / 696 Git status entries with both original digests; candidate 23-file tool manifest PASS at `1a30bddc6dca4ad7f7797189240c43d1db0c35d4447d7153c596e506c50344eb`; Change A and Change B strict validation exit 0; both OpenSpec statuses report 4/4; workflow-index verifier exit 0; run state remains `audit_ready` / G7.
- The content-stage `baseline-create --dry-run` and formal `verify-all` are not run before renewed acceptance: at G7 the former would attempt an already-frozen content transition, while the latter is designed to block until the approved recovery record and replacement manifest exist. The original G1 dry-run evidence remains preserved; both acceptance-dependent checks are required by task 7.8 after user approval.
- Six inaccessible empty `tmp*` directories left by the earlier sandbox-denied test attempt were verified as children of the Change A whitelist and removed with elevated filesystem access; they contained no recorded repository file or Git-status entry and do not alter either protected aggregate.
- Superseded producer self-check for candidate `1a30bddc6dca4ad7f7797189240c43d1db0c35d4447d7153c596e506c50344eb`: it was PASS against that candidate but ceased to be current when the independent review required changes. It is historical evidence only and is not independent review.

## Independent Review Remediation

- The first independent read-only review of candidate `1a30bddc6dca4ad7f7797189240c43d1db0c35d4447d7153c596e506c50344eb` returned `CHANGES_REQUIRED` with 1 critical and 4 important findings: full baseline rebinding could bypass recovery; state/gate consistency and post-G8 semantic freeze were incomplete; producer and reviewer identities were not separated; implementation authorization could be reused as acceptance; and `.cmd` paths containing command metacharacters could be split by `cmd.exe`. That candidate and its 73/73/full-verification evidence are historical and superseded, not current acceptance evidence.
- Remediation RED: six isolated reviewer-reproduction tests ran outside the restricted test sandbox and failed for the six expected assertions with no environment errors: baseline rebind returned PASS, state/gate mismatch returned PASS, post-G8 semantic mutation returned PASS, same-identity review returned PASS, reused authorization returned PASS, and an `&` wrapper path was split by `cmd.exe`.
- Remediation GREEN: the same six tests now pass. Additional focused positive/negative runs prove the immutable G2 anchor still accepts an exact recovery, the frozen workspace allows the correct state transition only, distinct review and approval events preserve the positive recovery path, and the launcher passes mock, real `&`-path, direct-executable and missing-launcher cases.
- At that review-remediation point, full verification, replacement digest, producer self-check and a new independent read-only review were pending, so task 7.5 was reopened until evidence could be regenerated against the remediated candidate.

## Remediated Candidate Verification

- Focused compatibility correction: after the first 79-test run exposed one old assertion that expected the established `frozen tool manifest changed` finding, identity validation was changed to accumulate both the new anchor-invalid finding and the original tool-digest finding. The old rebaseline test, the full-rebind blocker and the exact-approved-recovery positive test then passed 3/3.
- Full unit suite: 79/79 PASS. The six original reviewer reproductions all remain green, including a real `.CMD` wrapper under an `&` path.
- Plan fixture suite: 7/7 PASS across the six named fixture families plus the distinct `REVIEW_REQUIRED`/`BLOCKED` status test.
- Source baseline: PASS for 40 files at `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`.
- Recovery protection: the pre-recovery snapshot remains exactly 697 paths / 696 Git status entries at file digest `de7409e94875354b1570a3f8ca40b4db34111217b1dd1b97c6896dba99148569` and Git-status digest `54f4fc6b3b5878e527553d9a7b41ea00ac403267cb316e9f191f32ef84228a64`; the durable snapshot remains exactly 661 / 660 at `38b42a17492dd29c561f71cff4e377e92cb66872fd7b8825ce913b71b2631881` / `4dea982b6996cba6010c72b69b76130a923ef4fbbd4c4ea7785c3bdd8a583436`.
- Post-G8 semantic freeze candidate: 696 paths / 695 Git status entries at file digest `5efc6e52c92386379d865587bde84ffb3081097cb57f26172ae85095e5417e7f` and Git-status digest `f4d20f730385b39d6298848969a525de647a56001533f6d406f72fea37dd4b54`.
- Candidate tool verification: PASS for the original 23 tool paths at replacement digest `02dd47dfd189199e52f901db548a8f6a19c36d6e1588d3d491bc37b7476f51f8`; only `gates.py`, `scope.py` and their two tests differ from the formal frozen manifest, which remains unchanged pending renewed G1 acceptance.
- OpenSpec and repository checks: the recovered internal Change B strict check PASSed; standalone Change A and Change B strict validation exited 0; both statuses remain 4/4; workflow-index exited 0 with 39 optional playbooks and one default OpenSpec entry.
- One in-memory candidate verifier invocation omitted the required `status: verified` field and truthfully returned BLOCKED; it is not counted as passing evidence. The corrected complete manifest object returned PASS with the 23-file candidate digest above.
- Six additional sandbox-created empty test directories under the Change A whitelist were path-verified and removed; no recorded file or Git-status aggregate changed.
- Current producer self-check, recovery-manifest refreeze and a new independent read-only review remain pending. Renewed user G1 acceptance, formal manifest replacement, content scope/verify-all and G8 transition remain acceptance-dependent and have not occurred.

## Second Independent Review Remediation

- Independent reviewer `/root/review_tool_recovery_g1r_v4` completed a read-only review of candidate `02dd47dfd189199e52f901db548a8f6a19c36d6e1588d3d491bc37b7476f51f8` and returned `CHANGES_REQUIRED` with 0 critical, 2 important and 0 minor findings. That verdict is not approval and the candidate is superseded.
- Finding one: recovery validation converted arbitrary JSON reviewer values with `str(...)`, so `null`, objects and arrays were accepted as nonempty identities. Finding two: the live G9 gate path required only `user-review`, so a state/last-gate mismatch or post-G8 semantic drift could advance unless content scope happened to be run separately.
- RED evidence: three isolated test methods exited 1 with eight expected assertion failures and no environment error: six producer/independent non-string identities returned PASS, an `awaiting_user_review/G7` mismatch advanced, and G9 omitted `scope-check`. A preceding sandbox-temp permission failure was excluded from behavioral evidence.
- GREEN evidence: the same three test methods pass after requiring a nonempty string identity, enforcing the state/last-gate pair inside every transition, and adding live content `scope-check` to G9.
- Current full unit suite: 82/82 PASS. Plan fixture suite: 7/7 PASS. Source baseline: PASS for 40 files at `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`.
- Current candidate tool verification: PASS for the original 23 paths at replacement digest `016ae451a8ed2f05531e7cfbb1c6f93a98b8646b78b2f1d03b7772f626baf512`; exactly `gates.py`, `scope.py` and their two test files differ from the formal frozen manifest.
- All three recovery snapshots remain exact: protected 697/696 at `de7409e94875354b1570a3f8ca40b4db34111217b1dd1b97c6896dba99148569` / `54f4fc6b3b5878e527553d9a7b41ea00ac403267cb316e9f191f32ef84228a64`; durable 661/660 at `38b42a17492dd29c561f71cff4e377e92cb66872fd7b8825ce913b71b2631881` / `4dea982b6996cba6010c72b69b76130a923ef4fbbd4c4ea7785c3bdd8a583436`; frozen 696/695 at `5efc6e52c92386379d865587bde84ffb3081097cb57f26172ae85095e5417e7f` / `f4d20f730385b39d6298848969a525de647a56001533f6d406f72fea37dd4b54`.
- Internal and standalone Change B strict validation PASS; final standalone Change A strict validation PASS and status remains 4/4 after the remediation specification update; Change B status is also 4/4 and workflow-index verification PASS. Recovery-manifest refreeze, producer self-check and a fresh independent read-only review remain pending for the current candidate.

## Third Independent Review Remediation

- Independent reviewer `/root/review_tool_recovery_g1r_v5` completed a read-only review of candidate `016ae451a8ed2f05531e7cfbb1c6f93a98b8646b78b2f1d03b7772f626baf512` and returned `CHANGES_REQUIRED` with 0 critical, 2 important and 1 minor finding. All nine focused regressions, 82 unit tests, seven fixture tests, source/OpenSpec/status/workflow checks and before/after repository fingerprints passed; the verdict remained changes-required because static approval-boundary review found three defects.
- Finding one: renewed-G1 `approval_id` was excluded from `RECOVERY_SCOPE_FIELDS`, so the recovery record could rebind the event ID without changing its approved scope digest. Finding two: gate and recovery matchers accepted events missing `decided_at`, `decision_source` or `notes`, and did not reject duplicate IDs or same-scope conflicts. Minor finding: JSON `false` and `0.0` compared equal to integer zero and could masquerade as zero independent-review findings.
- RED evidence: four focused test methods exited 1 with fifteen expected assertion failures and no environment error. Changing only `approval_id` preserved the digest; boolean/float zero passed; six malformed/duplicate/conflicting recovery approvals and the same six human-gate approvals advanced instead of blocking.
- GREEN evidence: the same four methods pass after adding `approval_id` to canonical recovery scope, sharing a fail-closed approval-log validator between gate and recovery paths, requiring all eight plan fields plus a nonempty decision time for the selected event, rejecting duplicate IDs and same gate/scope ambiguity, and requiring `type(count) is int and count == 0`.
- Current full unit suite: 86/86 PASS. The real seven-record approval log has zero base-schema findings and zero duplicate IDs; the historical G0 null decision time remains recordable but cannot authorize a live transition.
- Current candidate verification: PASS for the original 23 tool paths at replacement digest `a0fceaa830ea9a99a9acafae84cfe546be6d58e5a0717eff93e30fcfb2bb5f94`; exactly `gates.py`, `scope.py` and their two test files differ from the formal manifest.
- All recovery snapshots remain exact at the previously recorded protected 697/696, durable 661/660 and frozen 696/695 counts and digests. Fixture, source, OpenSpec, workflow, recovery-manifest refreeze, producer self-check and a new independent review must be regenerated for the current candidate before renewed G1 can be requested.

## Fourth Independent Review Remediation

- Independent reviewer `/root/review_tool_recovery_g1r_v6` completed a read-only review of candidate `a0fceaa830ea9a99a9acafae84cfe546be6d58e5a0717eff93e30fcfb2bb5f94` and returned `CHANGES_REQUIRED` with 0 critical, 1 important and 0 minor finding. The prior ten risk classes were closed; 13 focused tests, 86 unit tests, seven fixtures and all source/OpenSpec/status/workflow/fingerprint checks passed without repository mutation.
- The remaining finding was exit semantics: a human gate mapped a non-object approval line or malformed JSON to `TOOL_ERROR / 3` because `_approvals` raised `ValueError`/`JSONDecodeError`, even though this is deterministic invalid governance data and must be `BLOCKED / 1`. State preservation was already correct.
- RED evidence: the focused test exited 1 with two expected assertion failures, proving both `[]` and malformed `{` returned TOOL_ERROR while preserving run-state bytes.
- GREEN evidence: the same test passes after separating deterministic value/JSON errors from real I/O errors. Invalid approval data now returns BLOCKED with unchanged state; `OSError` remains TOOL_ERROR.
- Current full unit suite: 87/87 PASS. Current candidate verification: PASS for the original 23 paths at replacement digest `2e7f308198a4959cfdea3e12c066fdaa3b386b8cd154c848bb1d4a644b9610f5`; exactly the same four authorized files differ from the formal manifest. Full fixture/source/OpenSpec/workflow verification, report refreeze, producer self-check and a fresh independent zero-finding review remain required before renewed G1.

## Final Independent Tool-Recovery Review

- Independent reviewer `/root/review_tool_recovery_g1r_v8`, identity `Codex independent reviewer /root/review_tool_recovery_g1r_v8`, completed a read-only review of candidate `2e7f308198a4959cfdea3e12c066fdaa3b386b8cd154c848bb1d4a644b9610f5` and returned `APPROVED` with 0 critical, 0 important and 0 minor findings. The reviewer is distinct from `Codex producer` and made no repository mutation.
- The review independently recomputed the formal/candidate manifests, exact four changed tools, 40-source digest, all three recovery snapshots, ten frozen changed-file hashes, seven-event approval schema/uniqueness, run-state and pending recovery status. All values matched the recovery report and fixed anchors.
- Independent runtime evidence: 20/20 focused regressions, 87/87 full unit tests and 7/7 fixture tests PASS; source baseline, internal Change B strict validation, standalone Change A/B strict validation, both 4/4 statuses and workflow-index PASS. Invalid/non-object approval JSON returns BLOCKED with unchanged state; injected approval I/O failure returns TOOL_ERROR with unchanged state.
- The reviewer confirmed closure of every prior finding: baseline rebinding, state/gate pairing, post-G8 freeze, reviewer types and independence, implementation/acceptance event separation, Windows metacharacter-safe launching, G9 live scope, renewed approval ID scope binding, complete/unambiguous approvals, exact integer-zero finding counts and deterministic approval-data exit semantics.
- This approval covers only the fixed tool-recovery candidate and evidence. It is not user renewed-G1 acceptance, does not authorize formal manifest replacement, and does not authorize G8/G9 or migration.
