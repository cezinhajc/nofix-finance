#!/usr/bin/env python3
import json
from pathlib import Path

import requests

from packages.banking.pierre_client import PierreClient
from scripts.sync_credit_card_purchase_to_notion import headers as notion_headers, load_env

WORKSPACE = Path('/root/.openclaw/workspace')
NOTION_ENV = WORKSPACE / '.env.notion'
PIERRE_ENV = WORKSPACE / 'nofix-finance' / '.env.pierre.local'
COMPRAS_DB_ID = '34d56dc3-d76c-818a-8f32-c8266272e728'


def load_simple_env(path: Path):
    data = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        data[k.strip()] = v.strip()
    return data


def notion_query(token: str, payload: dict):
    res = requests.post(
        f'https://api.notion.com/v1/databases/{COMPRAS_DB_ID}/query',
        headers=notion_headers(token),
        json=payload,
        timeout=60,
    )
    res.raise_for_status()
    return res.json()


def notion_create_page(token: str, properties: dict):
    res = requests.post(
        'https://api.notion.com/v1/pages',
        headers=notion_headers(token),
        json={'parent': {'database_id': COMPRAS_DB_ID}, 'properties': properties},
        timeout=60,
    )
    res.raise_for_status()
    return res.json()


def relation_prop(page_ids: list[str]):
    return {'relation': [{'id': page_id} for page_id in page_ids]}


def title_prop(text: str):
    return {'title': [{'type': 'text', 'text': {'content': text[:2000]}}]}


def number_prop(value: float):
    return {'number': value}


def date_prop(value: str):
    return {'date': {'start': value[:10]}}


def checkbox_prop(value: bool):
    return {'checkbox': value}


def select_prop(value: str):
    return {'select': {'name': value}}


def rich_text_prop(text: str):
    return {'rich_text': [{'type': 'text', 'text': {'content': text[:2000]}}]}


def purchase_exists(token: str, purchase_key: str):
    data = notion_query(token, {
        'filter': {
            'property': 'Purchase Key',
            'rich_text': {'equals': purchase_key}
        },
        'page_size': 1,
    })
    results = data.get('results', [])
    return results[0] if results else None


def find_card_page(token: str, card_name: str):
    res = requests.post(
        'https://api.notion.com/v1/databases/34d56dc3-d76c-8104-bde4-caa30af4a2f1/query',
        headers=notion_headers(token),
        json={'page_size': 100},
        timeout=60,
    )
    res.raise_for_status()
    for row in res.json().get('results', []):
        title = row.get('properties', {}).get('Nome do cartão', {}).get('title', [])
        name = ''.join(part.get('plain_text', '') for part in title)
        if name.strip().lower() == card_name.strip().lower():
            return row
    return None


def main():
    notion_env = load_env(NOTION_ENV)
    pierre_env = load_simple_env(PIERRE_ENV)
    notion_token = notion_env.get('NOTION_TOKEN')
    pierre_key = pierre_env.get('PIERRE_API_KEY')
    if not notion_token:
        raise SystemExit('NOTION_TOKEN ausente')
    if not pierre_key:
        raise SystemExit('PIERRE_API_KEY ausente em nofix-finance/.env.pierre.local')

    client = PierreClient(api_key=pierre_key)
    start_date, end_date = client.current_month_range()
    data = client.get_credit_card_transactions_month(start_date, end_date)

    created = []
    skipped = []

    accounts = data.get('data', {}).get('transactions', {}).get('accounts', {})
    for account_name, account_group in accounts.items():
        credit_cards = account_group.get('credit_cards', {})
        for card_name, card_group in credit_cards.items():
            purchases = card_group.get('purchases', [])
            for item in purchases:
                description = item.get('description') or item.get('merchant') or 'Compra sem descrição'
                amount = item.get('amount')
                tx_date = item.get('date', '')[:10]
                purchase_key = f"pierre:{card_name}:{tx_date}:{description}:{amount}"
                if purchase_exists(notion_token, purchase_key):
                    skipped.append({'description': description, 'reason': 'already_exists'})
                    continue

                card_page = find_card_page(notion_token, card_name)
                properties = {
                    'Descrição': title_prop(description),
                    'Valor total': number_prop(float(amount or 0)),
                    'Data da compra': date_prop(tx_date),
                    'Parcelado?': checkbox_prop(False),
                    'Número de parcelas': number_prop(1),
                    'Valor da parcela': number_prop(float(amount or 0)),
                    'Status': select_prop('Aberta'),
                    'Cartão': rich_text_prop(card_name),
                    'Processada?': checkbox_prop(False),
                    'Purchase Key': rich_text_prop(purchase_key),
                    'Observações': rich_text_prop(f'Importado da Pierre | account={account_name}'),
                }
                if card_page:
                    properties['Cartão Rel'] = relation_prop([card_page['id']])
                page = notion_create_page(notion_token, properties)
                created.append({'description': description, 'id': page['id'], 'card': card_name})

    print(json.dumps({'created': created, 'skipped': skipped, 'period': {'start': start_date, 'end': end_date}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
