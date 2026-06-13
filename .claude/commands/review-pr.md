---
allowed-tools: Bash(gh pr view:*),Bash(gh pr diff:*),Bash(gh pr comment:*),Bash(git diff:*),Bash(git log:*),Read,Glob,Grep
description: Review a pull request or working-tree diff against this repo's conventions
---

Perform a code review using subagents for this repo's focused concerns:

- tool-pattern-reviewer
- live-test-reviewer
- repo-conventions-reviewer

Instruct each to only provide noteworthy feedback. Once they finish, review the feedback and post only the feedback that you also deem noteworthy.

The reviewers read the diff, not the test output. Live test results are verified at the definition of ready, not here. Do not report on whether tests pass; report on whether the diff follows the conventions.

Provide feedback using inline comments for specific issues. Use a top-level comment for the summary. Keep feedback concise.
