import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ethioqen'
copyright = '2024, Beabfekad Zikie'
author = 'Beabfekad Zikie'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']