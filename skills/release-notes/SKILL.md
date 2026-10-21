---
name: release-notes
description: Drafts release notes for a Git repository from the commits between two refs, grouped into features, fixes and other changes, in the project's house style. Use when the user asks for release notes, a changelog entry, "what changed since <tag>", or a summary of a version's changes.
license: MIT
metadata:
  author: gensoura
  version: "1.0"
---

# Release notes

Turn the commits between two Git refs into release notes a user of the project can read.

## When to use

- The user asks for release notes, a changelog entry, or "what changed between X and Y".
- The user is cutting a release or tag and wants the summary written.

Do not use this skill for a single commit message or a pull request description.

## Steps

1. **Pick the range.** Ask for the two refs if the user didn't give them. Default to the latest tag (`git describe --tags --abbrev=0`) through `HEAD`.
2. **Collect the changes.** Run the bundled script from the repository root:

   ```bash
   python3 scripts/collect_changes.py <from-ref> <to-ref>
   ```

   It prints the commits grouped by type (`feat`, `fix`, everything else) as Markdown bullets. If the repository doesn't use Conventional Commits, everything lands under **Other changes**; regroup it by reading the subjects.
3. **Write the notes.** Fill in [the template](assets/release-notes-template.md). Follow [the style guide](references/STYLE-GUIDE.md): user-facing wording, one line per change, breaking changes first.
4. **Check before you hand it over.**
   - Every breaking change is listed under **Breaking changes**, with what the user must do.
   - No internal ticket numbers, author names or commit hashes, unless the user asked for them.
   - Version and date in the heading are right.

## Example

Input: `python3 scripts/collect_changes.py v1.3.0 v1.4.0`

Output (after step 3):

```markdown
## v1.4.0 (2026-10-21)

### Features
- Skills can now be synchronized from a GitHub folder.

### Fixes
- A record whose sync failed returns to its last good status when a retry succeeds.
```

## Edge cases

- **No commits in the range:** say so; don't invent changes.
- **Ref not found:** the script exits with code 2 and names the ref. Ask the user for a valid tag or branch.
- **Merge commits only:** the script skips merges; if nothing is left, read the merged branches' subjects with `git log --first-parent`.
