#!/usr/bin/env python3
import json
from pathlib import Path

import requests

from packages.notion.credit_card_sync import CreditCardSyncService

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
PARCELAS_DB_ID = '34d56dc3-d76c-81d9-bb68-d69a74ef659c'
CARTOES_DB_ID = '34d56dc3-d76c-8104-bde4-caa30af4a2f1'


def load_env(path: Path):
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


def headers(token: str):
    return {
        'Authorization': f'Bearer {token}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
    }


def create_page(token: str, database_id: str, properties: dict):
    payload = {'parent': {'database_id': database_id}, 'properties': properties}
    res = requests.post('https://api.notion.com/v1/pages', headers=headers(token), json=payload, timeout=60)
    res.raise_for_status()
    return res.json()


def update_page(token: str, page_id: str, properties: dict):
    res = requests.patch(f'https://api.notion.com/v1/pages/{page_id}', headers=headers(token), json={'properties': properties}, timeout=60)
    res.raise_for_status()
    return res.json()


def title_prop(text: str):
    return {'title': [{'type': 'text', 'text': {'content': text}}]}


def number_prop(value: float):
    return {'number': value}


def date_prop(value: str):
    return {'date': {'start': value}}


def select_prop(value: str):
    return {'select': {'name': value}}


def checkbox_prop(value: bool):
    return {'checkbox': value}


def rich_text_prop(text: str):
    return {'rich_text': [{'type': 'text', 'text': {'content': text}}]}


def find_existing_installment(token: str, label: str):
    query = requests.post(
        f'https://api.notion.com/v1/databases/{PARCELAS_DB_ID}/query',
        headers=headers(token),
        json={
            'filter': {
                'property': 'Parcela',
                'title': {'equals': label}
            },
            'page_size': 1,
        },
        timeout=60,
    )
    query.raise_for_status()
    results = query.json().get('results', [])
    return results[0] if results else None


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

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

    first_label = result['installments'][0]['label']
    existing = find_existing_installment(token, first_label)
    if existing:
        print(json.dumps({
            'status': 'skipped',
            'reason': 'purchase_already_processed',
            'purchase_key': result['purchase_key'],
            'existing_installment_id': existing['id'],
        }, ensure_ascii=False, indent=2))
        return

    created = []
    for item in result['installments']:
        page = create_page(token, PARCELAS_DB_ID, {
            'Parcela': title_prop(item['label']),
            'Número da parcela': number_prop(item['number']),
            'Valor da parcela': number_prop(item['amount']),
            'Competência': date_prop(f"{item['statement_year']}-{item['statement_month']:02d}-01"),
            'Vencimento': date_prop(item['due_date']),
            'Status': select_prop('Aberta'),
            'Lançamento gerado?': checkbox_prop(False),
            'Observações': rich_text_prop(f"Gerado automaticamente pelo Nofix | purchase_key={result['purchase_key']}"),
        })
        created.append({'id': page['id'], 'url': page.get('url')})

    card_page_id = None
    query = requests.post(
        f'https://api.notion.com/v1/databases/{CARTOES_DB_ID}/query',
        headers=headers(token),
        json={'page_size': 100},
        timeout=60,
    )
    query.raise_for_status()
    for row in query.json().get('results', []):
        title = row.get('properties', {}).get('Nome do cartão', {}).get('title', [])
        name = ''.join(part.get('plain_text', '') for part in title)
        if name == result['card']['name']:
            card_page_id = row['id']
            break

    updated_card = None
    if card_page_id:
        updated_card = update_page(token, card_page_id, {
            'Limite disponível': number_prop(result['new_limit_available'])
        })

    print(json.dumps({'created_installments': created, 'updated_card_id': card_page_id, 'new_limit_available': result['new_limit_available']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
