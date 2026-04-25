from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import calendar


@dataclass
class CreditCard:
    name: str
    closing_day: int
    due_day: int
    limit_total: float | None = None
    limit_available: float | None = None


@dataclass
class CreditPurchase:
    description: str
    purchase_date: date
    total_amount: float
    installments: int


@dataclass
class Installment:
    number: int
    amount: float
    statement_month: int
    statement_year: int
    due_date: date
    label: str


def add_months(year: int, month: int, count: int) -> tuple[int, int]:
    month_index = (year * 12 + (month - 1)) + count
    new_year = month_index // 12
    new_month = (month_index % 12) + 1
    return new_year, new_month


def safe_date(year: int, month: int, day: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, last_day))


def first_statement_offset(purchase_day: int, closing_day: int) -> int:
    return 1 if purchase_day <= closing_day else 2


def generate_installments(card: CreditCard, purchase: CreditPurchase) -> list[Installment]:
    if purchase.installments < 1:
        raise ValueError('installments must be >= 1')
    base_amount = round(purchase.total_amount / purchase.installments, 2)
    amounts = [base_amount] * purchase.installments
    diff = round(purchase.total_amount - sum(amounts), 2)
    amounts[-1] = round(amounts[-1] + diff, 2)

    offset = first_statement_offset(purchase.purchase_date.day, card.closing_day)
    items: list[Installment] = []

    for idx in range(purchase.installments):
        year, month = add_months(purchase.purchase_date.year, purchase.purchase_date.month, offset - 1 + idx)
        due = safe_date(year, month, card.due_day)
        items.append(
            Installment(
                number=idx + 1,
                amount=amounts[idx],
                statement_month=month,
                statement_year=year,
                due_date=due,
                label=f'{purchase.description} {idx + 1}/{purchase.installments}',
            )
        )
    return items


def calculate_new_available_limit(card: CreditCard, purchase_total: float) -> float | None:
    if card.limit_available is None:
        return None
    return round(card.limit_available - purchase_total, 2)
