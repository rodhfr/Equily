# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Equily is a personal finance tracking application built with Python 3.14+. The project uses `uv` for dependency management and is in active development.

## Development Commands

### Running Tests
```bash
uv run -m unittest discover
# Or use the provided script:
./src/run_tests.sh
```

### Running a Single Test
```bash
uv run -m unittest src.test_models.TestUserSystem.<test_name>
# Example:
uv run -m unittest src.test_models.TestUserSystem.test_add_category
```

### Running the Application
```bash
uv run src/main.py
```

## Architecture

### Domain Model Structure

The application follows a domain-driven design with clear separation of concerns:

**Core Domain Models** (src/models.py):
- `User`: Top-level entity that owns an Account and manages Categories
  - Enforces unique category names (case-insensitive)
  - Always has a "general" category that cannot be renamed or deleted
  - IDs currently use UUID4 (marked for migration to relational DB auto-increment)

- `Account`: Manages balance and transaction history
  - Validates sufficient balance before expenses
  - Maintains transaction list for audit trail

- `Transaction`: Immutable financial records with type (INCOME/EXPENSE), amount, date, category
  - Enforces positive amounts
  - Auto-generates timestamp and UUID on creation

- `Category`: User-defined classification for transactions
  - Cannot have empty names

- `UserInterface`: Facade that provides controlled access to User operations
  - Defaults transactions to "general" category when none specified
  - Returns defensive copies of internal collections to prevent direct mutation

**Custom Exceptions** (src/errors.py):
All domain operations use specific exceptions: `UserError`, `AccountError`, `TransactionError`, `CategoryError`

### Key Design Patterns

1. **Facade Pattern**: `UserInterface` abstracts User and Account complexity
2. **Defensive Copying**: Getters return copies to prevent external mutation
3. **Default Category**: All users have a protected "general" category
4. **Category Deletion Pattern**: `remove_category()` renames the category to "general" rather than deleting it (preserves transaction history)

### Important Business Rules

- Transaction amounts must be positive (sign determined by type)
- Expenses blocked if insufficient balance
- Category names are unique per user (case-insensitive)
- The "general" category cannot be renamed or deleted
- When a category is "removed", it's renamed to "general" (see `UserInterface.remove_category()` and `User.rename_general()`)

## Known TODOs

- Migrate from UUID to relational database auto-increment IDs (marked in Transaction, Category, and User classes)
