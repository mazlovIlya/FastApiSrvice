from datetime import datetime, timedelta
from typing import List, Dict
from app.models import Transaction

def calculate_balance(transactions: List[Transaction]) -> float:
    """
    Рассчитывает текущий баланс на основе списка транзакций.
    Доходы увеличивают баланс, расходы уменьшают.
    """
    balance = 0.0
    for transaction in transactions:
        if transaction.type == "income":
            balance += transaction.amount
        elif transaction.type == "expense":
            balance -= transaction.amount
    return balance

def filter_transactions_by_date(
    transactions: List[Transaction], 
    days_ago: int
) -> List[Transaction]:
    """
    Фильтрует транзакции за последние `days_ago` дней.
    """
    cutoff_date = datetime.now().date() - timedelta(days=days_ago)
    return [t for t in transactions if t.date >= cutoff_date]

def group_expenses_by_category(
    transactions: List[Transaction]
) -> Dict[str, float]:
    """
    Группирует расходы по категориям.
    """
    expenses_by_category = {}
    for transaction in transactions:
        if transaction.type != "expense":
            continue
        category_name = transaction.category.name
        expenses_by_category[category_name] = expenses_by_category.get(category_name, 0.0) + transaction.amount
    return expenses_by_category