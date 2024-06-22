from nh3 import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, clean
from copy import deepcopy


safe_attributes = set(["class"])

safe_schemes = set(["http", "https", "data"])

safe_tags = ALLOWED_TAGS

unsafe_tags = set(["script", "style"])


def sanitize(html: str):
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


def _get_safe_attributes():
    attributes = deepcopy(ALLOWED_ATTRIBUTES)
    for tag in safe_tags:
        if tag in attributes:
            attributes[tag] = attributes[tag] | safe_attributes
        else:
            attributes[tag] = safe_attributes
    return attributes
