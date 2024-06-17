from nbconvert import HTMLExporter
from nbformat.v4 import to_notebook
from sanitize_html import sanitize


def convert(notebook_json):
    # get a NotebookNode object that nbconvert can use
    notebook = to_notebook(notebook_json)

    # convert the notebook to HTML
    html_exporter = HTMLExporter()
    (notebook_html, resources_dict) = html_exporter.from_notebook_node(notebook)

    # remove any unsafe HTML
    safe_html = sanitize(notebook_html)
    return safe_html
