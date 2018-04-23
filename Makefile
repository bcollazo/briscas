init:
	pip install pipenv
	pipenv install --dev
ifeq (${TRAVIS_PYTHON_VERSION},2.7)
	pip install future
endif

test:
	pipenv run coverage run --source briscas -m py.test tests
ifeq (${TRAVIS_PYTHON_VERSION},3.6)
	pipenv run flake8 setup.py briscas tests
	pipenv run codecov
endif

build-s:
	python setup.py sdist

build-2:
	python setup.py bdist_wheel --python-tag py27

build-3:
	python setup.py bdist_wheel --python-tag py34
	python setup.py bdist_wheel --python-tag py35
	python setup.py bdist_wheel --python-tag py36

clean:
	find briscas -name *.pyc -delete
	find tests -name *.pyc -delete
	find briscas -name __pycache__ -delete
	find tests -name __pycache__ -delete
	rm -rf dist
	rm -rf build
	rm -rf briscas.egg-info
