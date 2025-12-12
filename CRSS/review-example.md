EX-ISSUE-01: “Profiles Used” header is wrong and omits Strict-B
----------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_reference_example_specifications.md

LOCATION:
  Line 12:
    **Profiles Used:** Strict-A, Core-B, Core-C

ISSUE:
  - The example actually uses four Modes: Strict-A, Strict-B, Core-B, Core-C.
  - The header also uses the term “Profiles Used” even though “Strict-A” and “Core-B”
    are Mode names in the official CRSS model (Profile + Safety Level).

IMPACT:
  - Inconsistent with:
      - The code (config.model and sensors.interfaces are Strict-B).
      - The compliance report (which lists Strict-B explicitly).
      - The CRSS “Mode = (Profile, Safety Level)” model.
  - Could mislead auditors into thinking Strict-B is not in scope.

RECOMMENDED FIX:
  - Change the header to use Mode terminology and include Strict-B, e.g.:

    From:
      **Profiles Used:** Strict-A, Core-B, Core-C

    To:
      **CRSS Modes Used:** Strict-A, Strict-B, Core-B, Core-C  
      *(Modes follow the CRSS definition Mode = (Profile, Safety Level);
        e.g. “Strict-A” = Profile Strict, Safety Level A.)*


EX-ISSUE-02: Architecture block and CRSS mapping still say “Voting (Core-B)”
-----------------------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_reference_example_specifications.md

LOCATION A (ASCII block diagram):
  Lines 279–287:
    279:  │ CRSS Client App         │
    280:  │  - JSON parsing (Core-C)│
    281:  │  - Validation (Core-C)  │
    282:  │  - Voting (Core-B)      │
    283:  │  - Safety Envelope      │
    286:  │    (Strict-A)           │

LOCATION B (CRSS Compliance Mapping):
  Lines 775–779:
    775: ### 22.2 Core-B Responsibilities
    776: Core-B is deterministic but not safety-critical:
    777: - computes median
    778: - evaluates spread
    779: - assigns disagreement severity

ACTUAL IMPLEMENTATION:
  - `crss_example_sensor_voting.safety_logic.voting`:
      - Annotated as Strict-A (@critical)
      - Implemented in `safety_logic/voting.py` (lines 1–15, 37)
  - `crss_example_sensor_voting.safety_logic.envelope`:
      - Also Strict-A (@critical)
  - No Core-B module computes the median/spread/voting status.

ISSUE:
  - The spec document still describes voting responsibilities as Core-B, while the
    implemented voting logic is entirely Strict-A.
  - Similarly, the CRSS mapping claims Core-B “computes median/evaluates spread/assigns
    disagreement severity”, which is actually done in Strict-A.

IMPACT:
  - Direct contradiction between:
      - Example specification (Sections 7 / 22),
      - The code,
      - The Master CRSS model that expects Level-A logic to live in Strict-A.
  - Could confuse auditors about which layer carries safety-critical voting logic.

RECOMMENDED FIX:
  1. Fix the ASCII block diagram (lines 279–287):

     - Change:
       - “Voting (Core-B)”
       - “Safety Envelope (Strict-A)”
     - To something like:
       - “Voting (Strict-A)”
       - “Safety Envelope (Strict-A)”

  2. Fix Section 22.2 (Core-B Responsibilities):

     - Remove voting-related bullets from Core-B:
       - `- computes median`
       - `- evaluates spread`
       - `- assigns disagreement severity`

     - Add those under Strict-A responsibilities (22.1), e.g.:

       Under 22.1 Strict-A implements:
         - TMR voting (median/plausibility/spread)
         - envelope clamp
         - rate limiting
         - SAFE_DEFAULT logic
         - status classification

     - Re-describe Core-B as:
         “Core-B orchestrators and deterministic helpers that are
          not on the Level-A critical path (offline step, TCP client,
          deterministic preprocessing if any).”


EX-ISSUE-03: “CRSS Profiles Used” header in compliance report uses old terminology
----------------------------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_compliance_report.md

