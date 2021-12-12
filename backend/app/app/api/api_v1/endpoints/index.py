from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from pathlib import Path
from markdown import markdown
from app.core.config import settings

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    summary="Index page view",
    description="Generate an HTML page based on the contents of the README file")
async def index_page() -> HTMLResponse:
    readme = Path("/app/README.md")
    try:
        with (open(readme, "r", encoding="utf-8")) as f:
            md = f.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find file README.md: %s" % str(e)
        )
    content: str = (
        "<!DOCTYPE html>\n"
        "<html>"
        "<head>"
        f"<title>{settings.PROJECT_NAME}</title>"
        "</head>"
        "<body>"
        f"{markdown(md)}"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=content, status_code=200)
