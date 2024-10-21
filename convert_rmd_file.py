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

    # Convert to HTML
    raw_html = _to_html(raw_rmd)

    # Remove unsafe HTML
    safe_html = sanitize_body(raw_html)

    return safe_html


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
        # Set eval = FALSE to prevent code execution.
        rmd = importr('rmarkdown')
        output_format = rmd.output_format(knitr = rmd.knitr_options(opts_chunk = "set(eval = FALSE)"), 
                                          pandoc = rmd.pandoc_options(to = "html"))
        rendered_html = rmd.render(in_file.name, output_format = output_format)
        out_path = rendered_html[0]

        try:
            out_file = open(out_path)
            read_outfile = out_file.read()
        finally:
            out_file.close()
            os.remove(out_path)
        return read_outfile
