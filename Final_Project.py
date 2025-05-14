# -*- coding: cp1251 -*-
import json
from datetime import datetime

# �������� ���� ��� ��������� �����
budget = 0
expenses = []

# ������������ ����� � �����
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

# ���������� ����� � ����
def save_data():
    data = {
        'budget': budget,
        'expenses': expenses
    }
    with open('finance_data.json', 'w') as file:
        json.dump(data, file)

# ��������� �����������
def show_welcome():
    print("\n=== Գ�������� ������ �������� ===")
    print("������ '��������' ��� ��������� ������\n")

# ��������� ��������� ������
def show_help():
    print("\n������� �������:")
    print("���������� ������ - ���������� ���������� ������")
    print("������ ������� - ������ ���� �������")
    print("�������� ������� - �������� ������ ������")
    print("������� - �������� ������� �������")
    print("��� �� ���������� - �������� ��� �� ����������")
    print("����� - ��������� ������")

# ������������ �������
def set_budget():
    global budget
    try:
        new_budget = float(input("������ ���� �������: "))
        if new_budget < 0:
            print("������ �� ���� ���� ��'�����!")
            return
        budget = new_budget
        save_data()
        print(f"������ �����������: {budget} ���")
    except ValueError:
        print("�������! ������ ������� ��������.")

# ��������� �������
def add_expense():
    global budget, expenses
    if budget <= 0:
        print("�������� ��������� ������!")
        return
    try:
        amount = float(input("������ ���� �������: "))
        if amount <= 0:
            print("���� ������� �� ���� ����� ����!")
            return
        category = input("������ �������� �������: ").strip()
        if not category:
            print("�������� �� ���� ���� ���������!")
            return
        date_str = input("������ ���� (��-��-���� ��� ������� ������� ��� �������): ").strip()
        if date_str:
            try:
                date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                print("������� ������ ����! ����������� ���������� ����.")
                date = datetime.now().date()
        else:
            date = datetime.now().date()
        if amount > budget:
            print("�����! ������� �������� ������� �������.")
        expense = {
            'amount': amount,
            'category': category,
            'date': date.strftime("%d-%m-%Y")
        }
        expenses.append(expense)
        budget -= amount
        save_data()
        print("������� ������!")
    except ValueError:
        print("�������! ������ ������� ���.")

# ��������� ������
def show_expenses():
    if not expenses:
        print("������ �� ����.")
        return
    print("\n������ ������:")
    print("{:<5} {:<10} {:<15} {:<12}".format("�", "����", "��������", "����"))
    for i, expense in enumerate(expenses, 1):
        print("{:<5} {:<10} {:<15} {:<12}".format(i, f"{expense['amount']} ���", expense['category'], expense['date']))

# ��������� ������� �������
def show_balance():
    print(f"\n������� �������: {budget} ���")

# ��� �� ����������
def show_category_report():
    if not expenses:
        print("������ �� ����.")
        return
    categories = {}
    for expense in expenses:
        category = expense['category']
        categories[category] = categories.get(category, 0) + expense['amount']
    print("\n��� �� ����������:")
    for category, amount in categories.items():
        print(f"{category}: {amount} ���")

# ������� ������� ��������
def main():
    load_data()
    show_welcome()
    while True:
        command = input("\n������ �������: ").strip().lower()
        if command == '��������':
            show_help()
        elif command == '���������� ������':
            set_budget()
        elif command == '������ �������':
            add_expense()
        elif command == '�������� �������':
            show_expenses()
        elif command == '�������':
            show_balance()
        elif command == '��� �� ����������':
            show_category_report()
        elif command == '�����':
            print("������ �� ������������ ����������� �������!")
            break
        else:
            print("������� �������. ������ '��������' ��� ������ ������.")

if __name__ == "__main__":
    main()
