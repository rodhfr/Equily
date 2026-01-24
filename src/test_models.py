import unittest
from datetime import datetime
from models import User, UserInterface, Transaction, Category
from errors import AccountError, TransactionError, UserError


class TestUserSystem(unittest.TestCase):
    def setUp(self):
        # Executa antes de cada teste
        self.user = User("Alice")
        self.ui = UserInterface(self.user)

    # ==========================
    # Testes de categorias
    # ==========================
    def test_add_category(self):
        cat = self.ui.add_category("Food")
        self.assertEqual(cat.name, "Food")
        self.assertIn(cat, self.ui.get_categories())

    def test_add_duplicate_category_raises(self):
        self.ui.add_category("Food")
        with self.assertRaises(UserError):
            self.ui.add_category("Food")  # duplicada

    def test_rename_category(self):
        cat = self.ui.add_category("Work")
        self.user.rename_category(cat, "Office")
        self.assertEqual(cat.name, "Office")

    def test_rename_general_category_raises(self):
        general = self.user.general
        with self.assertRaises(UserError):
            self.user.rename_category(general, "NewName")

    def test_rename_category_to_general(self):
        # Adiciona uma categoria normal
        cat = self.ui.add_category("Leisure")

        # Chama o método que renomeia para "general"
        self.user.rename_general(cat)

        # Verifica se o nome foi alterado
        self.assertEqual(cat.name, "general")

    # ==========================
    # Testes de transações
    # ==========================
    def test_add_income_transaction(self):
        salary = self.ui.add_category("Salary")
        tx = self.ui.add_transaction("INCOME", 1000, "Salary", salary)
        self.assertEqual(tx.amount, 1000)
        self.assertEqual(tx.type_t, "INCOME")
        self.assertEqual(tx.category, salary)
        self.assertEqual(self.ui.get_balance(), 1000)

    def test_add_expense_transaction(self):
        salary = self.ui.add_category("Salary")
        self.ui.add_transaction("INCOME", 500, "Salary", salary)
        food = self.ui.add_category("Food")
        tx = self.ui.add_transaction("EXPENSE", 200, "Groceries", food)
        self.assertEqual(tx.type_t, "EXPENSE")
        self.assertEqual(self.ui.get_balance(), 300)

    def test_expense_more_than_balance_raises(self):
        with self.assertRaises(AccountError):
            self.ui.add_transaction("EXPENSE", 100, "Too much")

    def test_transaction_default_category(self):
        tx = self.ui.add_transaction("INCOME", 500, "Freelance")
        self.assertEqual(tx.category, self.user.general)

    def test_invalid_transaction_type_raises(self):
        with self.assertRaises(TransactionError):
            self.ui.add_transaction("DONATION", 100)

    # ==========================
    # Testes de usuário
    # ==========================
    def test_set_name(self):
        self.ui.set_name("Bob")
        self.assertEqual(self.ui.get_name(), "Bob")

    def test_set_empty_name_raises(self):
        with self.assertRaises(UserError):
            self.ui.set_name("  ")


if __name__ == "__main__":
    unittest.main()
