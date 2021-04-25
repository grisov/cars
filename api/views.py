from flask import Markup, render_template
from markdown import markdown
from pathlib import Path
from api import app, logger


@app.route('/')  # type: ignore
def index():
    """Generate and render index page."""
    readme = Path(__file__).parent.parent.joinpath("readme.md")
    content: str = ""
    try:
        with (open(readme, "r", encoding="utf-8")) as f:
            content = f.read()
    except Exception as e:
        logger.error("Unable to read the ReadMe file: %s", e)
    content = Markup(markdown(content))
    return render_template(
        "index.html",
        title="Simple REST API for Yalantis",
        content=content or "No Content"
    )