LOCATION:
  Lines 6–10:
    6: - **CRSS Profiles Used**:
    7:   - Strict-A: safety controller (voting + envelope)
    8:   - Strict-B: config model, sensor interfaces
    9:   - Core-B: orchestrators (offline step, TCP client)
   10:   - Core-C: simulation, TCP server, logging, JSON I/O

ISSUE:
  - The list itself (Strict-A/B, Core-B/C) is correct and matches the code.
  - However, “Strict-A” and “Core-B” here are Mode names, not Profiles.
  - This is inconsistent with the CRSS definition:
      - Profile ∈ {Strict, Core}
      - Safety Level ∈ {A, B, C}
      - Mode name (e.g. “Strict-A”) combines the two.

IMPACT:
  - Terminology drift between:
      - Example compliance report,
      - Master CRSS model (“Mode”),
      - Mode metadata in `crss_modes/modes.py` and `scem/mar.yaml`.

RECOMMENDED FIX:
  - Update the header to be Mode-aware and clearer, e.g.:

    From:
      - **CRSS Profiles Used**:

    To:
      - **CRSS Modes Used (Profile + Safety Level)**:
        - Strict-A (Strict, Level A): safety controller (voting + envelope)
        - Strict-B (Strict, Level B): config model, sensor interfaces
        - Core-B (Core, Level B): orchestrators (offline step, TCP client)
        - Core-C (Core, Level C): simulation, TCP server, logging, JSON I/O


EX-ISSUE-04: Safety baseline evidence list points to non-existent filenames
---------------------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/scem/crss_sensor_voting_safety_baseline.md

LOCATION:
  Lines 46–50:
    46: ## 5. Evidence Summary
    48: - CRSS compliance report: `docs/crss_sensor_voting_compliance_report.md`
    49: - Coverage report: `reports/coverage_report.md`
    50: - Fault injection report: `reports/fault_injection_report.md`

ACTUAL FILES IN `reports/`:
  - `reports/crss_fault_injection_report.md`
  - `reports/Test coverage report.html`

ISSUE:
  - The baseline refers to `coverage_report.md` and `fault_injection_report.md`,
    which do not exist with those exact names.
  - The only Markdown report in the folder is `crss_fault_injection_report.md`,
    whose content is actually a coverage report, not a fault-injection report.
  - The HTML file looks like a coverage report export.

IMPACT:
  - Broken traceability:
      - Auditors following the baseline cannot find the referenced files.
  - Confusing labeling:
      - The “fault injection report” link actually leads to coverage content.

RECOMMENDED FIX:
  Option A (minimal rename):
  - Rename files and align them with the baseline:

    - Rename:
      - `reports/crss_fault_injection_report.md` → `reports/coverage_report.md`
    - Adjust baseline:
      - Coverage report: `reports/coverage_report.md`
      - Fault injection report: *(add a real FI report file or remove the line).*

  Option B (clean separation — recommended):
  1. Create two explicit Markdown reports:
     - `reports/coverage_report.md` (coverage details)
     - `reports/fault_injection_report.md` (test scenarios, FI cases, results)
  2. Move the current coverage content from `crss_fault_injection_report.md`
     into `coverage_report.md`.
  3. Use `crss_fault_injection_report.md` either as:
     - a redirect/stub that clearly says “see fault_injection_report.md”, or
     - remove it once not needed.
  4. Update lines 49–50 in the baseline to point to the new canonical filenames.


EX-ISSUE-05: Fault-injection vs coverage report title mismatch
--------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/reports/crss_fault_injection_report.md

LOCATION:
  Lines 1–2:
    1: # Coverage Report — Sensor Voting Reference Example
    2: ## 1. Tools

ISSUE:
  - The filename suggests a “fault injection report”, but the content is clearly
    a coverage report (coverage command, coverage tool, coverage HTML).
  - This conflicts with the safety baseline which expects a separate coverage
    report and a fault-injection report.

