from flask import Markup, render_template
from markdown import markdown
from api import app, logger


@app.route('/')  # type: ignore
def index():
    """Generate and render index page."""
    try:
        with (open(r"readme.md", "r", encoding="utf-8")) as f:
            content = f.read()
    except Exception as e:
        logger.error("Unable to read the ReadMe file: %s", e)
    content = Markup(markdown(content))
    return render_template(
        "index.html",
        title="Simple REST API for Yalantis",
        content=content or "No Content"
    )
