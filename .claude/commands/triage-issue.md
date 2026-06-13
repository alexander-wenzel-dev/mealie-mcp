---
allowed-tools: Bash(gh issue view:*),Bash(gh issue edit:*),Bash(gh issue comment:*),Bash(gh label list:*),Bash(gh search issues:*),Read,Glob,Grep
description: Triage a newly opened issue by classifying labels and surfacing likely duplicates
---

A new issue was opened. The dispatcher passes `REPO`, `ISSUE_NUMBER`, `TITLE`, and `AUTHOR` as positional context.

Read the issue body with `gh issue view <ISSUE_NUMBER> --json body --jq .body`.

Classify the issue and apply labels. List available labels with `gh label list` and apply with `gh issue edit <ISSUE_NUMBER> --add-label <name>`. Pick labels that describe what the issue is about, not how it should be fixed.

Search for likely duplicates with `gh search issues --repo <REPO> <terms>`. If a clear duplicate exists, post a comment via `gh issue comment <ISSUE_NUMBER>` linking the original.

If the issue is too vague to classify, post a comment asking for the missing information instead of guessing labels.
