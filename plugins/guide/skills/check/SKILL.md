---
name: check
description: >-
  Use to verify work or hunt for defects: "check this", "is this done", "verify this before we ship", "find bugs in this", "audit this". Starts `sentinel:gate` to verify an artifact against its criteria, or `ranger:audit` to look for reachable defects in code.
version: 1.0.0
---

# Guide — Check

Say "Mode: check." To confirm something meets its criteria (a spec, plan, implementation or PR), invoke the `sentinel:gate` skill. To find bugs or vulnerabilities in code, invoke the `ranger:audit` skill. If unsure, ask which the user wants: confirmation against criteria, or a defect hunt.
