#!/usr/bin/env python3
import json
from pathlib import Path

import requests

from packages.banking.pierre_client import PierreClient
from scripts.sync_credit_card_purchase_to_notion import headers as notion_headers, load_env

WORKSPACE = Path('/root/.openclaw/workspace')
NOTION_ENV = WORKSPACE / '.env.notion'
PIERRE_ENV = WORKSPACE / 'nofix-finance' / '.env.pierre.local'
CARTOES_DB_ID = '34d56dc3-d76c-8104-bde4-caa30af4a2f1'


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
        f'https://api.notion.com/v1/databases/{CARTOES_DB_ID}/query',
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
        json={'parent': {'database_id': CARTOES_DB_ID}, 'properties': properties},
        timeout=60,
    )
    res.raise_for_status()
    return res.json()


def notion_update_page(token: str, page_id: str, properties: dict):
    res = requests.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=notion_headers(token),
        json={'properties': properties},
        timeout=60,
    )
    res.raise_for_status()
    return res.json()


def title_prop(text: str):
    return {'title': [{'type': 'text', 'text': {'content': text[:2000]}}]}


def number_prop(value):
    return {'number': value}


def rich_text_prop(text: str):
    return {'rich_text': [{'type': 'text', 'text': {'content': text[:2000]}}]}


def checkbox_prop(value: bool):
    return {'checkbox': value}


def select_prop(value: str):
    return {'select': {'name': value}}


def find_card_page(token: str, card_name: str):
    data = notion_query(token, {'page_size': 100})
    for row in data.get('results', []):
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
    if not notion_token or not pierre_key:
        raise SystemExit('Credenciais ausentes')

    client = PierreClient(api_key=pierre_key)
    bill_summary = requests.get(f'{client.base_url}/get-bill-summary', headers=client.headers, timeout=60)
    bill_summary.raise_for_status()
    data = bill_summary.json()

    updated = []
    created = []

    for account in data.get('data', {}).get('accounts', []):
        card_name = account.get('account_name') or 'Cartão sem nome'
        page = find_card_page(notion_token, card_name)
        props = {
            'Banco': rich_text_prop(card_name),
            'Limite total': number_prop(account.get('credit_limit') or 0),
            'Limite disponível': number_prop(account.get('available_credit_limit') or 0),
            'Dia de fechamento': number_prop(account.get('closing_day') or 0),
            'Titular': rich_text_prop('Pierre/Open Finance'),
            'Ativo?': checkbox_prop(True),
            'Valor total da fatura': number_prop(account.get('current_bill_amount') or 0),
            'Observações': rich_text_prop(f"Fatura atual: {account.get('current_bill_amount') or 0} | Vencimento: {account.get('balance_due_date') or 'n/d'}"),
        }
        if page:
            notion_update_page(notion_token, page['id'], props)
            updated.append(card_name)
        else:
            notion_create_page(notion_token, {
                'Nome do cartão': title_prop(card_name),
                'Bandeira': select_prop('Visa'),
                **props,
            })
            created.append(card_name)

    print(json.dumps({'updated': updated, 'created': created}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
