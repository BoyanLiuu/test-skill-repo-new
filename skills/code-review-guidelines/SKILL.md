---
name: code-review-guidelines
description: Review a diff against this project's code review checklist. Use when the user asks for a code review, asks whether a change is ready to merge, or asks what to look for in a diff.
---

# Code Review Guidelines

Apply this checklist to the diff under review. Report findings grouped by severity.

## Getting the diff

```bash
git diff                # uncommitted work
git diff main...HEAD    # whole branch
git show <sha>          # a single commit
```

Review only changed lines plus enough surrounding code to judge them.

## Severity levels

| Level | Meaning | Blocks merge? |
|-------|---------|---------------|
| **blocker** | Correctness bug, data loss, security hole, breaking API change | Yes |
| **warning** | Missing test, unhandled error path, unclear naming, duplication | No |
| **nit** | Style, formatting, wording | No |

Only blockers fail a review. Don't pad a review with nits.

## Checklist

**Correctness**
- Off-by-one, null/undefined, empty-collection, and boundary cases
- Error paths: are failures handled or deliberately propagated?
- Concurrency: shared mutable state, missing await, race conditions
- Does the change actually do what the commit message / description claims?

**Security**
- No secrets, keys, or tokens in code, config, logs, or tests
- Input from users or other services is validated before use
- No string-built SQL, shell commands, or file paths from user input
- Permissions and auth checks are not widened without reason

**Tests**
- New behavior has a test; fixed bugs have a regression test
- Tests assert behavior, not implementation details
- No tests disabled, skipped, or weakened without justification

**Design**
- Fits existing patterns in the codebase — no parallel way of doing the same thing
- No dead code, leftover debug output, or commented-out blocks
- Public interfaces stay backward compatible, or the break is called out

**Readability**
- Names say what the thing is; comments explain *why*, not *what*
- Comment density and idiom match the surrounding file

## Output format

For each finding:

```
[blocker] path/to/file.py:42
Concurrent writers can both pass the existence check before either inserts,
so the second insert raises IntegrityError instead of being treated as a no-op.
Fix: use an upsert, or catch IntegrityError and treat it as success.
```

End with a one-line verdict: `PASS` (no blockers) or `FAIL` (blockers listed above).
