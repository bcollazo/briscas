init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run coverage run --source briscas -m py.test tests
ifeq (${TRAVIS_PYTHON_VERSION},3.6)
	pipenv run flake8 setup.py briscas tests
	pipenv run codecov
endif

build-upload:
	python setup.py sdist upload

clean:
	find briscas -name *.pyc -delete
	find tests -name *.pyc -delete
	find briscas -name __pycache__ -delete
	find tests -name __pycache__ -delete
	rm -rf dist
	rm -rf build
	rm -rf briscas.egg-info
