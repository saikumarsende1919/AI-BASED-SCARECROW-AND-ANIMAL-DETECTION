import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        try:
            ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
            print("Notebook ran successfully.")
        except Exception as e:
            print(f"Error executing the notebook: {e}")

if __name__ == "__main__":
    run_notebook("3.ipynb")
