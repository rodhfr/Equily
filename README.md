# Equily
[WIP]
A personal finance management application built with clean domain-driven design. Track income, expenses, and categorize transactions with a simple, dependency-free Python interface.

## Features

- **Transaction Management** — Record income and expenses with descriptions, categories, and automatic timestamps
- **Category System** — Create custom categories to organize transactions; protected default "general" category preserves history
- **Balance Tracking** — Real-time balance updates with validation to prevent overdrafts
- **Immutable Records** — Transactions are append-only, ensuring a reliable audit trail
- **Defensive API** — `UserInterface` facade returns copies of internal data, preventing accidental mutation

## Tech Stack

- Python 3.14+
- Zero external dependencies (stdlib only)
- `uv` for project management
- `unittest` for testing

## Project Structure

```
Equily/
├── src/
│   ├── models.py          # Domain models (User, Account, Transaction, Category)
│   ├── errors.py          # Custom exception hierarchy
│   ├── main.py            # Entry point / demo
│   ├── test_models.py     # Unit tests
│   └── run_tests.sh       # Test runner script
├── Planning/
│   └── CRUD_Planning.excalidraw
├── pyproject.toml
└── LICENSE                # BSD 2-Clause
```

## Getting Started

```bash
git clone https://github.com/rodhfr/Equily.git
cd Equily

# Run the demo
uv run src/main.py

# Run tests
uv run -m unittest discover
```

## Usage Example

```python
from src.models import UserInterface

ui = UserInterface("Alice")
ui.add_category("Food")
ui.add_transaction("INCOME", 3000, "Salary")
ui.add_transaction("EXPENSE", 45.90, "Groceries", "Food")

print(ui.get_balance())        # 2954.1
print(ui.get_categories())     # [general, Food]
print(ui.get_transactions())   # [Salary +3000, Groceries -45.90]
```

## Design

The project follows domain-driven design principles:

- **Transaction** — Immutable value object with UUID, type (INCOME/EXPENSE), amount, description, and category reference
- **Category** — Named grouping for transactions; unique per user (case-insensitive)
- **Account** — Maintains balance and transaction history with validation
- **User** — Aggregate root owning account and categories
- **UserInterface** — Facade providing a simplified, safe API over the domain layer

## License

BSD 2-Clause — see [LICENSE](LICENSE).
