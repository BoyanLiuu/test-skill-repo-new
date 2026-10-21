# Release notes style guide

## Audience

Write for someone who uses the project, not someone who works on it. Say what changed for them, not how it was built.

| Instead of | Write |
|---|---|
| Refactor sync task to carry previousStatus | A record returns to its last good status after a failed sync is retried |
| Bump jackson to 2.18 | (omit, unless it fixes something users saw) |
| Add PendingAuthRecordCount metric | Operators can now see how many records are waiting for authorization |

## Rules

1. **Breaking changes first**, each with the action the user must take.
2. **One line per change**, starting with a capital letter, ending without a period.
3. **Present tense, active voice**: "Adds", "Fixes", or a plain statement of the new behaviour.
4. **No internal detail**: no ticket numbers, commit hashes, author names, class names or file paths.
5. **Group, don't repeat**: several commits for one change become one line.
6. **Omit** chores, test-only changes, CI changes and dependency bumps with no user-visible effect.

## Heading

`## v<version> (<YYYY-MM-DD>)`, using the release date, not the date of the last commit.
