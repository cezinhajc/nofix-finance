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
        'Contas a Pagar': {
            'Título': {'title': {}},
            'Tipo da conta': {'select': {'options': [{'name': 'Fixa'}, {'name': 'Variável'}]}},
            'Status': {'select': {'options': [{'name': 'Prevista'}, {'name': 'Paga'}, {'name': 'Vencida'}, {'name': 'Cancelada'}]}},
            'Fornecedor': {'rich_text': {}},
            'Valor previsto': {'number': {'format': 'real'}},
            'Valor pago': {'number': {'format': 'real'}},
            'Competência': {'date': {}},
            'Vencimento': {'date': {}},
            'Data de pagamento': {'date': {}},
            'Forma de pagamento': {'select': {'options': [{'name': 'Pix'}, {'name': 'TED'}, {'name': 'Boleto'}, {'name': 'Cartão'}, {'name': 'Dinheiro'}, {'name': 'Outro'}]}},
            'Recorrente?': {'checkbox': {}},
            'Periodicidade': {'select': {'options': [{'name': 'Semanal'}, {'name': 'Quinzenal'}, {'name': 'Mensal'}, {'name': 'Anual'}, {'name': 'Avulsa'}]}},
            'Centro de custo': {'rich_text': {}},
            'Observações': {'rich_text': {}},
        },
        'Contas a Receber': {
            'Título': {'title': {}},
            'Tipo da conta': {'select': {'options': [{'name': 'Fixa'}, {'name': 'Variável'}]}},
            'Status': {'select': {'options': [{'name': 'Prevista'}, {'name': 'Recebida'}, {'name': 'Vencida'}, {'name': 'Cancelada'}]}},
            'Cliente': {'rich_text': {}},
            'Valor previsto': {'number': {'format': 'real'}},
            'Valor recebido': {'number': {'format': 'real'}},
            'Competência': {'date': {}},
            'Vencimento': {'date': {}},
            'Data de recebimento': {'date': {}},
            'Forma de recebimento': {'select': {'options': [{'name': 'Pix'}, {'name': 'TED'}, {'name': 'Boleto'}, {'name': 'Cartão'}, {'name': 'Dinheiro'}, {'name': 'Outro'}]}},
            'Recorrente?': {'checkbox': {}},
            'Periodicidade': {'select': {'options': [{'name': 'Semanal'}, {'name': 'Quinzenal'}, {'name': 'Mensal'}, {'name': 'Anual'}, {'name': 'Avulsa'}]}},
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
