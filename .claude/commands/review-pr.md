---
allowed-tools: Bash(gh pr view:*),Bash(gh pr diff:*),Bash(gh pr comment:*),Bash(git diff:*),Bash(git log:*),Read,Glob,Grep
description: Review a pull request or working-tree diff against this repo's conventions
---

Perform a code review against this repo's conventions using focused subagents, choosing which to run by what the diff changes:

- repo-conventions-reviewer: always. Security, writing style, commit and PR-body conventions, and unit-test conventions apply to any code or config change.
- tool-pattern-reviewer: only when the diff touches `src/mealie_mcp/tools/`.
- live-test-reviewer: only when the diff touches `tests/live/`.

When a PR number is provided, get the diff with `gh pr diff <number>` as your first action. Do not reconstruct it with raw git: the PR checkout is a detached head and chasing the merge base wastes turns. Only for a local review with no PR number, use `git diff origin/main...HEAD`. Then decide which subagents apply from the changed paths. Include the diff when instructing each subagent: they only have `Glob, Grep, Read` and cannot fetch it themselves, so without it they default to reading current file state and may flag pre-existing issues as PR concerns.

Run each subagent synchronously, so the call blocks until it returns its feedback. Do not end your turn to wait for a background completion notification; nothing wakes the run to resume. Instruct each to only provide noteworthy feedback. Once all have returned in this same turn, review the feedback and post only the feedback that you also deem noteworthy.

The reviewers read the diff, not the test output. Test results are verified by CI, not here. Do not report on whether tests pass; report on whether the diff follows the conventions.

Provide feedback using inline comments for specific issues. Use a top-level comment for the summary. Keep feedback concise. Posting the summary is the final, required step, done after the subagents return. Feedback you leave as a reply instead of posting through the comment tool is discarded and never reaches the user.