IMPACT:
  - Readers and auditors may misinterpret which artefact is which.
  - Traces from requirements → FI tests → FI report are obscured.

RECOMMENDED FIX:
  - Align the filename and title:
    - If this is coverage:
      - Rename the file to `coverage_report.md` and adjust the baseline (see EX-ISSUE-04).
    - If you want it to be fault-injection:
      - Change the title to “Fault Injection Report — …”
      - Replace or extend the content with fault-injection scenarios and results.
  - Ideally keep coverage and fault injection separate as per EX-ISSUE-04 Option B.


EX-ISSUE-06: Safety baseline “Safety Modes and Profiles” section could be clearer about Modes
---------------------------------------------------------------------------------------------
FILE:
  6-Examples/crss_example_sensor_voting_reference/scem/crss_sensor_voting_safety_baseline.md

LOCATION:
  Lines 19–35:
    19: ## 3. Safety Modes and Profiles
    21: - **Strict-A**:
    26: - **Strict-B**:
    29: - **Core-B**:
    33: - **Core-C**:

ISSUE:
  - The heading says “Safety Modes and Profiles” but then lists only Mode names
    (“Strict-A”, “Core-B”, etc.) without explicitly stating the underlying Profile
    + Safety Level mapping.
  - This is a minor terminology mismatch, not a logic error.

IMPACT:
  - Slightly reduces clarity for readers who just learned from the Master spec
    that “Strict-A” is a Mode = (Strict, Level A).

RECOMMENDED FIX:
  - Reword the section to make the Mode concept explicit, e.g.:

    - Change heading to:
        “## 3. CRSS Modes in Scope (Profile + Safety Level)”
    - Expand bullets, for example:
        - **Strict-A (Strict, Level A)**:
            - `safety_logic.voting`
            - `safety_logic.envelope`
            - `safety_logic.controller`
            - `actuator.interface`
        - **Strict-B (Strict, Level B)**:
            - `config.model`
            - `sensors.interfaces`
        - **Core-B (Core, Level B)**:
            - `app.main_loop`
            - `app.tcp_controller_client`
            - `config.loader`
        - **Core-C (Core, Level C)**:
            - `sensors.simulation`
            - `app.tcp_sensor_server`
            - `logging_utils.logger`
            - `io.json_protocol`


EX-ISSUE-07: Orchestrator layering vs CRSS inner-orchestrator concept
---------------------------------------------------------------------
FILES:
  - 6-Examples/crss_example_sensor_voting_reference/src/crss_example_sensor_voting/app/main_loop.py
  - 6-Examples/crss_example_sensor_voting_reference/src/crss_example_sensor_voting/app/tcp_controller_client.py
  - 6-Examples/crss_example_sensor_voting_reference/scem/mar.yaml
  - 6-Examples/crss_example_sensor_voting_reference/docs/crss_sensor_voting_compliance_report.md

LOCATIONS:
  - `app/main_loop.py`:
      Line 2:
        """Single-step orchestrator (non-critical) for offline runs and tests.
  - `app/tcp_controller_client.py`:
      Line 2:
        """TCP JSON client that runs the Strict-A controller.
  - `scem/mar.yaml`:
      Lines 17–21:
        17:   - name: crss_example_sensor_voting.config.loader
        18:     mode: Core-B
        19:   - name: crss_example_sensor_voting.app.main_loop
        20:     mode: Core-B
        21:   - name: crss_example_sensor_voting.app.tcp_controller_client
        22:     mode: Core-B
  - Compliance report:
      Line 9:
        - Core-B: orchestrators (offline step, TCP client)

CONTEXT:
  - The Master CRSS spec defines:
      - Outer Orchestrator: Core (handles I/O, frames, invokes Strict-B/A)
      - Inner Orchestrator: Strict-B, sequences validator + kernel (CRSS-Orch-2)

  - In this example:
      - Orchestrators (`main_loop`, `tcp_controller_client`) are Core-B.
      - There is no separate Strict-B “inner orchestrator” module; Strict-A logic is
        encapsulated directly in `SafetyController` plus its helpers.
      - Strict-B is used for config model and sensor interfaces only.

