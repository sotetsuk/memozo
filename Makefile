.PHONY: clean build test pypi

clean: 
		rm -rf build
		rm -rf dist
		rm -rf memozo.egg-info

build:
		python setup.py install

test:
		python -m unittest -v tests/*.py

pypi:
		python setup.py register
		python setup.py sdist bdist bdist_egg upload
lint:
		flake8 memozo/*.py
