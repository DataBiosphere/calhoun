"""Sanitize raw HTML strings, removing unsafe code suitable for display on user browsers."""

from bs4 import BeautifulSoup
from copy import deepcopy
from nh3 import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, clean


safe_attributes = set(["class"])
"""Attributes to support on any tag, beyond the nh3 defaults."""

safe_schemes = set(["http", "https", "data"])
"""Valid schemes for URLs in the `src` and `href` attributes."""

safe_tags = ALLOWED_TAGS
"""Valid tagnames."""

unsafe_tags = set(["script", "style"])
"""Tagnames to strip and remove all content within."""


def sanitize_body(html: str) -> str:
    """Sanitize only the contents of the <body> tag. Returns an HTML string."""
    # Get the body
    soup = BeautifulSoup(html, 'html.parser')
    body_tag = soup.body

    # Swap body tag for a safe tagname. Sanitizer will strip <body> tags as unsafe, so we preserve the location of the outermost body tag, and its attributes.
    body_tag.name = "div"

    body_html = str(body_tag)
    safe_body_html = sanitize(body_html)
    safe_body_soup = BeautifulSoup(safe_body_html, "html.parser")

    # Swap tagname back to <body>. This approach leaves other attributes of the body tag intact.
    safe_body_soup.div.name = "body"

    # Inject sanitized <body>
    body_tag.replace_with(safe_body_soup.body)

    safe_html = str(soup)
    return safe_html


def sanitize(html: str) -> str:
    """Remove unsafe tags and attributes from raw HTML. Returns an HTML string."""
    if not html:
        return None

    # see https://nh3.readthedocs.io/en/stable/index.html#module-nh3
    safe_html = clean(
        html=html,
        tags=safe_tags,
        clean_content_tags=unsafe_tags,
        attributes=_get_safe_attributes(),
        strip_comments=True,
        link_rel="noopener noreferrer",
        url_schemes=safe_schemes
    )

    return safe_html


def _get_safe_attributes() -> dict[str, set]:
    """A dict of HTML tagnames to the valid attributes they support."""
    attributes = deepcopy(ALLOWED_ATTRIBUTES)
    for tag in safe_tags:
        if tag in attributes:
            attributes[tag] = attributes[tag] | safe_attributes
        else:
            attributes[tag] = safe_attributes
    return attributes
