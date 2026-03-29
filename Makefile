PYTHON ?= python3
PACKAGE = wireguard_server

.PHONY: install-dev fmt lint test test-unit test-integration build clean package-deb package-rpm

install-dev:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e .[dev]

fmt:
	ruff format .
	ruff check . --fix

lint:
	ruff check .
	mypy src

test:
	pytest -q

test-unit:
	pytest tests/unit -q

test-integration:
	pytest tests/integration -q

build:
	$(PYTHON) -m build

package-deb:
	nfpm package --packager deb --config packaging/nfpm.yaml

package-rpm:
	nfpm package --packager rpm --config packaging/nfpm.yaml

clean:
	rm -rf dist build .pytest_cache .mypy_cache .ruff_cache *.egg-info