---
name: opc-rd
description: "Use when the user explicitly invokes $opc-rd or explicitly asks to apply this One Person Company R&D standard. Do not trigger for ordinary implementation, debugging, documentation, skill editing, review, release, or deployment work."
---

# OPC R&D (One Person Company)

This skill is opt-in. When the user has not explicitly requested it, use the task's normal workflow.

When invoked:

- Start with the requested result. Read only the files needed to produce it.
- Do not add process artifacts, methods, reviews, agents, or tools unless the user explicitly requests them for the current task.
- For real production changes, customer data, credentials, payments, external communication, permission changes, destructive operations, or irreversible effects, obtain the required explicit authorization before the effect and preserve a practical recovery path.
- Verify the requested result in proportion to the change. Do not invent pressure scenarios or additional product requirements.
- Only when the user also asks to apply personal stack preferences, read [references/stack-defaults.md](references/stack-defaults.md); repository and current user choices override it.

Finish by reporting only what changed, the checks actually run, and any material remaining risk.
