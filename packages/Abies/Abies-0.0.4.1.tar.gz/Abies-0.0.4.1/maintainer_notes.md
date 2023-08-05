## Build project
python -m build

## Publish to pypi.org
twine upload dist/*.tar.gz --skip-existing
