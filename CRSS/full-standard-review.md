ISSUE-01: Orchestrator level contradiction (Strict-B vs “Strict-B or Strict-A”)
-------------------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Line 91:
      - [main.py (Strict-B or Strict-A non-critical orchestrator)](#mainpy-strict-b-or-strict-a-non-critical-orchestrator)
  - Line 1236:
      # main.py (Strict-B or Strict-A non-critical orchestrator)
  - Lines 1558–1564:
      1558 **Outer Orchestrator (Core)**  
      ...
      1564 **Inner Orchestrator (Strict-B)**  

ISSUE:
  The ToC and the “main.py” heading describe main.py as
  “Strict-B or Strict-A non-critical orchestrator” while §16.8 explicitly
  defines the inner orchestrator as Strict-B. The architecture blueprint
  (5-Annexes/crss_python_architecture_blueprint.md, lines 295–323) also uses a
  Strict-B orchestrator only.

IMPACT:
  - Confusing for implementers and auditors about whether a Strict-A orchestrator is allowed.
  - Risks misplacing orchestration responsibilities into Strict-A, which you otherwise reserve
    for validators and kernels.
  - Creates a visible inconsistency between Master and Architecture Blueprint.

RECOMMENDED FIX:
  - Make orchestrator level unambiguous and aligned with the architecture blueprint:
    - Change line 91 to:
        - [main.py (Strict-B non-critical orchestrator)](...)
    - Change line 1236 to:
        # main.py (Strict-B non-critical orchestrator)
    - In §16.8 (lines ~1558–1564), optionally add:
        “The inner orchestrator is always Strict-B; Strict-A is reserved for
         Level-A validators and kernels only.”
  - If you ever want Strict-A orchestrators, explicitly update §16.8 and the blueprint
    to say “Strict-B or Strict-A (non-critical only)” and describe the rules distinctly.
  - I recommend enforcing **Strict-B only** for inner orchestrators.


ISSUE-02: Import rules table ambiguity (Mode & Safety Levels model)
-------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_mode_and_safety_model.md

LOCATION:
  - Lines 242–250:
      243 | Caller -> Callee            | Allowed? | Notes                                     |
      244 |----------------------------|---------|-------------------------------------------|
      245 | Core -> Core                |        |                                           |
      246 | Core -> Strict              | [NOT ALLOWED]       |                                           |
      247 | Strict -> Core              |        | With restrictions                         |
      248 | Strict-A (Critical) -> Core | [NOT ALLOWED]       |                                           |
      249 | Strict-A (Non-Critical) -> Core |    | If result cannot enter critical path      |

  - Master cross-reference:
      1-Specifications/Master/crss_python_standard_safety_master.md
      Lines 1504–1506:
        **CRSS-Call-Profile-2**  
        Strict→Core allowed only in tests/tools.

ISSUE:
  The “Allowed?” column is left blank for:
  - Core -> Core
  - Strict -> Core
  - Strict-A (Non-Critical) -> Core

  Meanwhile, the Master document defines explicit profile rules:
  - CRSS-Call-Profile-1: Strict must not depend on Core in baseline.
  - CRSS-Call-Profile-2: Strict→Core allowed only in tests/tools.

  The Mode model table is therefore ambiguous, and appears looser than the Master.

IMPACT:
  - Tools or readers relying on this table could interpret blank cells as “Allowed”
    or “unspecified”, contradicting Master constraints.
  - Inconsistent enforcement at code-review and tooling level.

RECOMMENDED FIX:
  - Make the table fully explicit and align with Master rules:
      245 | Core -> Core                | Allowed      |                                           |
      246 | Core -> Strict              | [NOT ALLOWED] |                                           |
      247 | Strict -> Core              | [NOT ALLOWED] | Except where CRSS-Call-Profile-2 (tests/tools) applies |
      248 | Strict-A (Critical) -> Core | [NOT ALLOWED] |                                           |
      249 | Strict-A (Non-Critical) -> Core | [NOT ALLOWED] | Except where CRSS-Call-Profile-2 (tests/tools) applies |

  - Add a short note below the table:
      “For Strict→Core, the only exception is CRSS-Call-Profile-2 (tests/tools only),
       defined in the Master standard. Production builds MUST treat Strict→Core as NOT ALLOWED.”


ISSUE-03: Safety Levels & Mode duplication without explicit source-of-truth
---------------------------------------------------------------------------
FILES:
  - 1-Specifications/Master/crss_python_mode_and_safety_model.md
  - 1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Mode & Safety in Mode model:
      Line 89:  ### 1.2 Safety Levels
      Line 106: Mode = (Profile, Safety Level)

  - Mode & Safety in Master:
      Line 165: ### 1.2 Safety Levels
      Line 182: Mode = (Profile, Safety Level)

ISSUE:
  Safety Levels and Mode are defined in both the Mode model and the Master document.
  The definitions are currently consistent, but there is no explicit declaration that
  one document is the normative source-of-truth and the other is a summary.

IMPACT:
  - Future edits risk drifting one definition without updating the other, creating contradictions.
  - Auditors may ask which document has precedence if wording diverges.

RECOMMENDED FIX:
  - In the Master, near lines 165–182, add:
      “The normative definition of Safety Levels and Mode is given in
       ‘CRSS-Python Mode, Safety Levels & Critical Phase Model’. This section
       summarises that model and MUST NOT override it.”
  - Optionally add a similar note at the start of the Mode model:
      “This document is the canonical source for Safety Levels and Mode semantics.”
  - This formally resolves precedence and prevents future inconsistencies.


ISSUE-04: Phase-aware “Forbidden in Critical Code” lacks CRSS rule linkage
---------------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_phase_aware_rule_interpretation_model.md

LOCATION:
  - Lines 40–55:
      40 ### [NOT ALLOWED] Forbidden in Critical Code
      41 
      42 - **I/O of any kind**
      43   - filesystem
      44   - network
      45   - database
      46   - IPC
      47 - **Blocking operations**
      48   - locks
      49   - waits
      50   - condition variables
      51   - blocking queues
      52 - **Dynamic memory allocation** beyond trivial proven-bounded temporaries
      53 - **Subprocess invocation / OS commands**
      54 - **Environment variable access**
      55 - **Runtime scheduling-dependent behavior**
      ...
  - Lines 68–79:
      68 ## 2. Interpretation in Non-Critical Code
      72 ### [OK] Permitted in Non-Critical Code
      74 - File / network I/O
      75 - Memory allocation & object creation
      76 - Caching, buffering, lookup tables
      77 - Subprocess invocation
      78 - Configuration loading
      79 - Platform / environment access

ISSUE:
  The phase-aware document clearly lists forbidden and allowed behaviors, but those
  constraints are not explicitly tied to CRSS-* rule IDs or to the Master’s call/phase rules.
  For example, the critical-phase forbiddances are not referenced back to CRSS-Call-Phase-1
  or any phase-specific rule.

IMPACT:
  - Makes traceability to normative rules weaker for audits and tooling.
  - A regulator may ask: “Which CRSS rule enforces ‘no I/O in critical’?”
  - Harder to prove that static analysis checks implement the normative spec.

RECOMMENDED FIX:
  - At line 40, change heading to:
      “### [NOT ALLOWED] Forbidden in Critical Code (CRSS-Phase-1–3)”
  - Introduce a small set of phase rules in the Master (if not already), e.g.:
      - CRSS-Phase-1 (Critical I/O Ban)
      - CRSS-Phase-2 (Critical Allocation Ban)
      - CRSS-Phase-3 (Critical Blocking Ban)
  - In this document, annotate each bullet group with references, e.g.:
      “Forbidden in critical code (per CRSS-Phase-1, CRSS-Call-Phase-1).”
  - This provides clear, auditable linkage from narrative lists to formal rules.


ISSUE-05: Level-A “mandatory data flow” is not expressed as a normative rule
----------------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Lines 1362–1369:
      1362 Defines cross-safety call rules, orchestrator structure, and the mandatory Level-A data flow:
      1363 
      1364 ```
      1365 Core-C/B Gateway
      1366     → Strict-B Config/Data Provider
      1367     → Strict-A Level-A Validator
      1368     → Strict-A Critical Kernel
      1369 ```

ISSUE:
  The text labels this pipeline as the “mandatory Level-A data flow”, but this flow is
  not given its own CRSS rule ID and is not explicitly stated as a MUST-level requirement.
  Nothing explicitly forbids calling the Strict-A kernel directly from Core or Strict-B
  with ad-hoc or partially validated data.

IMPACT:
  - Creates a safety-level escalation loophole:
      - A developer could feed configuration or sensor data directly into the Strict-A kernel,
        bypassing the Strict-B Config/Data Provider and the Strict-A validator, while still
        claiming compliance with CRSS-Call-1.
  - Weakens your central architectural guarantee that all Level-A data is fully validated.

RECOMMENDED FIX:
  - Introduce a new rule immediately after line 1369, for example:

      **CRSS-Call-Data-1 (Normative — Level-A Data Entry)**  
      Any data influencing Level-A @critical decisions MUST:
      1. Be ingested via a Core-C/B Gateway or Strict-B source.  
      2. Be structurally validated and normalized by a Strict-B Config/Data Provider.  
      3. Be semantically validated by a Strict-A Level-A Validator.  
      4. Only then be provided to Strict-A Critical Kernel functions.  

      Direct feeding of unvalidated or partially validated data into Level-A validators or
      kernels is NOT ALLOWED.

  - Clarify that any path like `Core -> Strict-A Kernel` or `Strict-B -> Strict-A Kernel`
    **without** the provider+validator chain is a violation of CRSS-Call-Data-1.


ISSUE-06: Same-level cyclic dependencies not addressed for Level-A
------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Call rule for Level-A:
      Lines 1434–1455:
        1434 #### 16.3.1 Absolute Rules for Level-A Code
        1438 **CRSS-Call-1 (Normative — Level-A Isolation)**  
        1440 1. A Level-A function (critical or non-critical):
        ...
        1449    - other Level-A Strict functions, or
        1450    - local pure helpers that are explicitly classified as Level-A Strict.

ISSUE:
  CRSS-Call-1, 2, 3 prevent cross-level cycles (A↔B, B↔C, A↔Core, etc.), but the
  standard does not address **same-level cyclic dependencies** (e.g. A1 → A2 → A1).
  This is not inherently unsafe but complicates SCEM & formal reasoning for Level-A.

IMPACT:
  - Level-A call graphs could contain cycles that:
      - Make static analysis and timing reasoning harder.
      - Increase proof complexity for certification.
  - Tools and reviewers lack guidance on whether such cycles are acceptable or discouraged.

RECOMMENDED FIX:
  - Near CRSS-Call-1, add guidance or a new rule, such as:

      **CRSS-Call-4 (Level-A Call Graph Structure)**  
      For Level-A code, the call graph SHOULD form a Directed Acyclic Graph (DAG) at the
      module/service level. Where cycles are unavoidable, they MUST be:
      - Documented in SCEM, and
      - Justified in the safety case.

  - Alternatively, state explicitly that cycles within Level-A are allowed but must
    not cross phase or profile boundaries, and must be documented.


ISSUE-07: Downward contamination via mutation of Level-A-owned data
-------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Summary of Level-A separation:
      Lines 1622–1630:
        1622 ### 16.10 Summary — Level-A Separation
        1624 Level-A code:
        1626 - makes no downward calls (B/C/Core)
        1627 - performs no logging
        1628 - sends no metrics
        1629 - uses no Core utilities

ISSUE:
  The Master clearly prevents Level-A from calling B/C/Core or logging, which prevents
  direct downward contamination. However, the spec does not explicitly forbid lower levels
  (B/C/Core) from mutating shared Level-A data structures after they have been passed into
  Level-A, or from holding references that can be mutated later.

IMPACT:
  - A lower level could accidentally or maliciously alter data that the Level-A kernel
    assumes to be immutable, undermining safety guarantees.
  - This creates a subtle contamination channel: Level-A’s effective behavior could depend
    on lower-level state changes after validation.

RECOMMENDED FIX:
  - After line 1629, add:

      - does not share mutable state with lower levels

  - And earlier in §16 (e.g., near CRSS-Call-Data-1), introduce:

      **CRSS-Data-Ownership-1 (Level-A Data Ownership)**  
      Data structures owned by Level-A validators or kernel MUST NOT be mutated by Level-B/C/Core
      after they have been passed into Level-A. Any data shared between Level-A and lower levels
      MUST be immutable or copied per handoff.

  - Encourage SCEM to capture ownership/immutability constraints explicitly.


ISSUE-08: Config misclassification boundary not fully explicit
--------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Level-A data flow description:
      Lines 1362–1369 (pipeline)
  - Level-A separation:
      Lines 1622–1630 (summary)
  - Example architecture:
      5-Annexes/crss_python_architecture_blueprint.md
      Lines 295–321:
        298 # main_supervisor.py (Strict-B orchestrator)
        299 from input_gateway import read_inputs
        300 from config_manager import load_config
        ...
        315     decision = ctrl.decide(...)
        323 This orchestrator is **non-critical**; only `decide()` is `@critical`.

ISSUE:
  The conceptual division is clear:
  - Config ingestion and parsing: Strict-B / Core.
  - Validation: Strict-A.
  - Kernel: Strict-A @critical.

  But there is no explicit, standalone rule stating that **all config ingestion and parsing
  must stay out of Level-A**, nor a rule forbidding Level-A from parsing or transforming raw
  configuration directly.

IMPACT:
  - Developers may push more logic into Level-A validators or even the kernel “because it’s
    safety-relevant config”, unintentionally mixing responsibilities.
  - Harder to argue that Level-A code is bounded and deterministic if it performs parsing.

RECOMMENDED FIX:
  - Add a rule near the Level-A pipeline (around lines 1362–1369), for example:

      **CRSS-Config-1 (Configuration Boundary)**  
      All configuration ingestion, parsing, and initial decoding MUST be implemented at
      Level-B or Core. Level-A code (validators and kernel) MUST only operate on already
      validated, normalized, bounded config structures provided by Strict-B Config/Data
      Providers.

  - Optionally cross-reference this rule from the Strict and Core profile documents so that
    profile authors know where config responsibilities sit.


ISSUE-09: Safety-level escalation loophole via tests/tools & direct kernel calls
-------------------------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Level-A pipeline:
      Lines 1362–1369.
  - Profile call rule:
      Lines 1504–1506:
        1504 **CRSS-Call-Profile-2**  
        1505 Strict→Core allowed only in tests/tools.
  - Phase interaction rule:
      Lines 1511–1515 (CRSS-Call-Phase-1).

ISSUE:
  Two related loopholes:
  1. It is not explicitly forbidden for a Core or Strict-B entrypoint to call the Strict-A
     kernel directly with ad-hoc data, bypassing the Config/Data Provider and validators.
  2. CRSS-Call-Profile-2 allows Strict→Core “only in tests/tools”, but there is no explicit
     constraint that such test/tool code must be excluded from production builds.

IMPACT:
  - Implementers might:
    - Introduce convenience paths (Core → Strict-A kernel) that skip validation.
    - Ship binaries that still contain test-only Strict→Core assumptions.
  - This undermines the central “all Level-A data passes through a validated pipeline”
    guarantee.

RECOMMENDED FIX:
  - Implement CRSS-Call-Data-1 as described in ISSUE-05 to close the bypass loophole.
  - Extend CRSS-Call-Profile-2 at lines 1504–1506 to:

      **CRSS-Call-Profile-2**  
      Strict→Core is allowed only in tests/tools that are:
      - Clearly separated (e.g. test-only modules/namespaces), and
      - EXCLUDED from certified/production builds.

  - Optionally note that any Strict→Core call discovered in production artifacts is a
    **hard non-compliance**.


ISSUE-10: Logging policy section in Mode model is scope-ambiguous
-----------------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_mode_and_safety_model.md

LOCATION:
  - Lines 267–275:
      267 ##  7. Exception Policies
      269 Logging Allowed Only If:
      271 - Non-blocking
      272 - No heavy formatting
      273 - No network logging in critical
      274 - No exceptions propagated

  - Cross-reference:
      1-Specifications/Master/crss_python_standard_safety_master.md
      Lines 1438–1445 (CRSS-Call-1: Level-A MUST NOT call Core logging, metrics, etc.)
      Lines 1626–1629 (Level-A: “performs no logging”, “uses no Core utilities”).

ISSUE:
  The logging conditions in the Mode model do not explicitly state that they **do not
  override** the stricter Level-A logging ban in the Master. Read in isolation, the
  “Logging Allowed Only If” bullets might be misinterpreted as generally valid even for
  Level-A @critical code, conflicting with CRSS-Call-1 and §16.10 Level-A separation.

IMPACT:
  - Potential misinterpretation where readers think:
      “Logging is allowed in critical as long as it’s non-blocking and no network.”
  - This would contradict Level-A’s explicit “no logging” rule.

RECOMMENDED FIX:
  - Add a scoping sentence at line 267–269:

      “These logging policies apply to non-Level-A contexts. They do NOT relax the
       strict Level-A isolation rules in the Master standard (CRSS-Call-1 and §16.10),
       where Level-A code performs no logging at all.”

  - Optionally link to the Master section:
      “For Level-A logging constraints, see CRSS-Call-1 and ‘Summary — Level-A Separation’.”


ISSUE-11: Call graph notation not standardized for SCEM
-------------------------------------------------------
FILE:
  1-Specifications/Master/crss_python_standard_safety_master.md

LOCATION:
  - Level-A pipeline in ASCII:
      Lines 1362–1369.
  - Machine-readable metadata example:
      Lines 1638–1648:
        1638 ## 17. Machine-Readable Metadata (Optional Annex)
        1642 ```yaml
        1643 - unit: "safety_controller.SafetyController.control_loop"
        1644   profile: "Strict"
        1645   safety_level: "A"
        1646   mode: "Strict-A"
        1647   phase: "critical"
        1648   calls:
        1649     - "builtins.float"  # safe

  - SCEM annex:
      2-Governance/crss_python_SCEM_annexes.md (no direct contradiction, but no unified notation either).

ISSUE:
  The spec uses multiple forms to describe call graphs (tables, ASCII arrows, and code),
  and hints at machine-readable metadata. However, there is no single “recommended notation”
  for SCEM call graphs that includes Mode, Phase, and Profile information together.

IMPACT:
  - Different teams might invent incompatible SCEM call graph formats.
  - Tools and auditors may have to interpret a variety of representations.
  - Harder to standardize automated checks across projects.

RECOMMENDED FIX:
  - Extend §17 (lines 1638–1648) with a short “Recommended SCEM Call Graph Notation”:

      - Nodes labelled as `module.function [Mode, Phase]`.
      - Edges represented explicitly in the `calls:` list.
      - Example including Level-A pipeline:
        - `core_gateway.main [Core-C, non_critical]`
        - `config_provider.load [Strict-B, non_critical]`
        - `validator.validate_config [Strict-A, non_critical]`
        - `kernel.control_loop [Strict-A, critical]`

  - In 2-Governance/crss_python_SCEM_annexes.md, reference this notation as the default
    expected format for SCEM call graph artifacts.


SUMMARY
-------
- I scanned all 41 `.md` documents in the ZIP (Overview, Specifications, Governance,
  Deployment, Policies, Annexes, Release docs).
- No additional *hard contradictions* were found beyond the issues listed above.
- Overview, governance, deployment, and architecture annexes are consistent with the
  CRSS model as defined in the Master + Mode + Phase documents; they mostly differ only
  in level of detail or audience.
- The issues above are mainly:
  - A clear orchestrator-level contradiction (ISSUE-01).
  - Ambiguities or un-named normative requirements around imports, logging, and Level-A
    data flow.
  - Missing explicit rules for Level-A call graph structure, data ownership, and test-only
    Strict→Core exceptions.

Once you patch these, the standard will be much tighter, easier to audit, and safer to
enforce with tooling.