ISSUE:
  - The example is **architecturally valid and CRSS-compliant for the safety kernel**,
    but it does not demonstrate the full “Outer Core + Inner Strict-B orchestrator”
    pattern described in the Master spec’s reference architecture.
  - Readers might assume the example shows a full CRSS layering including a Strict-B
    inner orchestrator; instead it shows Core-B harnesses calling Strict-A directly.

IMPACT:
  - Potential confusion:
      - For people using this example as a template for a full deployment including
        inner orchestrators.
  - Not a logic bug in the code: Strict-A remains isolated and pure, and SCEM correctly
    marks orchestrators as non-critical Core-B.

RECOMMENDED FIX:
  Option A (clarify scope — simplest):
  - In the specs/compliance docs, explicitly state:

    - The example focuses on the **Strict-A kernel** and shows Core-B harness
      orchestrators for testing and offline runs.
    - The Strict-B “inner orchestrator” concept from the Master spec is **not**
      instantiated here; instead, the Strict-A controller encapsulates both validation
      and kernel responsibilities, with clear SCEM boundaries.

  - A suggested sentence in the reference spec / compliance report:
    “This example covers a CRSS-compliant Strict-A safety kernel plus non-critical
     Core-B/Core-C harnesses. The Strict-B inner orchestrator described in the Master
     standard is not modeled as a separate module here; projects needing a full
     CRSS pipeline should add a Strict-B inner orchestrator that sequences validators
     and kernel functions.”

  Option B (extend the example — more work, but ideal):
  - Introduce a new module, e.g. `safety_logic.orchestrator` (mode: Strict-B), that:
      - Accepts normalized sensor values and config.
      - Calls Strict-A validator(s) and kernel in the correct order.
  - Have Core-B apps (`main_loop`, `tcp_controller_client`) call this Strict-B
    inner orchestrator instead of `SafetyController` directly.
  - Update `scem/mar.yaml` and docs to show the full Outer(Core)→Inner(Strict-B)→Strict-A chain.


EX-ISSUE-08: Overall CRSS compliance status of the example
----------------------------------------------------------
FILES AFFECTED:
  - All core example code under:
      6-Examples/crss_example_sensor_voting_reference/src/crss_example_sensor_voting/
  - SCEM artefacts under:
      6-Examples/crss_example_sensor_voting_reference/scem/

SUMMARY (NOT A DEFECT, JUST A STATEMENT OF STATUS):
  - CRSS Mode & Phase usage in the example is consistent with the redesigned CRSS model:
      - Strict-A: `safety_logic.controller`, `safety_logic.voting`, `safety_logic.envelope`,
        `actuator.interface` (critical-phase functions decorated with `@critical_phase`).
      - Strict-B: `config.model`, `sensors.interfaces` (pure data/typing, no I/O).
      - Core-B: `app.main_loop`, `app.tcp_controller_client`, `config.loader`
        (non-critical orchestrators, GC control, config loading from Strict-B model).
      - Core-C: `sensors.simulation`, `io.json_protocol`, `logging_utils.logger`,
        `app.tcp_sensor_server` (I/O, randomness, JSON/TCP, logging, simulation).
  - Strict-A modules:
      - No imports of logging, socket, random, I/O, or OS APIs.
      - Pure numeric logic only; all I/O is properly confined to Core-* modules.
  - SCEM (`mar.yaml`, `deps.yaml`, `cbd.yaml`) matches the actual import/call structure.
  - Phase markers (`critical_phase`, `non_critical_phase`) are semantics-preserving,
    and tests verify that they do not alter behavior.

IMPACT:
  - No code-level CRSS violations were found in the example kernel; all issues above
    are about documentation/terminology/evidence clarity.
  - Once the listed documentation fixes are applied, the example will be a very clean,
    fully-aligned reference for the updated CRSS standard.
