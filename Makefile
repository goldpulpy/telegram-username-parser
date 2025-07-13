VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

GREEN = \033[0;32m
NC = \033[0m

.PHONY: setup
setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	@python3 -m venv $(VENV)
	@echo "$(GREEN)Installing dependencies...$(NC)"
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)Done! Virtual environment created and dependencies installed.$(NC)"

.PHONY: clean
clean:
	@echo "$(GREEN)Deleting virtual environment...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)Virtual environment deleted.$(NC)"
	@echo "$(GREEN)Clear python cache...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "$(GREEN)Done!$(NC)"

.PHONY: help
help:
	@echo "$(GREEN)Available commands:$(NC)"
	@echo "  make setup   - Create virtual environment and install dependencies"
	@echo "  make clean   - Delete virtual environment"
	@echo "  make help    - Show this help"

.DEFAULT_GOAL := help 