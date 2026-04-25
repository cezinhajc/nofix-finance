#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
PARCELAS_DB_ID = '34d56dc3-d76c-81d9-bb68-d69a74ef659c'
PAGAR_DB_ID = '34d56dc3-d76c-816a-823a-c3e07e93eec6'


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


def query_database(token: str, database_id: str, payload: dict):
    res = requests.post(f'https://api.notion.com/v1/databases/{database_id}/query', headers=headers(token), json=payload, timeout=60)
    res.raise_for_status()
    return res.json()


def create_page(token: str, database_id: str, properties: dict):
    res = requests.post('https://api.notion.com/v1/pages', headers=headers(token), json={'parent': {'database_id': database_id}, 'properties': properties}, timeout=60)
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


def extract_title(row: dict, prop: str):
    parts = row.get('properties', {}).get(prop, {}).get('title', [])
    return ''.join(part.get('plain_text', '') for part in parts)


def extract_number(row: dict, prop: str):
    return row.get('properties', {}).get(prop, {}).get('number')


def extract_date(row: dict, prop: str):
    date_obj = row.get('properties', {}).get(prop, {}).get('date')
    return date_obj.get('start') if date_obj else None


def payable_exists(token: str, parcel_label: str):
    data = query_database(token, PAGAR_DB_ID, {
        'filter': {
            'property': 'Observações',
            'rich_text': {'contains': f'parcel_ref={parcel_label}'}
        },
        'page_size': 1,
    })
    results = data.get('results', [])
    return results[0] if results else None


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    parcelas = query_database(token, PARCELAS_DB_ID, {'page_size': 100}).get('results', [])
    created = []
    skipped = []

    for row in parcelas:
        label = extract_title(row, 'Parcela')
        value = extract_number(row, 'Valor da parcela')
        due = extract_date(row, 'Vencimento')
        if not label or value is None or not due:
            skipped.append({'label': label, 'reason': 'missing_data'})
            continue
        if payable_exists(token, label):
            skipped.append({'label': label, 'reason': 'already_exists'})
            continue

        payable = create_page(token, PAGAR_DB_ID, {
            'Título': title_prop(label),
            'Tipo da conta': select_prop('Variável'),
            'Status': select_prop('Prevista'),
            'Fornecedor': rich_text_prop('Cartão de crédito'),
            'Valor previsto': number_prop(value),
            'Competência': date_prop(due[:7] + '-01'),
            'Vencimento': date_prop(due),
            'Recorrente?': checkbox_prop(False),
            'Periodicidade': select_prop('Avulsa'),
            'Observações': rich_text_prop(f'Gerado a partir de parcela de cartão | parcel_ref={label}'),
        })
        created.append({'label': label, 'id': payable['id'], 'url': payable.get('url')})

    print(json.dumps({'created': created, 'skipped': skipped}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
