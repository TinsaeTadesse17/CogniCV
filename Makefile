.PHONY: clean run

clean:
	-find . -type d -name 'tmp_*' -exec rm -rf {} +
	-find . -type d -name '__pycache__' -exec rm -rf {} +
	-find . -type d -name '*.pyc' -exec rm -f {} +
	-find . -type f -name '*.log' -exec rm -f {} +

build:
	@command -v docker-compose >/dev/null 2>&1 || { \
		echo >&2 "Docker Compose is not installed. Installing..."; \
		sudo apt-get update && sudo apt-get install -y docker-compose; \
	}
	docker compose build
	@command -v python3 >/dev/null 2>&1 || { \
		echo >&2 "Python3 is not installed. Installing..."; \
		sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip; \
	}
	@if [ ! -d .venv ]; then \
		python3 -m venv .venv; \
	fi
	. .venv/bin/activate && pip install -r requirements.txt --break-system-packages
	cd frontend && \
		command -v node >/dev/null 2>&1 || { \
			echo >&2 "Node.js is not installed. Installing..."; \
			sudo apt-get update && sudo apt-get install -y nodejs npm; \
		} && \
		npm install
		echo >&2 "Frontend dependencies installed. Run 'make run' to start the application."

run:
	if [ ! -d .venv ]; then \
		echo ".venv not found. Running 'make build' first..."; \
		$(MAKE) build; \
	fi
	. .venv/bin/activate && uvicorn src.main:app --reload &
	cd frontend && npm run dev
	wait
