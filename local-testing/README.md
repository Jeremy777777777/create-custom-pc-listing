# Anaconda / Jupyter Listing testing

Use the dedicated `listing-testing` environment (Python 3.12) for programmable Listing text, workbook and image checks. [Workflow preference and scope](../references/python-jupyter-testing.md). This directory contains reproducible setup and reusable tests, not an uploaded Python installation.

## Setup

From the repository root, with your local `conda` available:

```sh
conda env create -f local-testing/environment.yml
conda run -n listing-testing python -m ipykernel install --user --name listing-testing --display-name "Python (Listing Testing)"
conda run -n listing-testing python -X utf8 local-testing/check-environment.py
```

Inspect an existing environment before creating/changing it. Do not overwrite `base` or change global PATH. If `conda` is not on PATH, use its actual executable path; the confirmed Windows installation is documented in the workflow preference. Environment/kernel access outside the workspace may require permission.

The environment covers Pillow/openpyxl, YAML validation, pytest, JupyterLab and headless Notebook execution. `environment.yml` and `requirements.txt` describe supported ranges. [installed-versions.txt](installed-versions.txt) records the direct versions tested on the user's machine, not a complete transitive/cross-platform lock. Current repository dependency requirements take precedence; report conflicts before changing the environment.

## Notebook debugging

In existing Jupyter, select **Python (Listing Testing)** for [smoke-test.ipynb](smoke-test.ipynb) and future Listing notebooks. The smoke test verifies interpreter/package identity, YAML parsing, an in-memory 2000px PNG and an in-memory Excel round trip without modifying product assets.

[check-environment.py](check-environment.py) executes this Notebook headlessly and checks dependency/kernel compatibility. No Jupyter server needs to stay open. To start JupyterLab manually:

```sh
conda run --no-capture-output -n listing-testing python -m jupyterlab
```

Keep servers local and authenticated. Do not upload credentials, private source records, environment binaries, local kernelspecs or unreviewed Notebook outputs.

## Repository checks

Windows PowerShell, from the repository root:

```powershell
./local-testing/run-listing-tests.ps1 -GalleryGate
```

The runner defaults to this checkout, resolves the dedicated environment from `LISTING_PYTHON`, an active `listing-testing` environment or the local user's conventional Anaconda location, and verifies the interpreter. For a nonstandard install pass `-PythonPath <actual interpreter>`. For another checkout pass `-RepoPath <actual checkout>`. It fails on the first failed check and never silently falls back to another Python.

Portable equivalents:

```sh
conda run -n listing-testing python -X utf8 -m unittest discover -s scripts/tests -v
conda run -n listing-testing python -X utf8 scripts/check-workbooks.py --directory .
conda run -n listing-testing python -X utf8 scripts/gallery_engine.py gate --directory .
```

For revision-scoped gallery checks pass both `-Base <commit> -Head <commit>` to the PowerShell runner with `-GalleryGate`, or `--base <commit> --head <commit>` to the gallery command. Workbook/gallery checkers may write normal summary JSON in the checkout; they do not rewrite canonical product assets. Quarantined galleries remain excluded, not PASS.

Choose additional checks that match the requested content, such as current title length, warranty/bullet structure, base configuration or actual image readability. Unit/structure checks and environment smoke tests do not verify hardware claims, source rights, visual quality or Amazon eligibility. Existing GitHub CI stays isolated and does not need to access the user's Anaconda installation.
