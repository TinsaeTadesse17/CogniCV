.PHONY: clean run

clean:
	-find . -type d -name 'tmp_*' -exec rm -rf {} +
	-find . -type d -name '__pycache__' -exec rm -rf {} +
	-find . -type d -name '*.pyc' -exec rm -f {} +
	-find . -type f -name '*.log' -exec rm -f {} +

run:
	@command -v docker-compose >/dev/null 2>&1 || { \
		echo >&2 "Docker Compose is not installed. Installing..."; \
		sudo apt-get update && sudo apt-get install -y docker-compose; \
	}
	uvicorn src.main:app --reload
