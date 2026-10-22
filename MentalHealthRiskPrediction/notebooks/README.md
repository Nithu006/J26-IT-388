# Planned experiment notebooks

`nbformat` is not installed in the available Python runtime. Per the requested
fallback, the six notebook files were not created. No experiment was executed.

After review, run these commands in a project virtual environment to create valid
starter notebooks (this dependency is small and does not download models):

```powershell
python -m pip install nbformat==5.10.4
@'
from pathlib import Path
import nbformat
names = [
    "01_dataset_exploration", "02_data_preprocessing",
    "03_text_feature_extraction", "04_behavioral_feature_analysis",
    "05_hybrid_model_experiments", "06_model_evaluation",
]
for name in names:
    path = Path("notebooks") / (name + ".ipynb")
    if path.exists():
        continue
    book = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_markdown_cell(
            "# " + name.replace("_", " ") +
            "\n\nPending approved data and contracts. No research results."
        ),
        nbformat.v4.new_code_cell("# Add approved experiment after review.")
    ])
    nbformat.validate(book)
    nbformat.write(book, path)
'@ | python -
```

Run from the workspace root. The command preserves existing notebooks. Review dataset
permissions and label definitions before adding data; clear sensitive outputs before
sharing notebooks. VS Code notebook execution also needs a reviewed Jupyter/kernel setup.
