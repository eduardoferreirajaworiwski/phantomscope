PYTHON ?= python3

.PHONY: install api dashboard test lint demo demo-interview

install:
	$(PYTHON) -m pip install -e ".[dev]"

api:
	uvicorn phantomscope.api.main:app --reload

dashboard:
	streamlit run app/dashboard.py

test:
	pytest

lint:
	ruff check .

demo:
	PHANTOMSCOPE_OFFLINE_MODE=true uvicorn phantomscope.api.main:app --reload

demo-interview:
	bash scripts/demo_interview.sh
