.PHONY: clean-pyc ext-test test tox-test test-with-mem upload-docs docs audit

all: clean-pyc test

test:
	py.test tests examples

tox-test:
	tox

release:
	git archive --format zip --output "/Users/rosscdh/p/chute/ansible-raspberry-pi/new-raspberry/roles/chute_client/files/chute-client.zip" master

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
