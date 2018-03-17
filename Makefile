init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run coverage run --source briscas -m py.test tests
	echo ${TRAVIS_PYTHON_VERSION}
ifeq (${TRAVIS_PYTHON_VERSION},3.6)
	pipenv run flake8 setup.py briscas tests
	pipenv run codecov
endif

