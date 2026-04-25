from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from packages.core.credit_card_rules import CreditCard, CreditPurchase, calculate_new_available_limit, generate_installments


class CreditCardSyncService:
    def process_purchase(self, card_data: dict, purchase_data: dict) -> dict:
        card = CreditCard(
            name=card_data['name'],
            closing_day=int(card_data['closing_day']),
            due_day=int(card_data['due_day']),
            limit_total=float(card_data['limit_total']) if card_data.get('limit_total') is not None else None,
            limit_available=float(card_data['limit_available']) if card_data.get('limit_available') is not None else None,
        )
        purchase = CreditPurchase(
            description=purchase_data['description'],
            purchase_date=date.fromisoformat(purchase_data['purchase_date']),
            total_amount=float(purchase_data['total_amount']),
            installments=int(purchase_data['installments']),
        )

        installments = generate_installments(card, purchase)
        new_limit = calculate_new_available_limit(card, purchase.total_amount)

        return {
            'purchase_key': f"{purchase.description}|{purchase.purchase_date.isoformat()}|{purchase.total_amount}|{purchase.installments}|{card.name}",
            'card': asdict(card),
            'purchase': {
                **purchase_data,
                'calculated_installment_amount': round(purchase.total_amount / purchase.installments, 2),
            },
            'installments': [
                {
                    'number': item.number,
                    'amount': item.amount,
                    'statement_month': item.statement_month,
                    'statement_year': item.statement_year,
                    'due_date': item.due_date.isoformat(),
                    'label': item.label,
                }
                for item in installments
            ],
            'new_limit_available': new_limit,
        }


def save_preview(data: dict, output_path: str):
    Path(output_path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
