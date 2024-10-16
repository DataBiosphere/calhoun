"""HTML converter for .rmd files."""

from rpy2.robjects.packages import importr
from tempfile import NamedTemporaryFile
import logging
import os

from sanitize_html import sanitize_body


def to_safe_html(stream: bytes) -> str:
    """Convert an RMarkdown bytestream (.rmd) to HTML with potentially dangerous code removed.

    Returns:
        HTML string safe for browser display.
    """
    binary_data = stream.read()
    raw_rmd = binary_data.decode('ascii')

    # # Remove executable code blocks
    # safe_rmd = _sanitize_rmd(raw_rmd)

    # Convert to HTML
    raw_html = _to_html(raw_rmd)

    # Remove unsafe HTML
    safe_html = sanitize_body(raw_html)

    return safe_html


# def _sanitize_rmd(data: str) -> bytes:
#     """Strip code blocks (ex ```{bash}) from .rmd string.
#
#     When rendering, knitr (https://rmarkdown.rstudio.com/authoring_quick_tour.html#Rendering_Output) executes all code in these blocks.
#     Running arbitrary user code on the Calhoun server would leave us exposed to attack.
#     For details, see https://docs.google.com/document/d/1aNCOKitTJH-GEkBSR4i-x91O0OQCZ8ZYa3feXtkja94/edit#heading=h.rvpr6zoz0jem
#
#     Returns:
#         bytestring of .rmd without executable code blocks.
#     """
#
#     dont_run_code_block = '`r knitr::opts_chunk$set(eval = FALSE)`'
#     file = dont_run_code_block + data
#
#     return file.encode('ascii')


def _to_html(data: bytes) -> str:
    """Convert a .rmd file to raw HTML using RMarkdown.

    Returns:
        HTML string.
    """
    # The rmarkdown converter unfortunately only works with files.
    # So we create temp files for the source markdown and destination html data.
    # The temp files are deleted as soon as the below with block ends.
    with NamedTemporaryFile(suffix='.Rmd') as in_file:
        in_file.write(data)
        in_file.seek(0)

        # Call R rmarkdown package from python.
        # See https://cran.r-project.org/web/packages/rmarkdown/index.html
        rmd = importr('rmarkdown')
        rendered_html = rmd.render(in_file.name, knitr_meta={'eval': False})
        out_path = rendered_html[0]

        try:
            out_file = open(out_path)
            read_outfile = out_file.read()
        finally:
            out_file.close()
            os.remove(out_path)
        return read_outfile
