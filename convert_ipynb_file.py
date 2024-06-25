"""HTML converter for .ipynb files."""

from nbconvert import HTMLExporter
from nbconvert.preprocessors import ClearMetadataPreprocessor
from nbformat.v4 import to_notebook

from sanitize_html import sanitize_body


def to_safe_html(notebook_json: dict[str, any]) -> str:
    """Convert a JSON Jupyter notebook (.ipynb) to HTML with potentially dangerous code removed.

    Returns:
        HTML string safe for browser display.
    """
    # get a NotebookNode object that nbconvert can use
    notebook = to_notebook(notebook_json)

    # strips notebook metadata to remove Jupyter widgets, which inject scripts into the html <head>
    preprocessor = ClearMetadataPreprocessor(enabled=True, clear_cell_metadata=False)

    # export notebook to HTML
    html_exporter = HTMLExporter()
    html_exporter.register_preprocessor(ClearMetadataPreprocessor, enabled=True)
    (notebook_html, _) = html_exporter.from_notebook_node(notebook)

    safe_html = sanitize_body(notebook_html)
    return safe_html
