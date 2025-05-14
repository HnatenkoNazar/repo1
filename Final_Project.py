# -*- coding: cp1251 -*-
import json
from datetime import datetime

# Глобальні змінні для зберігання даних
budget = 0
expenses = []

# Завантаження даних з файлу
def load_data():
    global budget, expenses
    try:
        with open('finance_data.json', 'r') as file:
            data = json.load(file)
            budget = data.get('budget', 0)
            expenses = data.get('expenses', [])
    except FileNotFoundError:
        budget = 0
        expenses = []

# Збереження даних у файл
def save_data():
    data = {
        'budget': budget,
        'expenses': expenses
    }
    with open('finance_data.json', 'w') as file:
        json.dump(data, file)

# Привітання користувача
def show_welcome():
    print("\n=== Фінансовий трекер студента ===")
    print("Введіть 'допомога' для перегляду команд\n")

# Виведення доступних команд
def show_help():
    print("\nДоступні команди:")
    print("встановити бюджет - Встановити початковий бюджет")
    print("додати витрату - Додати нову витрату")
    print("показати витрати - Показати історію витрат")
    print("залишок - Показати залишок бюджету")
    print("звіт за категоріями - Показати звіт за категоріями")
    print("вийти - Завершити роботу")

# Встановлення бюджету
def set_budget():
    global budget
    try:
        new_budget = float(input("Введіть суму бюджету: "))
        if new_budget < 0:
            print("Бюджет не може бути від'ємним!")
            return
        budget = new_budget
        save_data()
        print(f"Бюджет встановлено: {budget} грн")
    except ValueError:
        print("Помилка! Введіть числове значення.")

# Додавання витрати
def add_expense():
    global budget, expenses
    if budget <= 0:
        print("Спочатку встановіть бюджет!")
        return
    try:
        amount = float(input("Введіть суму витрати: "))
        if amount <= 0:
            print("Сума витрати має бути більше нуля!")
            return
        category = input("Введіть категорію витрати: ").strip()
        if not category:
            print("Категорія не може бути порожньою!")
            return
        date_str = input("Введіть дату (ДД-ММ-РРРР або залиште порожнім для сьогодні): ").strip()
        if date_str:
            try:
                date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                print("Невірний формат дати! Використано сьогоднішню дату.")
                date = datetime.now().date()
        else:
            date = datetime.now().date()
        if amount > budget:
            print("Увага! Витрата перевищує залишок бюджету.")
        expense = {
            'amount': amount,
            'category': category,
            'date': date.strftime("%d-%m-%Y")
        }
        expenses.append(expense)
        budget -= amount
        save_data()
        print("Витрату додано!")
    except ValueError:
        print("Помилка! Введіть коректні дані.")

# Виведення витрат
def show_expenses():
    if not expenses:
        print("Витрат ще немає.")
        return
    print("\nСписок витрат:")
    print("{:<5} {:<10} {:<15} {:<12}".format("№", "Сума", "Категорія", "Дата"))
    for i, expense in enumerate(expenses, 1):
        print("{:<5} {:<10} {:<15} {:<12}".format(i, f"{expense['amount']} грн", expense['category'], expense['date']))

# Виведення залишку бюджету
def show_balance():
    print(f"\nЗалишок бюджету: {budget} грн")

# Звіт за категоріями
def show_category_report():
    if not expenses:
        print("Витрат ще немає.")
        return
    categories = {}
    for expense in expenses:
        category = expense['category']
        categories[category] = categories.get(category, 0) + expense['amount']
    print("\nЗвіт за категоріями:")
    for category, amount in categories.items():
        print(f"{category}: {amount} грн")

# Головна функція програми
def main():
    load_data()
    show_welcome()
    while True:
        command = input("\nВведіть команду: ").strip().lower()
        if command == 'допомога':
            show_help()
        elif command == 'встановити бюджет':
            set_budget()
        elif command == 'додати витрату':
            add_expense()
        elif command == 'показати витрати':
            show_expenses()
        elif command == 'залишок':
            show_balance()
        elif command == 'звіт за категоріями':
            show_category_report()
        elif command == 'вийти':
            print("Дякуємо за використання фінансового трекера!")
            break
        else:
            print("Невідома команда. Введіть 'допомога' для списку команд.")

if __name__ == "__main__":
    main()



