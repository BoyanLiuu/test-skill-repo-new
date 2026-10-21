#!/usr/bin/env python3
"""Print the commits between two Git refs as Markdown, grouped by Conventional Commit type.

Usage: python3 scripts/collect_changes.py <from-ref> <to-ref>

Run it from the repository root. Needs only Python 3.8+ and git; no other dependencies.
Exit codes: 0 ok, 1 usage error, 2 a ref was not found, 3 git failed.
"""
import re
import subprocess
import sys

GROUPS = (("feat", "Features"), ("fix", "Fixes"))
SUBJECT = re.compile(r"^(?P<type>[a-z]+)(\([^)]*\))?(?P<breaking>!)?:\s*(?P<text>.+)$")


def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def require_ref(ref):
    try:
        git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    except RuntimeError:
        print(f"error: ref not found: {ref}", file=sys.stderr)
        sys.exit(2)


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    start, end = argv[1], argv[2]
    require_ref(start)
    require_ref(end)
    try:
        subjects = git("log", "--no-merges", "--format=%s", f"{start}..{end}").splitlines()
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3

    grouped = {title: [] for _, title in GROUPS}
    other, breaking = [], []
    titles = dict(GROUPS)
    for subject in filter(None, (s.strip() for s in subjects)):
        m = SUBJECT.match(subject)
        text = m.group("text") if m else subject
        if m and m.group("breaking"):
            breaking.append(text)
        if m and m.group("type") in titles:
            grouped[titles[m.group("type")]].append(text)
        else:
            other.append(text)

    if not (breaking or other or any(grouped.values())):
        print(f"No commits between {start} and {end}.")
        return 0
    sections = [("Breaking changes", breaking), *grouped.items(), ("Other changes", other)]
    for title, items in sections:
        if items:
            print(f"### {title}")
            print("\n".join(f"- {item}" for item in items))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
