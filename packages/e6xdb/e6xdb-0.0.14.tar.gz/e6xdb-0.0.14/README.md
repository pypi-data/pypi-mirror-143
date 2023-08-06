pip install wheel twine\
python setup.py sdist bdist_wheel\
twine check *\
twine upload  -uadikish1990 -pe6x.labs@5g --repository-url https://upload.pypi.org/legacy/ dist/*\
pip install uniphi

