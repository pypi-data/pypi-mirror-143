pip install wheel twine\
\
twine check *\
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*\
pip install uniphi

