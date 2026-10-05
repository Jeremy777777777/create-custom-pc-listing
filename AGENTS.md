# Listing development and testing

Read [SKILL.md](SKILL.md) and the applicable current references before changing Listing text, workbooks, images or workflow rules.

For all Listing modes, the user prefers the dedicated Anaconda `listing-testing` Python 3.12 environment and Jupyter kernel `listing-testing` (**Python (Listing Testing)**). Read [Python/Jupyter testing](references/python-jupyter-testing.md) before programmable generation, inspection or testing. Use that environment for relevant copy/workbook/image checks and reproducible Notebook debugging. Direct Python execution in the same environment is supported; an always-open Jupyter server is not required.

Check the selected interpreter; if unavailable, report the missing environment and follow the documented setup with appropriate permission. Do not silently use WindowsApps Python, change `base`/global PATH or bypass existing product facts, style approval, manual QA and delivery gates. Tests do not establish Amazon eligibility. Keep experiments outside canonical product output and do not upload credentials, local kernelspecs, environment binaries or private Notebook outputs.
