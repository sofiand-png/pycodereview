**Version:** v1.0.0
**Status:** Informative
**Maturity:** Stable
© 2025 Sofian Daghsen – All rights reserved
Distributed under CC BY-NC-ND 4.0 — see LICENSE-CRSS.

**Note:** The structure in this template is Informative. 
The normative CBM content requirements are defined in the Deployment Master and Release Management specifications.

---

cbm_version: "1.0.0"
baseline_id: "BASELINE-XXXX"
release_id: "RELEASE-XXXX"
commit_hash: "xxxxxxxxxxxxxxxxxxxx"

# 1. Requirements

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Source Code](#2-source-code)
- [3. Python Interpreter](#3-python-interpreter)
- [4. Dependencies](#4-dependencies)
- [5. Operating System](#5-operating-system)
- [6. Container/VM Image (if applicable)](#6-containervm-image-if-applicable)
- [7. Hardware Platform](#7-hardware-platform)
- [8. Build Configuration](#8-build-configuration)
- [9. Database / External State (if applicable)](#9-database-external-state-if-applicable)
- [10. Test Context](#10-test-context)
- [11. Linked Artifacts (Mandatory)](#11-linked-artifacts-mandatory)
- [12. Integrity](#12-integrity)

requirements:
  requirements_version: "REQ-SET-1.2.3"
  criticality_level: "A|B|C"
  safety_level: "ASIL/SIL/Class"
  mapping_document: "rtm_vX.Y.Z.pdf"

# 2. Source Code
source:
  repository_url: "https://..."
  branch: "main"
  commit_hash: "xxxxxxxxxxxx"
  signed: true

# 3. Python Interpreter
interpreter:
  implementation: "CPython"
  version: "3.10.8"
  build_flags:
    - "Py_DEBUG=0"
    - "WITH_PYMALLOC=1"
  distribution: "Ubuntu package / custom / vendor"

# 4. Dependencies
dependencies:
  manifest_file: "requirements.txt"
  packages:
    - name: "numpy"
      version: "1.24.2"
      checksum: "sha256:..."
    - name: "..."
  private_repository: "Nexus URL"
  lockfile: "requirements.lock"
  no_floating_versions: true

# 5. Operating System
os:
  name: "Ubuntu"
  version: "22.04.3"
  kernel: "5.15.0-89-generic"
  configs:
    sysctl:
      - "vm.swappiness=0"
      - "kernel.sched_autogroup_enabled=0"

# 6. Container/VM Image (if applicable)
runtime_image:
  image_name: "crss_runtime_1.0.0"
  image_digest: "sha256:..."
  base_image: "ubuntu:22.04"
  frozen: true

# 7. Hardware Platform
hardware:
  cpu_model: "Intel Xeon XYZ"
  cpu_speed_ghz: 3.0
  ram_gb: 16
  disk_type: "NVMe SSD"
  network_latency_ms_max: 10

# 8. Build Configuration
build:
  tool_versions:
    pip: "24.0"
    build_system: "setuptools 65.0"
  build_commands:
    - "pip install -r requirements.lock"
    - "python -OO build.py"
  environment_variables:
    - "CRSS_MODE=STRICT"
  hashes:
    source_archive: "sha256:..."
    build_artifact: "sha256:..."

# 9. Database / External State (if applicable)
data_sources:
  schema_version: "schema_1.3.0"
  initial_data_checksum: "sha256:..."

# 10. Test Context
testing:
  test_suite_version: "TEST-2.1"
  coverage_report: "coverage.html"
  mcdc_report: "mcdc.html"
  platform_matrix: "matrix.json"
  fault_injection_logs: ["fault1.log", "fault2.log"]

# 11. Linked Artifacts (Mandatory)
artifacts:
  rcr: "rcr_v1.2.pdf"
  tep: "tep_v3.0.zip"
  sbr: "sbr_v1.0.pdf"
  cc: "cc_v1.0.pdf"

# 12. Integrity
signatures:
  generated_by: "Name / Org"
  verified_by: "Independent Authority"
  timestamp: "YYYY-MM-DD"
  hash_of_this_document: "sha256:..."
