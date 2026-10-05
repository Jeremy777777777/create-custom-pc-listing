# Listing Python / Jupyter preference — 2026-10-05

The user requested that the reusable local Anaconda/Jupyter setup be recorded in GitHub so future Listing text, workbook and image work reuses it. This is a tooling preference, not a replacement of catalog facts, style approval, visual QA or delivery rules.

## Select the environment

- Conda environment: `listing-testing`, Python 3.12 (matching the repository CI Python minor version).
- Jupyter kernel: `listing-testing`, displayed as **Python (Listing Testing)**.
- Confirmed interpreter on the user's current Windows computer: `C:/Users/jerem/anaconda3/envs/listing-testing/python.exe`.
- On another machine, resolve the same named environment locally; never assume the Windows path exists. [Setup and commands](../local-testing/README.md), [environment specification](../local-testing/environment.yml).

At the start of a Listing run, select and verify the intended interpreter before programmable work. Prefer this environment for scripts and Notebook execution. Use Jupyter for exploratory debugging when useful; direct execution in that same environment is appropriate for repeatable tests. No persistent browser or server is required. If the environment/kernel is missing or incompatible, report it and obtain any required installation/access permission; do not silently switch to `base`, WindowsApps or another runtime. User-approved alternative runtimes and cloud CI remain possible when this local environment is unavailable.

## Apply checks to the requested scope

- **Text and Excel:** inspect generated title length, base configuration, bullet structure, required warranty text, worksheet mappings and current workbook structure against the active rules. Python can find structural inconsistencies; it cannot verify an unsupported product claim. Use existing validators where available and write narrowly scoped checks for the actual copy when needed.
- **Images:** use Pillow and the current gallery scripts for decoded dimensions/formats, hashes, masks/layout measurements, slot completeness and current-byte evidence. Review actual output separately for geometry, facts, spelling, style and source rights. This preference does not authorize Python to replace the required image-generation tool for AI image editing.
- **Workflow changes:** run the repository unit tests, relevant workbook/gallery checks and skill validation where applicable. Do not claim Notebook smoke tests alone validate Listing content.

After environment creation/change, or when troubleshooting the kernel, run [check-environment.py](../local-testing/check-environment.py). It checks package compatibility, interpreter/kernel identity and executes [smoke-test.ipynb](../local-testing/smoke-test.ipynb) in memory. For ordinary unchanged runs, a lightweight interpreter/import check is enough; do not run unrelated Notebook experiments for every copy edit.

Use [run-listing-tests.ps1](../local-testing/run-listing-tests.ps1) for the current Windows checkout or the portable commands in the setup guide. Revision-scoped gallery checks take both base and head. Existing CI uses its isolated Python runtime; it does not call the user's computer or require Anaconda/Jupyter on the GitHub runner.

Keep diagnostic notebooks/outputs in a scratch directory outside canonical product slots. Publish only intentionally reviewed reusable notebooks without private source data, credentials or output leakage. Do not upload environment binaries/cache or machine-generated kernelspecs. No testing utility changes the existing GitHub-delivery or per-product style-approval contract.
