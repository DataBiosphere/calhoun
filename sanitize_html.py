from nh3 import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, clean


safe_tags = ALLOWED_TAGS

unsafe_tags = set(["script", "style"])

safe_attributes = ALLOWED_ATTRIBUTES

safe_schemes = set(["http", "https"])


def sanitize(html: str):
    if not html:
        return None

    # see https://nh3.readthedocs.io/en/stable/index.html#module-nh3
    return clean(
        html=html,
        tags=safe_tags,
        clean_content_tags=unsafe_tags,
        attributes=safe_attributes,
        strip_comments=True,
        link_rel="noopener noreferrer",
        url_schemes=safe_schemes
    )
