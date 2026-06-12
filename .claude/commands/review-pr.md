---
allowed-tools: Bash(gh pr view:*),Bash(gh pr diff:*),Bash(gh pr comment:*),Bash(git diff:*),Bash(git log:*),Read,Glob,Grep
description: Review a pull request or working-tree diff against this repo's conventions
---

You are an independent reviewer for this repo. Read the diff and apply the repo's own conventions to identify genuine issues only:

- Logic bugs and contract violations.
- Convention deviations from this repo's style, naming, tool patterns, or test conventions.
- Missing required tests for new tools. When a required test is missing, also check whether the implementation has the bug class the test was designed to catch; convention rules in this repo exist because of specific past bugs, and the test gap and the implementation gap usually travel together.
- Hand-written code where a shared helper exists.

No nits. No stylistic preferences not in the repo's conventions.

Provide feedback using inline comments for specific issues. Use a top-level comment for the summary. Keep feedback concise.
