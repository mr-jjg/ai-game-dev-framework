# PLANNING.md
# Claude Code standing instructions — read this file at the start of every session.

---

## Step 0 — Identify the state

Before doing anything else, determine which state this session is entering.
If it is not immediately clear from the human's opening message, ask explicitly.
Do not infer. Do not proceed until the state is confirmed.

States you operate in:

- SESSION_1 — first session, CONCEPT.md is blank
- PLANNING — preparing a BUILD session for Claude.ai
- REVIEW — evaluating SESSION_END.zip from a completed BUILD session
- ESCALATE — resolving an out-of-scope question flagged during BUILD
- SESSION_END — closing an unresolvable session

---

## SESSION_1

Condition: CONCEPT.md is blank.

This is the bootstrapping session. No game exists yet. Your job is to work
with the human to establish the game concept and seed all project documents.

1. Ask the human to describe the game they want to build. Listen. Ask
   clarifying questions until you have enough to populate CONCEPT.md with
   confidence. Do not populate it from a guess.

2. Produce the following documents:

   CONCEPT.md       — what the game is: genre, core loop, tone, scope
                      constraints, what it will not do
   ROADMAP.md       — rough list of problems to solve, coarse enough to
                      be honest, specific enough to anchor SESSION_2
   GDD.md           — blank structure only; sections defined, no content
   FYI.md           — first entry: decisions made during SESSION_1,
                      why this genre, what was scoped out and why
   SESSION_LOG.csv  — first row; use schema:
                      session_id, name, date_start, date_end, summary,
                      roadmap_items, files_changed, git_commit_hash
   DIGEST.md        — blank; codebase does not exist yet

3. Present all documents to the human for review. Iterate until approved.

4. Execute the two-commit pair:
   - First commit: all files above except SESSION_LOG.csv
     Commit message: "feat: [session 1] bootstrap project documents"
   - Capture hash, append SESSION_LOG.csv row with git_commit_hash populated
   - Second commit: SESSION_LOG.csv only
     Commit message: "chore: session log update session 1"

Exit → PLANNING

---

## PLANNING

Condition: CONCEPT.md is populated. Human has initiated a new session.

Your job is to prepare Claude.ai for a focused BUILD session.

1. Read in order:
   - ROADMAP.md        — where are we now, where are we going?
   - SESSION_LOG.csv   — where have we been?
   - DIGEST.md         — what does the project look like?
   - Relevant codebase files — drill into what's relevant to this session

2. Collaborate with the human. Align on session intent and scope.
   What is the goal of this BUILD session? What ROADMAP item is being targeted?

3. Reason through context sufficiency in order:
   a. Can Claude.ai solve this from DIGEST.md + relevant files alone?
   b. If not, is this one session's worth of work?
   c. If not, decompose the ROADMAP item into sub-items, augment ROADMAP.md,
      and repeat from step 3 with the first sub-item.

4. Produce SESSION_START.zip containing:
   - INSTRUCTIONS.md
   - CONCEPT.md
   - ROADMAP.md
   - GDD.md
   - FYI.md
   - SESSION_LOG.csv
   - SESSION_END.md
   - DIGEST.md
   - Any relevant code files identified in step 1

5. Produce the session spec prompt:
   - Concise description of what the human and Claude.ai are doing today
   - This is NOT inside the zip — it is what the human pastes to open
     the Claude.ai session
   - One short paragraph maximum

Present SESSION_START.zip and session spec prompt to human for review.
Human drops zip into Claude.ai project, pastes session spec prompt to open session.

Exit → BUILD (Claude.ai takes over)

---

## REVIEW

Condition: Human has returned with SESSION_END.zip from a completed BUILD session.

Your job is to evaluate whether the session output meets the spec.

1. Unpack SESSION_END.zip.

2. Read the git diff.

3. Check SESSION_END.zip contents against the session spec prompt for alignment.
   Ask yourself: does what came back match what was asked for?

4a. If spec met:
   - Have the human drop SESSION_END.zip in the repo root and run:
       python update.py
     The script will: unpack the zip, write updated repo files,
     append the session summary row to SESSION_LOG.csv (with
     git_commit_hash blank), and delete the zip.
   - Propose a commit message to the human for review and approval.
     Format: "feat: [session N] <description of work>"
   - On human approval, execute first commit (all updated repo files
     except SESSION_LOG.csv)
   - Capture the commit hash. Open SESSION_LOG.csv, find the new row
     (git_commit_hash will be blank), populate it with the hash.
   - Execute second commit (SESSION_LOG.csv only)
     Commit message: "chore: session log update session N"
   Exit → PLANNING

4b. If spec not met:
   - Produce a clear, concise ITERATION prompt describing exactly what
     is missing or wrong. The human will take this back to Claude.ai.
   - If the loop has repeated without progress, say so explicitly and
     ask the human whether to continue or end the session.
   Exit → BUILD or → SESSION_END

---

## ESCALATE

Condition: Human has arrived with an escalation prompt written by Claude.ai
during a BUILD session.

Your job is to resolve a specific out-of-scope question so BUILD can continue.

1. Read the escalation prompt carefully.

2. Read the git diff to catch any codebase changes since PLANNING.

3. Work with the human to resolve the question. Use full repo access.
   If you need the full BUILD conversation, ask the human to retrieve it
   from Claude.ai by name and drop it into this context.

4. Produce REPORT.md — a concise, targeted answer to the escalation question.
   Human carries REPORT.md back to the Claude.ai BUILD session.

5. If the question cannot be resolved:
   Say so explicitly. Do not loop.
   Exit → SESSION_END

Exit → BUILD (human carries REPORT.md back)

---

## SESSION_END (unresolved)

Condition: ESCALATE could not resolve, or BUILD/REVIEW loop has stalled.

1. Update any relevant docs to reflect current state accurately.

2. Annotate the open ROADMAP.md item — note what was attempted,
   what blocked progress, and what the next PLANNING session should address.

3. Append SESSION_LOG.csv row with unresolved status noted in summary field.

4. Execute two-commit pair:
   - First commit: all updated files except SESSION_LOG.csv
     Commit message: "chore: [session N] unresolved session - <brief reason>"
   - Capture hash, append SESSION_LOG.csv row with git_commit_hash populated
   - Second commit: SESSION_LOG.csv only
     Commit message: "chore: session log update session N"

Exit → PLANNING (next session picks up from ROADMAP annotation)

---

## Standing rules (apply in all states)

- If the state is unclear, ask. Do not infer.
- If input is ambiguous or incomplete, say so and ask before producing output.
- If the same problem loops more than twice without progress, stop and say so.
- Handoff documents must be concise. Every line earns its place.
- The human approves all commit messages before Claude Code commits.
- The human is the ultimate arbiter of all committed code.
- At session 10, and every 5 sessions after, include a brief retrospective
  prompt in the session spec: is what we're building still what CONCEPT.md
  describes? Are there ROADMAP items we keep deferring that are load-bearing?
