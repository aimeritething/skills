---
name: review-new-work
description: Implementation cleanup review for issue links, PRD links, branch diffs, latest commits, or prompts such as "review the new commit" or "review this implementation". Use when the user wants Codex to understand the intended change, inspect local diffs and commits, compare against an issue or PRD when provided, directly apply non-behavior-changing readability and maintainability improvements, and run validation.
---

# Review New Work

## Goal

Review already-written work and improve its structure without changing behavior. If the code is already clean, make no edits and say so.

## Inputs

- If the user provides an issue or PRD link, open it with the appropriate available tool and extract the intent, acceptance criteria, and constraints before reading code. If the link is inaccessible, say that clearly and ask the user to provide the contents or confirm continuing from local changes only.
- If the user asks to review a commit, use the requested commit. For "new commit" or "latest commit", inspect `HEAD`.
- If no commit is specified, inspect the current branch changes. Prefer the upstream or default-branch merge base when it is obvious; otherwise use `git status`, recent commits, and the working tree to determine the review surface.
- Read project instructions and standards before changing code. In this repo, load `AGENTS.md` and `.sandcastle/CODING_STANDARDS.md` when present.

## Workflow

1. Understand the change. Read the relevant diff and commits, then summarize the intended behavior in your own working notes before editing.
2. Check correctness. Verify the implementation matches the issue, PRD, commit intent, or user request. Look for missing edge cases, missing tests, unsafe casts, `any` types, unchecked assumptions, injection risks, credential leaks, and behavior that depends on fragile ordering or hidden state.
3. Look for simplifications that preserve behavior:
   - Reduce unnecessary complexity and nesting.
   - Remove redundant code, wrappers, and abstractions.
   - Improve unclear variable, function, and component names.
   - Consolidate related logic when it makes the code easier to read.
   - Remove comments that only restate obvious code.
   - Replace nested ternary expressions with clearer `switch` statements or `if`/`else` chains.
   - Prefer explicit, readable code over compact cleverness.
4. Keep useful structure. Do not flatten code when the abstraction carries meaning, separates concerns, improves testability, or makes future extension easier.
5. Apply edits directly on the branch when improvements are clear. Preserve all existing features, outputs, public APIs, and user-visible behavior.
6. Run relevant validation. For this repo, default to `bun typecheck` and `bun check`; run narrower or broader tests when the touched area calls for it. If validation cannot run, report why.

## Boundaries

- Do not turn this into a feature rewrite. Only refactor, simplify, rename, or tighten checks when behavior stays intact.
- Do not revert unrelated user changes. Work with dirty state carefully and keep edits scoped to the review surface.
- Do not add broad abstractions just to reduce line count.
- Do not leave speculative TODOs or explanatory comments unless they clarify genuinely non-obvious behavior.

## Final Response

Report the result briefly:

- State whether edits were made or the code was already clean.
- Name the important files changed.
- List validation commands run and their outcomes.
- Mention any remaining risks, skipped checks, or follow-up questions.
