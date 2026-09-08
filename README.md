# AI-Assisted Game Dev Framework

A forkable scaffold for building games with AI assistance across two environments,
without losing the thread between sessions.

---

## What this is

Building software conversationally with an LLM has a known failure mode: the model
has no memory between sessions, so context has to be rebuilt every time. Rebuild it
badly and you get confident wrong answers. Rebuild it exhaustively and you burn the
context window before any work happens.

This framework solves that by splitting the work across two environments with
different strengths:

**Claude Code** has filesystem access. It reads the whole repo, holds the project
in view, and decides what a given session actually needs. It plans, it reviews,
it answers the hard questions that require full context.

**Claude.ai** is where you build. It receives a lean, targeted context package
prepared by Claude Code - not the whole project, just what today's work requires.
You develop in your engine; it pair programs with you.

You are in the loop at every handoff. Nothing moves between environments without
passing through you.

The framework is engine-agnostic. Nothing in it assumes Godot, Unity, or anything
else. Engine specifics live in your project documents, not in the machinery.

---

## The loop

```
PLANNING  (Claude Code)   →  prepare the session, produce context package
BUILD     (Claude.ai)     →  do the work
REVIEW    (Claude Code)   →  check it, commit it
                          →  back to PLANNING
```

Two side paths:

**ESCALATE** - during BUILD, a question comes up that needs full-project context.
Claude.ai writes you a prompt. You take it to Claude Code, get an answer, come back.

**SESSION_END** - something can't be resolved. Rather than looping, the session
closes cleanly with notes on what blocked it. The next PLANNING session picks it up.

Planning happens before every session. It can take two minutes. It never gets skipped.

---

## Files

| File | What it is |
|------|-----------|
| `claude-ai/INSTRUCTIONS.md` | Claude.ai's standing instructions. Goes in every session. |
| `CONCEPT.md` | What the game is. Genre, core loop, scope, what it will not do. |
| `ROADMAP.md` | What's being built and in what order. The living spec. |
| `GDD.md` | How it works. Grows as systems get designed. |
| `FYI.md` | Decision log. Why choices were made, and what they foreclose. |
| `DIGEST.md` | Codebase map. Like a header file for the whole project. |
| `SESSION_LOG.csv` | One row per session. The index and the audit trail. |
| `CLAUDE.md` | Claude Code's standing instructions. Auto-loaded every session. |
| `claude-ai/SESSION_END.md` | How Claude.ai closes a session. |
| `update.py` | Applies a finished session's changes to the repo. |

---

## Getting started

**1. Fork and clone.** That's the whole setup. No scripts, no dependencies,
no database.

**2. Open Claude Code in the repo.** Tell it you're starting a new project.
It auto-loads `CLAUDE.md`, sees that `CONCEPT.md` is blank, and runs
SESSION_1: working with you to define the game and seed every project document.

**3. Create a Claude.ai Project.** From here on, Claude Code prepares each
session's context package. You drop it in and build.

---

## Running a session

**Plan it.** Open Claude Code. It reads the roadmap, the log, the digest, and
whatever code is relevant. You align on what this session is for. It hands you
a zip and a prompt.

**Build it.** Open a new Claude.ai conversation in your Project. Paste the prompt,
drop the zip. Work. Name the conversation something you'll recognize later - that
name is how you find it again if you ever need the full transcript.

**Close it.** Tell Claude.ai the session is over. It reads `SESSION_END.md`,
proposes updates to every document that changed, and produces `SESSION_END.zip`
once you approve them.

**Review it.** Drop the zip in the repo root:

```
python update.py
```

Then back to Claude Code. It reads the diff, checks the work against what was
asked for, and proposes a commit message. You approve. It commits.

---

## Why commits come in pairs

Every session produces two commits:

```
abc1234  feat: [session 7] player movement and collision
def5678  chore: session log update session 7
```

The first is the work. The second is `SESSION_LOG.csv` with the first commit's
hash written into it - which can't happen until that commit exists. The rhythm
is self-documenting: the log entry is always the commit immediately after the
one it describes.

---

## Design principles

**Verbosity is a bug.** You are context-switching between two agents and
reviewing everything both of them produce. Long documents get skimmed, and
skimming is silent truncation. Every line earns its place.

**Ask, don't infer.** Both agents are instructed to stop and ask when something
is ambiguous rather than proceeding on a guess. A clarifying question costs
one exchange. A wrong assumption costs a session.

**The human is the arbiter.** No commit happens without your approval. No context
moves between environments without passing through you. The agents propose;
you decide.

**One source of truth.** Documents live in the repo. Claude Code bundles them
into each session package, so there's nothing to keep in sync manually and
nothing to forget to upload.

**History lives in the log.** Completed roadmap items get deleted, not archived.
`ROADMAP.md` answers where you are and where you're going. `SESSION_LOG.csv`
answers where you've been.

---

## On the record

Commit messages tell you what changed. They don't tell you why the decision was
made, what alternatives were considered, or what the choice ruled out. In a
conversational workflow that reasoning is the most valuable thing produced and
the easiest thing to lose.

`FYI.md` is the decision log. `SESSION_LOG.csv` is the index - and if you ever
need the full conversation behind a decision, the log has the name to look it up.

The practice comes from what's sometimes called an Automated Decision Log. The
implementation here is deliberately simple: a markdown file, an instruction to
keep it current, and a human who reads it.

Verify what goes in it. The point of the log is that it's trustworthy.
