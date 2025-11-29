✔️ Final CRSS Scope Categories (Only 4 Allowed)
1. scope: critical

Rule applies ONLY inside:

functions annotated @critical, OR

MAR-designated critical units.

Meaning:

The rule is not applied to non-critical code.

The rule prohibits behaviors that break determinism.

Used for:

I/O bans

blocking bans

allocation/GC bans

subprocess bans

timing/entropy/bad randomness

env-dependent behavior

2. scope: non_critical

Rule applies ONLY to non-critical code.

Used extremely rarely — only when:

something is allowed in non-critical code

but forbidden in critical code

AND you need to enforce additional constraints on non-critical regions.

Examples:

Rich logging

Debug instrumentation

Heavy telemetry

Non-critical scope DOES NOT mean “rules are relaxed.”
Strict MUST-NOT rules still apply globally unless otherwise stated.

3. scope: all_code

Rule applies universally:

critical

non_critical

core

strict

all levels

Used for:

security rules

authorization rules

secrets / credentials

sensitive data handling

input validation

parser safety

memory bounds

global state

versioning

deployment integrity

architecture constraints

SCEM / evidence rules

testing obligations

No exceptions.
Critical code must follow these too.

4. scope: all_code (phase-aware) — ★ IMPORTANT ★

This is the one you asked to be explained perfectly.

✔ Meaning:

It applies to all units, but the enforcement is different depending on the phase:

In @critical

The rule is enforced with maximum strictness.

Forbidden constructs → MUST-NOT

Allowed constructs → severely constrained

In non-critical

The rule still applies

But with a more permissive form

Non-critical may perform additional actions not allowed in critical

Still MUST respect safety constraints

Still MUST respect all Core/Strict MUST/MUST-NOT

✔ Why this scope exists:

Some rules:

are relevant to all code,

but require stricter interpretation inside critical.

Examples include:

memory bounds

caching constraints

serializer/decoder safety

network robustness rules (not I/O bans, but retry/backoff)

bounded data formats

safe collection growth rules

These are NOT pure deterministic bans, but they STILL require strict handling in critical zones.

✔ Example:

Rule: “Caches must be bounded.”

In non-critical:
→ MAY allocate cache entries if bounded.

In critical:
→ MUST NOT allocate cache entries; may only read.

Thus:
scope: all_code (phase-aware)

❗ Final Confirmation Required Before I Rewrite the Entire Core Spec

Please reply with:

“Confirmed — use these 4 scope categories.”

Once you confirm:

✔ I will rewrite the entire Core spec
✔ Assign the correct scope for EVERY rule
✔ Add small explicit explanatory notes where needed
✔ Keep every rule ID exactly unchanged
✔ Regenerate a fully polished, downloadable Markdown file
✔ Then proceed to the Strict spec afterward

Please confirm:
“Confirmed — use these 4 scope categories.”