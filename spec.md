# DevFlow V2 Design Context

## Background

DevFlow V1 successfully introduced a disciplined workflow for AI-assisted software engineering:

```
/understand
/design
/tdd
/tasksplit
/implement
/review
```

This workflow works well for greenfield projects because the AI can usually understand the entire codebase within the available context.

However, after using DevFlow on large enterprise repositories, a major limitation became clear.

---

# Problem Statement

Large brownfield projects are fundamentally different.

Typical enterprise repositories contain:

* Hundreds of thousands of lines of code
* Multiple services
* Many business domains
* Years of architectural decisions
* Hidden conventions
* Existing implementation patterns

The current workflow assumes that the AI already has enough context before `/design`.

This assumption is false for large repositories.

The real bottleneck is **context acquisition**, not code generation.

---

# New Design Principle

The goal is NOT to help the AI understand the entire repository.

The goal is to help the AI acquire **just enough context** to safely design and implement a specific change.

Think like a senior engineer.

A senior engineer does not read 500k LOC before implementing a feature.

Instead they:

* clarify the requirement
* identify the affected subsystem
* investigate only relevant code
* identify existing patterns
* understand constraints
* then begin designing

DevFlow V2 should teach AI agents to follow this same process.

---

# Public Workflow

The public workflow should remain intentionally small.

```
/understand
/design
/tdd
/tasksplit
/implement
/review
```

Do not introduce many new public commands.

The intelligence should live inside `/understand`.

---

# New Role of /understand

## Goal

Create enough context to safely design a change.

NOT

* understand the whole repository
* generate architecture documentation
* build a knowledge graph

Instead:

Acquire sufficient understanding of the feature's surrounding system.

---

# Responsibilities of /understand

## Phase 1 — Clarify the Requirement

Ask questions such as:

* What change is requested?
* Why is it needed?
* What is the expected outcome?
* Are there acceptance criteria?

Produce a clear problem statement.

---

## Phase 2 — Locate the System

Instead of scanning the whole repository, guide the user through targeted investigation.

Examples:

* Find the API involved
* Find the service responsible
* Find similar functionality
* Find related classes
* Find related modules

The AI should ask the user to perform targeted IDE searches when necessary.

Examples:

* Symbol Search
* Find References
* Call Hierarchy
* Search by endpoint
* Search by class name

---

## Phase 3 — Build Context Incrementally

As new information is discovered, continuously build a working understanding.

Example:

Feature

Affected Domain

Affected Components

Relevant Files

Existing Patterns

Dependencies

Integrations

Constraints

Risks

Unknowns

---

## Phase 4 — Discover Existing Patterns

Before designing anything, investigate:

* similar features
* similar APIs
* retry implementations
* authorization patterns
* validation patterns
* persistence patterns

The AI should encourage reuse before invention.

---

## Phase 5 — Discover Constraints

Ask about:

* backward compatibility
* security
* performance
* deployment
* customer impact
* data migration

These often determine the implementation strategy.

---

## Phase 6 — Determine Readiness

Only proceed to `/design` once enough context has been gathered.

---

# Investigation UX

The AI should not ask broad questions.

Instead, each investigation should be small and actionable.

Example:

Objective

Identify the service responsible for shipment synchronization.

Suggested Search

ShipmentSync

Expected Output

* class names
* package names
* relevant files

Next Step

Share the results here.

The AI should guide one investigation at a time.

---

# Understanding Progress

During the conversation, maintain a visible progress tracker.

Example

```
Understanding Progress

✓ Problem Statement

✓ Business Goal

◯ Domain

◯ Components

◯ Existing Patterns

◯ Constraints

◯ Risks

◯ Ready for Design
```

As information is collected, update the progress.

This makes the investigation feel structured instead of conversational.

---

# FEATURE_PLAN.md

The output of `/understand` should be a reusable artifact.

Suggested sections:

* Feature Summary
* Business Goal
* Scope
* Affected Domains
* Relevant Components
* Relevant Files
* Existing Patterns
* Constraints
* Risks
* Unknowns
* Open Questions

This becomes the input to `/design`.

---

# Optional Project Memory

Future versions may support lightweight project memory such as:

```
.devflow/

PROJECT_CONTEXT.md
ARCHITECTURE.md
CONVENTIONS.md
DECISIONS.md
```

These files are optional.

They should accelerate understanding but should never become mandatory.

DevFlow should always work even without them.

---

# Important Design Decisions

Do NOT build:

* Knowledge Graph
* Neo4j
* Vector Database
* Repository Parser Platform
* Custom Indexing Engine

Instead, leverage:

* IDE symbol search
* Find References
* Call Hierarchy
* Existing repository structure
* Human guidance

The workflow is the product.

The IDE provides repository intelligence.

---

# Immediate Development Tasks

## Task 1

Redesign the `/understand` skill around investigation instead of summarization.

---

## Task 2

Design the investigation conversation flow.

Determine:

* question ordering
* stopping conditions
* progress model

---

## Task 3

Design the FEATURE_PLAN.md template produced by `/understand`.

---

## Task 4

Create reusable investigation prompts for common scenarios:

* locate API
* locate service
* locate database
* locate similar implementation
* locate integration
* locate configuration

---

## Task 5

Design how `/design` consumes FEATURE_PLAN.md.

Ensure every later workflow step depends on the structured understanding rather than the original user request.

---

# Core Philosophy

DevFlow is not trying to make AI smarter.

DevFlow is teaching AI to behave like an experienced software engineer.

For brownfield development, that begins with disciplined investigation before design.
