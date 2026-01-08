---
description: Commit all changes and push to GitHub
---

# Commit and Push to GitHub

Commit all changes and push to GitHub.

## Instructions

1. Run `git status` to see all changed and untracked files
2. Run `git diff --stat` to see a summary of changes
3. Run `git log --oneline -3` to see recent commit message style
4. Add all changes with `git add -A`
5. Create a commit with a descriptive message that:
   - Summarizes the nature of the changes (new feature, bug fix, enhancement, etc.)
   - Is concise (1-2 sentences) focusing on the "why" not the "what"
   - Ends with: `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>`
6. Push to the remote repository with `git push origin <current-branch>`
7. Report the commit hash and summary to the user

## Important Notes

- If there are no changes to commit, inform the user
- Never commit files that appear to contain secrets (.env, credentials, API keys)
- Use a HEREDOC for the commit message to ensure proper formatting
