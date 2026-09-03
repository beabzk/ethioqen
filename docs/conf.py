import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ethioqen'
copyright = '2024-2026, Beabfekad Zikie'
author = 'Beabfekad Zikie'
try:
    from importlib.metadata import version as _pkg_version
    release = _pkg_version('ethioqen')
except Exception:
    import tomllib
    with open(os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml'), 'rb') as f:
        release = tomllib.load(f)['project']['version']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']