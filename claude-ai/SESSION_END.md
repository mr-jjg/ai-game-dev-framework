# SESSION_END.md
# Read this file only when the human has explicitly confirmed the session is over.

---

## Step 1 — Produce the session summary

Before touching any files, write a session summary for the human to review:

- What was built or decided this session
- Which ROADMAP.md items were targeted
- Which repo files changed
- Any decisions worth logging in FYI.md

Present the summary. Do not proceed until the human approves it.

---

## Step 2 — Propose file updates

For each file that needs updating, read the current file first.
Match its existing formatting exactly — do not introduce new styles or structures.
The file is the source of truth for its own format.

### CONCEPT.md
Rarely changes. Only update if a fundamental design decision was revised this session.
If unchanged, skip it.

### ROADMAP.md
Update status tags on items worked this session: [planned] [in-progress] [done] [blocked].
Remove completed milestones entirely — do not archive them. History lives in SESSION_LOG.csv.
Add new items or sub-items discovered this session.
Add a blocked note if anything is blocked, describing what the next PLANNING session should address.
If unchanged, skip it.

### GDD.md
Add or expand sections for any mechanic or system designed or implemented this session.
Do not duplicate CONCEPT.md. GDD.md answers "how does it work", not "what is it".
If unchanged, skip it.

### FYI.md
Append one entry per significant decision made this session.
Entries are append-only. To reverse a prior decision, add a new entry noting the reversal.
If no significant decisions were made, skip it.

### DIGEST.md
Update any file summaries for code that changed this session.
Add entries for new files. Do not describe assets — name and type only.
If unchanged, skip it.

---

## Step 3 — Present all proposed updates

Show the human every proposed change before writing anything.
Iterate until the human is satisfied.
Do not produce the zip until all updates are approved.

---

## Step 4 — Produce SESSION_END.zip

The zip contains:
- Every repo file that changed (approved updates from Step 3)
- session_summary.txt — the approved session summary from Step 1,
  formatted as a single SESSION_LOG.csv row:
  session_id, name, date_start, date_end, summary, roadmap_items,
  files_changed, git_commit_hash
  Leave git_commit_hash blank — Claude Code populates it during REVIEW.

Present the zip to the human with the update command:
"Drop SESSION_END.zip in the repo root and run: python update.py"

---

## Standing rules

- Read before you write. Every file update starts with reading the current file.
- Match the format you find. Never introduce style changes.
- If a file does not need updating, do not include it in the zip.
- The human approves all proposed changes before the zip is produced.
- session_summary.txt is not a repo file — it is instructions for Claude Code.
