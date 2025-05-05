from datetime import datetime, timedelta
from typing import List, Dict
from app.models import Transaction

def analyze_expenses(transactions: List[Transaction]) -> Dict:
    """
    Анализирует расходы за последние 3 месяца и генерирует рекомендации.
    """
    # Фильтруем только расходы за последние 90 дней
    recent_expenses = filter_expenses_last_n_days(transactions, 90)
    
    if not recent_expenses:
        return {"message": "Недостаточно данных для анализа", "recommendations": []}
    
    # Группируем расходы по категориям
    expenses_by_category = group_expenses_by_category(recent_expenses)
    
    # Вычисляем средние расходы в категории
    avg_expenses = calculate_average_expenses(expenses_by_category)
    
    # Генерируем рекомендации
    recommendations = generate_recommendations(expenses_by_category, avg_expenses)
    
    return {
        "total_expenses": sum(expenses_by_category.values()),
        "expenses_by_category": expenses_by_category,
        "recommendations": recommendations
    }

def filter_expenses_last_n_days(transactions: List[Transaction], days: int) -> List[Transaction]:
    """
    Фильтрует только расходы за последние `days` дней.
    """
    cutoff_date = datetime.now().date() - timedelta(days=days)
    return [t for t in transactions if t.type == "expense" and t.date >= cutoff_date]

def group_expenses_by_category(transactions: List[Transaction]) -> Dict[str, float]:
    """
    Группирует расходы по категориям.
    """
    expenses_by_category = {}
    for transaction in transactions:
        category_name = transaction.category.name
        expenses_by_category[category_name] = expenses_by_category.get(category_name, 0.0) + transaction.amount
    return expenses_by_category

def calculate_average_expenses(expenses_by_category: Dict[str, float]) -> Dict[str, float]:
    """
    Вычисляет средние расходы в каждой категории (например, за месяц).
    """
    avg_expenses = {}
    for category, total in expenses_by_category.items():
        avg_expenses[category] = total / 3  # За 3 месяца
    return avg_expenses

def generate_recommendations(
    expenses_by_category: Dict[str, float], 
    avg_expenses: Dict[str, float]
) -> List[str]:
    """
    Генерирует рекомендации по сокращению расходов.
    """
    recommendations = []
    for category, total in expenses_by_category.items():
        avg = avg_expenses.get(category, 0)
        if total > avg * 1.5:  # Если расходы в 1.5 раза выше среднего
            savings = total - avg
            recommendations.append(
                f"Сократите расходы в категории '{category}' на {savings:.2f} руб. "
                f"Текущие расходы: {total:.2f} руб., средние: {avg:.2f} руб."
            )
    if not recommendations:
        recommendations.append("Ваши расходы в норме!")
    return recommendations