#!/usr/bin/env python3
from datetime import date

from packages.core.credit_card_rules import CreditCard, CreditPurchase, calculate_new_available_limit, generate_installments


def main():
    card = CreditCard(name='Cartão Exemplo', closing_day=20, due_day=10, limit_total=5000, limit_available=5000)
    purchase = CreditPurchase(description='Notebook', purchase_date=date(2026, 4, 15), total_amount=1200.0, installments=6)

    installments = generate_installments(card, purchase)
    new_limit = calculate_new_available_limit(card, purchase.total_amount)

    print('Parcelas geradas:')
    for item in installments:
        print(f'- {item.label} | R$ {item.amount:.2f} | vencimento {item.due_date.isoformat()}')

    print(f'Novo limite disponível: {new_limit}')


if __name__ == '__main__':
    main()
