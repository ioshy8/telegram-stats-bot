test:
	python -m pytest tests/ -v

type-check:
	mypy src/

format:
	black src/ tests/

lint: type-check
	@echo "✅ Типизация в порядке"

check: test lint
	@echo "✅ Все проверки пройдены"
