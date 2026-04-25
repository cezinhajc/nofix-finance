#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
PARENT_PAGE_ID = '34c56dc3-d76c-8004-a991-ef414ef9b828'


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


def create_database(token: str, title: str, properties: dict):
    payload = {
        'parent': {'type': 'page_id', 'page_id': PARENT_PAGE_ID},
        'title': [{'type': 'text', 'text': {'content': title}}],
        'properties': properties,
    }
    res = requests.post('https://api.notion.com/v1/databases', headers=headers(token), data=json.dumps(payload), timeout=60)
    res.raise_for_status()
    return res.json()


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    schemas = {
        'Cartões': {
            'Nome do cartão': {'title': {}},
            'Banco': {'rich_text': {}},
            'Bandeira': {'select': {'options': [{'name': 'Visa'}, {'name': 'Mastercard'}, {'name': 'Elo'}, {'name': 'Amex'}, {'name': 'Hipercard'}, {'name': 'Outra'}]}},
            'Limite total': {'number': {'format': 'real'}},
            'Limite disponível': {'number': {'format': 'real'}},
            'Dia de fechamento': {'number': {'format': 'number'}},
            'Dia de vencimento': {'number': {'format': 'number'}},
            'Titular': {'rich_text': {}},
            'Ativo?': {'checkbox': {}},
            'Observações': {'rich_text': {}},
        },
        'Compras no Cartão': {
            'Descrição': {'title': {}},
            'Valor total': {'number': {'format': 'real'}},
            'Data da compra': {'date': {}},
            'Parcelado?': {'checkbox': {}},
            'Número de parcelas': {'number': {'format': 'number'}},
            'Valor da parcela': {'number': {'format': 'real'}},
            'Primeira fatura': {'date': {}},
            'Status': {'select': {'options': [{'name': 'Aberta'}, {'name': 'Faturada'}, {'name': 'Quitada'}, {'name': 'Cancelada'}]}},
            'Observações': {'rich_text': {}},
        },
        'Parcelas do Cartão': {
            'Parcela': {'title': {}},
            'Número da parcela': {'number': {'format': 'number'}},
            'Valor da parcela': {'number': {'format': 'real'}},
            'Competência': {'date': {}},
            'Vencimento': {'date': {}},
            'Status': {'select': {'options': [{'name': 'Aberta'}, {'name': 'Faturada'}, {'name': 'Paga'}, {'name': 'Cancelada'}]}},
            'Lançamento gerado?': {'checkbox': {}},
            'Observações': {'rich_text': {}},
        },
    }

    created = {}
    for name, props in schemas.items():
        db = create_database(token, name, props)
        created[name] = {'id': db['id'], 'url': db.get('url')}
        print(f'Criada: {name} -> {db["id"]}')

    print(json.dumps(created, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
