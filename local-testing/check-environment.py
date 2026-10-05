"""Execute the Listing smoke notebook in memory using its registered kernel."""
import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager


def main():
    if Path(sys.prefix).name != "listing-testing" or sys.version_info[:2] != (3, 12):
        raise RuntimeError(f"Use the Listing Python 3.12 interpreter, not {sys.executable}")
    subprocess.run([sys.executable, "-m", "pip", "check"], check=True)
    spec = KernelSpecManager().get_kernel_spec("listing-testing")
    if Path(spec.argv[0]).resolve() != Path(sys.executable).resolve():
        raise RuntimeError(f"Kernel points to another interpreter: {spec.argv[0]}")
    source = Path(__file__).with_name("smoke-test.ipynb")
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(notebook, timeout=120, kernel_name="listing-testing").execute()
    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                print(output.text, end="")
    print("PASS: registered Jupyter kernel executed the smoke notebook; no product files changed")


if __name__ == "__main__":
    main()
