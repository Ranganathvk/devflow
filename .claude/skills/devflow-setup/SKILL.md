---
name: devflow-setup
description: >-
  Initializes Devflow in the current repository after the Cursor plugin is
  installed. Creates devflow.context.yaml, SPEC.md, and PROJECT_STATE.md
  without overwriting existing files. Use when setting up Devflow in a project.
disable-model-invocation: true
---

# /devflow-setup — Initialize this project

## Purpose

Create the minimal project-local state required by Devflow. Plugin installation
provides the skills; this command initializes the repository that will use them.

## Workflow

1. Confirm the current workspace is the intended project root.
2. If `devflow.context.yaml` exists, read `context_dir` and use it.
3. Otherwise ask for a context folder name, recommending `artifacts`, then
   create `devflow.context.yaml` from
   [the manifest template](references/devflow.context.template.yaml).
4. Create the resolved context directory if missing.
5. If `<context_dir>/SPEC.md` is missing, copy
   [the SPEC template](references/SPEC.template.md).
6. If `<context_dir>/PROJECT_STATE.md` is missing, copy
   [the state template](references/PROJECT_STATE.template.md), replacing
   `{context_dir}` with the resolved folder name.
7. Do not create reference contracts. Workflow skills create contracts only
   when they are needed.
8. Report created and preserved paths. Suggest `/to-spec <path>` when a source
   requirements document exists; otherwise suggest `/grillme spec`.

## Safety

- Never overwrite or merge an existing manifest, SPEC, or project-state file.
- Never copy `core/`, `.cursor/skills/`, or adapter files into the project.
- Never initialize outside the current workspace.
- If the workspace root is unclear, ask before writing.

## Expected result

```text
<project>/
├── devflow.context.yaml
└── artifacts/                 # or the chosen context_dir
    ├── SPEC.md
    └── PROJECT_STATE.md
```
