---
name: test-ritual
description: A stack-agnostic process for writing proper tests for a feature after it has been built. Discovers the project's existing test setup and conventions, decides what actually needs testing (behavior, edge cases, error paths), writes tests that match the codebase, runs them, and reports coverage honestly. Use when a feature or change has landed and needs test coverage, or when the user says "write tests", "test this", "add coverage", or "test the new feature".
---

# test-ritual: proper tests for a feature that already exists

## Overview

The **test-ritual** is for the moment a feature has been built and now needs real test coverage. It is deliberately stack-agnostic: instead of assuming a framework, it starts by reading the project to learn how this codebase tests things, then writes tests that fit in as if a regular contributor wrote them. The output is tests that catch real regressions, match local conventions, and actually run green.

The bar is not "some tests exist". The bar is: if someone breaks this feature later, one of these tests fails and tells them what broke.

## When to trigger this skill

Run the ritual when:

- A feature or change has landed (possibly built by someone else) and needs coverage
- The user says "write tests", "test this", "add coverage", "test the new feature"
- You are about to wrap up work and the new code has no tests yet

If you are testing code you just wrote yourself, this still applies. Adversarial distance helps: test the behavior the feature promises, not the implementation you happen to remember writing.

## Phase 1: Discover the test setup

Never guess the framework. Find it. Before writing a single test, learn:

1. **What framework and runner does this project use?** Check the manifest and config: `package.json` (scripts, devDependencies), `pyproject.toml` / `setup.cfg` / `tox.ini`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `*.csproj`, a `Makefile`, or CI config under `.github/workflows`. The "test" script and the CI job usually name the exact command.
2. **Where do tests live and how are they named?** Look for existing test files (`test/`, `tests/`, `__tests__/`, `*_test.go`, `*.spec.ts`, `test_*.py`, `*Test.java`). Match the directory and naming convention exactly.
3. **How are tests actually run?** Find the real command (`npm test`, `pytest`, `go test ./...`, `cargo test`, `bundle exec rspec`, `dotnet test`, or a `make test` target). You will use this to verify your work.
4. **What patterns does this codebase already use?** Open two or three existing test files and read them. Note the assertion style, how they set up and tear down, how they mock or fake dependencies, how they name test cases, and whether they use fixtures, factories, or helpers. Your tests should look like these.

If the project has **no tests at all**, say so explicitly, then choose the standard framework for the stack (the one the ecosystem defaults to), set up the minimum config, and note in your report that you introduced the test harness.

## Phase 2: Decide what to test

Read the feature and its contract before writing anything. For the new behavior, enumerate:

- **The happy path.** The main thing the feature is supposed to do, with realistic inputs, asserting the real observable outcome.
- **Edge cases and boundaries.** Empty inputs, zero, one, and many. Maximum and minimum values. Off-by-one boundaries. Unicode or unusual strings where relevant.
- **Error paths.** Invalid input, missing permissions, not-found, timeouts, and failures of dependencies. Assert that the feature fails the way it promises to (right error, right status, no silent success, no corrupt state).
- **State and side effects.** If the feature writes to a database, emits an event, sends a request, or mutates shared state, assert that the side effect happened (and did not happen on the error paths).
- **Regressions.** If this feature fixes a bug, write the test that would have caught the original bug.

Test **behavior and the public contract**, not private implementation details. A good test survives a refactor that preserves behavior. If your test breaks every time someone renames an internal helper, it is testing the wrong thing.

Prefer a few clear, well-named tests over a large brittle suite. One assertion-focused test per behavior beats one giant test that checks everything and fails uninformatively.

## Phase 3: Write the tests

- **Match the local style** discovered in Phase 1: same directory, same naming, same assertion and setup patterns.
- **Name each test for the behavior it checks.** A reader should understand what broke from the failing test name alone. `returns 404 when the invite has expired` beats `test invite 3`.
- **Arrange, act, assert.** Keep setup, the call under test, and the assertions visually distinct.
- **Make each test independent.** No ordering dependencies, no shared mutable state leaking between tests. Each sets up and cleans up what it needs.
- **Isolate real external dependencies** (network, clock, filesystem, third-party APIs) using whatever mechanism the codebase already uses. Do not hit the network in a unit test. If the feature genuinely needs an integration test, write it as one and mark it the way the project marks integration tests.
- **Assert the meaningful outcome,** not an incidental detail. Avoid snapshot-only tests that assert a blob without checking the thing that actually matters.

## Phase 4: Run and verify

Writing tests that were never executed is not done. Run them:

1. Run the exact command from Phase 1. Confirm your new tests are **collected and executed** (a test that silently does not run is worse than no test).
2. Make them pass. If a test fails, decide honestly: is it a bad test, or did it find a real bug? If it found a real bug, surface it rather than weakening the test to go green.
3. **Sanity-check that the tests can fail.** A test that passes no matter what is worthless. If unsure, briefly break the feature (or the expected value) and confirm the test goes red, then restore it.
4. Check coverage of **the new code specifically** if the project has a coverage tool. Aim to cover the branches you enumerated in Phase 2, not a vanity percentage of the whole repo.

## Phase 5: Report

Tell the user, concisely:

- **What you tested:** the behaviors covered (happy path, which edge cases, which error paths).
- **How to run them:** the exact command.
- **Results:** they pass (with the count), or what is failing and why.
- **What you deliberately did not cover,** and why. Silent gaps read as "fully tested" when they are not. If a path needs an integration environment you did not have, say so.
- **Anything the tests revealed:** a real bug, an ambiguous contract, a missing spec.

## What not to do

- Do not test the framework or the language. Assume `Array.push` works.
- Do not write tests you never ran.
- Do not assert on private internals that a safe refactor would change.
- Do not write one enormous test that fails uninformatively.
- Do not skip the error paths because they are tedious. They are where the bugs live.
- Do not weaken or delete a test to make the suite green when the test found a real problem.
- Do not claim coverage you did not verify.

## Checklist

- [ ] Found the framework, test location, naming convention, and run command
- [ ] Read existing tests and matched their style
- [ ] Enumerated happy path, edge cases, error paths, and side effects
- [ ] Wrote independent, behavior-focused, well-named tests
- [ ] Isolated external dependencies the way the codebase does
- [ ] Ran the suite; new tests are collected and pass
- [ ] Confirmed the tests can actually fail
- [ ] Checked coverage of the new code
- [ ] Reported what is covered, how to run it, and any gaps or findings

## Summary

The test-ritual turns "a feature was built" into "a feature is protected". Learn how the project tests, cover the behavior and its edges and its failures, match the local style, run it for real, and report honestly, including what you left uncovered.
