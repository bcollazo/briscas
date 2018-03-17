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

