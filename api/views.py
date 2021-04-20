from flask import render_template
from api import app


@app.route('/')
def index():
    readme = "ASD"
    return render_template("index.html",
        title="Simple REST API for Yalantis",
        context={'content': readme})
