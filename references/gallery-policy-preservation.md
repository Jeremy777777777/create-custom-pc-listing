# Preserve unchanged historical gallery reviews across policy updates

A new catalog decision must not silently renew old reviews or force unrelated image replacement. Revision-scoped gallery checks may verify unchanged galleries against the trusted base commit's recorded policy and report `historicalPriorPolicyGalleriesNotCurrent`. They do not count these galleries as new full-gallery/current-policy PASS and never rewrite their product files, images, status or review records.

The preservation path requires a trusted base, the exact same complete product inventory and bytes (text line-ending normalization only), unchanged recipe bytes, matching visual/semantic input bindings calculated from that base's policy files, and the existing full file/hash/geometry/evidence checks. A pre-ledger binding is explicitly reported as research-unbound. Changed/new/deleted images, facts, reviews, recipes or product files cannot use this route. Failed geometry, hashes, source assets or malformed evidence remain failures. Ordinary full scans without a base and `accept` still require current policy-bound review.

This supports the 2026-10-20 desktop/AIO keyboard-and-mouse decision without relabelling untouched old laptop galleries. Future modification of a historical gallery requires the current rules and fresh actual review for the requested scope. Publication readiness is independent.
