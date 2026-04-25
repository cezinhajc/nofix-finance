#!/usr/bin/env python3
from pathlib import Path

from packages.notion.credit_card_sync import CreditCardSyncService, save_preview


def main():
    service = CreditCardSyncService()
    result = service.process_purchase(
        card_data={
            'name': 'Cartão Inter',
            'closing_day': 20,
            'due_day': 10,
            'limit_total': 5000,
            'limit_available': 5000,
        },
        purchase_data={
            'description': 'Notebook Dell',
            'purchase_date': '2026-04-15',
            'total_amount': 2400,
            'installments': 6,
        },
    )
    out = Path('/root/.openclaw/workspace/nofix-finance/tmp_credit_card_sync_preview.json')
    save_preview(result, str(out))
    print(out.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
