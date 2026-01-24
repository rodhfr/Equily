import uuid
from datetime import datetime
from errors import CategoryError, TransactionError, AccountError, UserError
from typing import Optional, List


class Transaction:
    def __init__(
        self,
        type_t: str,
        amount: float,
        description: str = "",
        category: Optional["Category"] = None,
    ):
        if type_t not in {"INCOME", "EXPENSE"}:
            raise TransactionError("Invalid transaction type")

        if amount <= 0:
            raise TransactionError("Transaction amount must be positive")

        self.type_t: str = type_t
        self.amount: float = amount
        self.description: str = description
        self.category: Optional[Category] = category
        self.date: datetime = datetime.now()
        # TODO: change this id for relational db id (auto_increment or serial).
        self.transaction_id: str = str(uuid.uuid4())


class Category:
    def __init__(self, name: str):
        if not name.strip():
            raise CategoryError("Category name cannot be empty")

        # TODO: change this id for relational db id (auto_increment or serial).
        self.category_id: str = str(uuid.uuid4())
        self.name: str = name


class Account:
    def __init__(self):
        self.balance = 0
        self.transactions = []

    def apply_transaction(self, transaction):
        if transaction.type_t == "EXPENSE" and self.balance < transaction.amount:
            raise AccountError("Insufficient Balance")

        self.balance += (
            transaction.amount
            if transaction.type_t == "INCOME"
            else -transaction.amount
        )

        self.transactions.append(transaction)


class User:
    def __init__(self, name):
        # TODO: change this id for relational db id (auto_increment or serial).
        self.user_id: str = str(uuid.uuid4())
        self.name: str = name
        self.account: Account = Account()
        self.categories: List[Category] = []
        self.general: Category = self.add_category("general")

    def add_category(self, name):
        for cat in self.categories:
            if cat.name.lower() == name.lower():
                raise UserError(f"Category '{name}' already exists.")
        category = Category(name)
        self.categories.append(category)
        return category

    def rename_category(self, category_obj, new_name):
        if category_obj == self.general:
            raise UserError("Cannot rename the general category")
        if not new_name.strip():
            raise UserError("Category name cannot be empty")
        for cat in self.categories:
            if cat.name.lower() == new_name.lower() and cat != category_obj:
                raise UserError(f"Category '{new_name}' already exists")
        if category_obj in self.categories:
            category_obj.name = new_name
        else:
            raise UserError("Category not found")

    def rename_general(self, category_obj: "Category") -> None:
        if category_obj == self.general:
            raise UserError("Cannot delete the general category")
        if category_obj in self.categories:
            category_obj.name = "general"
        else:
            raise UserError("Category not found")


class UserInterface:
    def __init__(self, user):
        self._user = user

    def get_name(self):
        return self._user.name

    def set_name(self, new_name):
        if not new_name.strip():
            raise UserError("Name cannot be empty")
        self._user.name = new_name

    def get_balance(self):
        return self._user.account.balance

    def add_category(self, category_name):
        return self._user.add_category(category_name)

    def remove_category(self, category: "Category") -> None:
        return self._user.rename_general(category)

    def add_transaction(self, type_t, amount, description="", category=None):
        if category is None:
            category = self._user.general
        transaction = Transaction(type_t, amount, description, category)
        self._user.account.apply_transaction(transaction)
        return transaction

    # Getter para categorias
    def get_categories(self):
        return (
            self._user.categories.copy()
        )  # devolve cópia para não alterar diretamente

    # Getter para transações
    def get_transactions(self):
        return self._user.account.transactions.copy()


# Create usr and interface
user = User("Alice")
ui = UserInterface(user)
salary = ui.add_category("Salary")
food = ui.add_category("Food")
work = ui.add_category("Work")


# api to call transaction
ui.add_transaction("INCOME", 1000, "Salary for working as a teacher", salary)
ui.add_transaction("EXPENSE", 200, "Groceries", food)
ui.add_transaction("EXPENSE", 50, "Groceries", food)
ui.add_transaction("EXPENSE", 200, "Groceries", food)
ui.add_transaction("INCOME", 5000, "Internship")

ui.remove_category(food)  # food.name agora é "general"
print("ola", food.name)  # "general"


print(ui.get_balance())

for t in ui.get_transactions():
    print(t.date, t.type_t, t.amount, t.category.name, t.description)
