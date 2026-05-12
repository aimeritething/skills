---
name: peel
description: Interview the user about a plan or design by peeling back layers — start with the big picture (goals, constraints, users), then architecture and tradeoffs, then implementation details. Use when user wants to stress-test a plan, get grilled on their design, or says "peel" / "peel the onion". A structured alternative to grill-me.
---

Interview me relentlessly about this plan until we reach a shared understanding. Ask questions one at a time, and provide your recommended answer with each.

## Questioning approach: peel the onion

A good design review doesn't start with "what database will you use?" — it starts with "what problem are you solving and for whom?" The broad questions often reveal that the details need to be rethought entirely, so nailing them first saves everyone time.

**Layer 1 — The big picture.** Start here. Understand the goals, constraints, and context before touching any implementation:
- What problem does this solve, and why now?
- Who are the users / stakeholders, and what do they care about most?
- What are the hard constraints (timeline, budget, compatibility, team size)?
- What does success look like? How will you know this worked?

**Layer 2 — Architecture and approach.** Once the "why" is clear, explore the "how" at a structural level:
- What are the major components and how do they interact?
- What alternatives did you consider, and why did you pick this one?
- Where are the key tradeoffs, and which side are you leaning?
- What are the biggest risks or unknowns?

**Layer 3 — Details and edge cases.** Only after the higher layers are solid, drill into specifics:
- Implementation choices, data models, API shapes
- Error handling, failure modes, rollback strategies
- Edge cases, performance concerns, security implications
- Migration path, backwards compatibility, deployment plan

Move to the next layer when you feel the current one is sufficiently resolved — you don't need to exhaustively cover every question before progressing. If a detail-level question surfaces a gap in the big picture, zoom back out.

If a question can be answered by exploring the codebase, explore the codebase instead.
