RUN_ONLINE_TESTS=0
SQLALCHEMY_URL="sqlite:///$(realpath tests/tests.sqlite)"

export RUN_ONLINE_TESTS
export SQLALCHEMY_URL
