#!/usr/bin/env python3
import json
from pathlib import Path

import requests

from packages.notion.credit_card_sync import CreditCardSyncService
from scripts.sync_credit_card_purchase_to_notion import create_page, date_prop, checkbox_prop, headers, load_env, number_prop, rich_text_prop, select_prop, title_prop, update_page, find_existing_installment

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
COMPRAS_DB_ID = '34d56dc3-d76c-818a-8f32-c8266272e728'
PARCELAS_DB_ID = '34d56dc3-d76c-81d9-bb68-d69a74ef659c'
CARTOES_DB_ID = '34d56dc3-d76c-8104-bde4-caa30af4a2f1'
DEFAULT_CARD_NAME = 'Cartão Inter'


def query_database(token: str, database_id: str, payload: dict):
    res = requests.post(f'https://api.notion.com/v1/databases/{database_id}/query', headers=headers(token), json=payload, timeout=60)
    res.raise_for_status()
    return res.json()


def extract_title(row: dict, prop: str):
    parts = row.get('properties', {}).get(prop, {}).get('title', [])
    return ''.join(part.get('plain_text', '') for part in parts)


def extract_number(row: dict, prop: str):
    return row.get('properties', {}).get(prop, {}).get('number')


def extract_date(row: dict, prop: str):
    date_obj = row.get('properties', {}).get(prop, {}).get('date')
    return date_obj.get('start') if date_obj else None


def extract_checkbox(row: dict, prop: str):
    return row.get('properties', {}).get(prop, {}).get('checkbox')


def extract_rich_text(row: dict, prop: str):
    parts = row.get('properties', {}).get(prop, {}).get('rich_text', [])
    return ''.join(part.get('plain_text', '') for part in parts)


def get_cards(token: str):
    rows = query_database(token, CARTOES_DB_ID, {'page_size': 100}).get('results', [])
    cards = []
    for row in rows:
        title = row.get('properties', {}).get('Nome do cartão', {}).get('title', [])
        name = ''.join(part.get('plain_text', '') for part in title)
        cards.append({
            'page_id': row['id'],
            'name': name,
            'closing_day': row['properties']['Dia de fechamento']['number'],
            'due_day': row['properties']['Dia de vencimento']['number'],
            'limit_total': row['properties']['Limite total']['number'],
            'limit_available': row['properties']['Limite disponível']['number'],
        })
    return cards


def pick_card(cards: list[dict], requested_name: str | None):
    requested_name = (requested_name or '').strip()
    if requested_name:
        for card in cards:
            if card['name'].lower() == requested_name.lower():
                return card
    for card in cards:
        if card['name'] == DEFAULT_CARD_NAME:
            return card
    return cards[0] if cards else None


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    cards = get_cards(token)
    if not cards:
        raise SystemExit('Nenhum cartão encontrado')

    rows = query_database(token, COMPRAS_DB_ID, {'page_size': 100}).get('results', [])
    service = CreditCardSyncService()
    processed = []
    skipped = []

    for row in rows:
        if extract_checkbox(row, 'Processada?'):
            skipped.append({'id': row['id'], 'reason': 'already_marked_processed'})
            continue

        description = extract_title(row, 'Descrição')
        total_amount = extract_number(row, 'Valor total')
        purchase_date = extract_date(row, 'Data da compra')
        installments = extract_number(row, 'Número de parcelas') or 1
        requested_card_name = extract_rich_text(row, 'Cartão')
        card = pick_card(cards, requested_card_name)

        if not description or total_amount is None or not purchase_date:
            skipped.append({'id': row['id'], 'reason': 'missing_data'})
            continue
        if not card:
            skipped.append({'id': row['id'], 'reason': 'card_not_found'})
            continue

        result = service.process_purchase(
            card_data=card,
            purchase_data={
                'description': description,
                'purchase_date': purchase_date,
                'total_amount': total_amount,
                'installments': int(installments),
            },
        )

        existing = find_existing_installment(token, result['installments'][0]['label'])
        if existing:
            update_page(token, row['id'], {
                'Processada?': checkbox_prop(True),
                'Purchase Key': rich_text_prop(result['purchase_key']),
            })
            skipped.append({'id': row['id'], 'description': description, 'reason': 'already_processed_found_in_installments'})
            continue

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
            created.append(page['id'])

        update_page(token, card['page_id'], {'Limite disponível': number_prop(result['new_limit_available'])})
        update_page(token, row['id'], {
            'Processada?': checkbox_prop(True),
            'Purchase Key': rich_text_prop(result['purchase_key']),
        })
        processed.append({'id': row['id'], 'description': description, 'card': card['name'], 'created_installments': len(created)})

    print(json.dumps({'processed': processed, 'skipped': skipped}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
