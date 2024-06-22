from nbconvert import HTMLExporter
from nbformat.v4 import to_notebook
from sanitize_html import sanitize
from bs4 import BeautifulSoup


def convert(notebook_json):
    # get a NotebookNode object that nbconvert can use
    notebook = to_notebook(notebook_json)

    # convert the notebook to HTML
    html_exporter = HTMLExporter()
    (notebook_html, resources_dict) = html_exporter.from_notebook_node(notebook)
    soup = BeautifulSoup(notebook_html, 'html.parser')
    body_tag = soup.body

    # temporarily swap body tag for a safe tagname
    body_tag.name = "div"

    body_html = str(body_tag)
    safe_body_html = sanitize(body_html)
    safe_body_soup = BeautifulSoup(safe_body_html, "html.parser")

    # swap tagname back
    safe_body_soup.div.name = "body"

    body_tag.replace_with(safe_body_soup.body)

    safe_html = str(soup)
    return safe_html
