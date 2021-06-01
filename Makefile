
all: 
	@echo "Pleas choose specific target option"

upgrade: clean bump build upload

.PHONY: devenv
devenv:
	( \
		virtualenv -p /usr/local/bin/python venv; \
  	. ./venv/bin/activate; \
		python --version; \
		python -m pip install -r devenv_requirements.txt; \
	)

.PHONY: build
build: clean
	( \
  	. ./venv/bin/activate; \
		python --version; \
		python -m build; \
	)

.PHONY: bump
bump: 
	# Bump patch version	
	bash bump.sh patch

.PHONY: testupload
testupload:
	# Upload to https://test.pypi.org
	# Login according to: https://packaging.python.org/tutorials/packaging-projects/ 
	( \
  	. ./venv/bin/activate; \
		python --version; \
		python -m twine upload --repository testpypi dist/*; \
	)

.PHONY: upload
upload:
	# Upload to https://pypi.org
	( \
  	. ./venv/bin/activate; \
		python --version; \
		python -m twine upload dist/*; \
	)

.PHONY: clean
clean:
	#-rm -i build/*
	-rm -r build/*
	-rm -r dist/*
	-rm -r bip39.egg-info
