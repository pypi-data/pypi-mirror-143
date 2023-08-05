## Build project
python -m build

## Publish to pypi.org
python -m twine upload dist/*.tar.gz
