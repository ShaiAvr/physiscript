# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import inspect
from importlib import import_module
from pathlib import Path

import jinja2
from sphinx.application import Sphinx

import physiscript
from physiscript.utils import Color

REPO_DIR = Path(__file__).resolve().parent.parent.parent
CODE_URL = physiscript.REPOSITORY
if CODE_URL.endswith("/"):
    CODE_URL = CODE_URL[:-1]

project = "physiscript"
author = "Shai Avraham"
copyright = f"2023, {author}"  # noqa: A001
release = physiscript.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "autoapi.extension",
    "sphinx_toolbox.source",
    "notfound.extension",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": physiscript.REPOSITORY,
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
}
html_context = {
    "default_colors": {name: Color.get(name) for name in Color.names()},
}


def rst_jinja(app: Sphinx, _: str, source: list[str]) -> None:
    """Render our pages as a jinja template for fancy templating goodness."""
    # Make sure we're outputting HTML
    if app.builder.format != "html":
        return
    src = source[0]
    rendered = app.builder.templates.render_string(src, app.config.html_context)
    source[0] = rendered


def setup(app: Sphinx) -> None:
    app.connect("source-read", rst_jinja)


# linkcode settings
def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    if domain != "py":
        return None
    try:
        mod = import_module(info["module"])
    except ModuleNotFoundError:
        return None
    fullname = info["fullname"]
    obj = mod
    for part in fullname.split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None

    try:
        filepath = (
            Path(inspect.getsourcefile(obj)).resolve().relative_to(REPO_DIR).as_posix()
        )
        source, line_start = inspect.getsourcelines(obj)
        line_end = line_start + len(source) - 1
    except Exception:
        return None

    return f"{CODE_URL}/blob/master/{filepath}#L{line_start}-L{line_end}"


# intersphinx settings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# sphinx_toolbox settings
# sphinx_toolbox.github
github_username = "ShaiAvr"
github_repository = physiscript.REPOSITORY

# sphinx_toolbox.source
source_link_target = "GitHub"

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_attr_annotations = True

# sphinx_copybutton config
copybutton_exclude = ".linenos, .gp, .go"

# autoapi and autodoc config
autodoc_typehints = "both"
autoapi_dirs = ["../../src"]
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "undoc-members",
]
autoapi_template_dir = "_templates/autoapi"

physiscript_aliases_map = {
    "physiscript.App": "physiscript.app.App",
}


def _resolve_alias(text: str) -> str:
    return physiscript_aliases_map.get(text, text)


def autoapi_prepare_jinja_env(jinja_env: jinja2.Environment) -> None:
    jinja_env.filters["resolve_alias"] = _resolve_alias
