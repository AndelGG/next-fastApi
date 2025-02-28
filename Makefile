lint:
	pre-commit run --all
run:
	uvicorn src.main:app --reload
