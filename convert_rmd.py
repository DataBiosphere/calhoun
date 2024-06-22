import logging
import os
from sanitize_html import sanitize
from tempfile import NamedTemporaryFile
from rpy2.robjects.packages import importr
from bs4 import BeautifulSoup


def convert(stream):
    binary_data = stream.read()
    raw_rmd = binary_data.decode('ascii')

    safe_rmd = _sanitize_rmd(raw_rmd)
    raw_html = _to_html(safe_rmd)

    soup = BeautifulSoup(raw_html, 'html.parser')
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



def _sanitize_rmd(data: str) -> bytes:
    """
    Strip code blocks (ex ```{bash}) from the rmd before rendering it.
    When rendering, kitr (https://rmarkdown.rstudio.com/authoring_quick_tour.html#Rendering_Output) executes all code in these blocks.
    Running arbitrary user code on the Calhoun server would leave us exposed to attack.
    For details, see https://docs.google.com/document/d/1aNCOKitTJH-GEkBSR4i-x91O0OQCZ8ZYa3feXtkja94/edit#heading=h.rvpr6zoz0jem
    """
    lines = data.split('\n')
    sanitized_file = []
    for line in lines:
        if line.startswith('```'):
            sanitized_line = '```'
        else:
            sanitized_line = line
        sanitized_file.append(sanitized_line)

    file = '\n'.join(sanitized_file)
    return file.encode('ascii')


def _to_html(data: bytes):
    # The rmarkdown converter unfortunately only works with files.
    # So we create temp files for the source markdown and destination html data.
    # The temp files are deleted as soon as the below with block ends.
    with NamedTemporaryFile(suffix=".Rmd") as in_file:
        in_file.write(data)
        in_file.seek(0)

        # Call R rmarkdown package from python.
        # See https://cran.r-project.org/web/packages/rmarkdown/index.html
        rmd = importr("rmarkdown")
        rendered_html = rmd.render(in_file.name)
        out_path = rendered_html[0]

        try:
            out_file = open(out_path)
            read_outfile = out_file.read()
        finally:
            out_file.close()
            os.remove(out_path)
        return read_outfile
