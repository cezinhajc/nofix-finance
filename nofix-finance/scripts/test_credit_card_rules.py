#!/usr/bin/env python3
from datetime import date

from packages.core.credit_card_rules import CreditCard, CreditPurchase, calculate_new_available_limit, generate_installments


def scenario(title, card, purchase):
    print(f'\n{title}')
    installments = generate_installments(card, purchase)
    for item in installments:
        print(f'- {item.label} | R$ {item.amount:.2f} | vencimento {item.due_date.isoformat()}')
    print(f'Novo limite disponível: {calculate_new_available_limit(card, purchase.total_amount)}')


def main():
    card = CreditCard(name='Cartão Exemplo', closing_day=20, due_day=10, limit_total=5000, limit_available=5000)

    scenario(
        'Compra antes do fechamento e depois do vencimento do mês',
        card,
        CreditPurchase(description='Notebook', purchase_date=date(2026, 4, 15), total_amount=1200.0, installments=6),
    )

    scenario(
        'Compra antes do fechamento e antes do vencimento do mês',
        card,
        CreditPurchase(description='Celular', purchase_date=date(2026, 4, 5), total_amount=900.0, installments=3),
    )

    scenario(
        'Compra após o fechamento',
        card,
        CreditPurchase(description='Monitor', purchase_date=date(2026, 4, 25), total_amount=600.0, installments=2),
    )


if __name__ == '__main__':
    main()
