#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
SEED_FILE = WORKSPACE / 'nofix-finance' / 'templates' / 'seeds' / 'pilot-julio-simpia.json'
NOTION_VERSION = '2022-06-28'
DATABASES = {
    'entidades': '34c56dc3-d76c-81b6-a0b6-c370cbc2c647',
    'categorias': '34c56dc3-d76c-8147-86c9-e11913ee76a5',
    'clientes_projetos': '34c56dc3-d76c-8135-953e-e3c666be38c3',
}


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
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties,
    }
    res = requests.post('https://api.notion.com/v1/pages', headers=headers(token), json=payload, timeout=60)
    res.raise_for_status()
    return res.json()


def title_prop(name: str):
    return {'title': [{'type': 'text', 'text': {'content': name}}]}


def select_prop(name: str):
    return {'select': {'name': name}}


def rich_text_prop(text: str):
    return {'rich_text': [{'type': 'text', 'text': {'content': text}}]}


def build_entidade(item):
    return {
        'Nome': title_prop(item['nome']),
        'Tipo': select_prop(item['tipo']),
        'Status': select_prop(item['status']),
        'Moeda': select_prop(item['moeda']),
        'Timezone': rich_text_prop(item['timezone']),
    }


def build_categoria(item):
    return {
        'Nome': title_prop(item['nome']),
        'Tipo': select_prop(item['tipo']),
        'Categoria pai': rich_text_prop(''),
        'Observações': rich_text_prop(f"Entidade sugerida: {item['entidade']}"),
        'Ativa?': {'checkbox': True},
    }


def build_cliente(item):
    return {
        'Nome': title_prop(item['nome']),
        'Tipo': select_prop(item['tipo']),
        'Status': select_prop(item['status']),
        'Cliente principal': rich_text_prop(item['nome']),
    }


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')
    seed = json.loads(SEED_FILE.read_text(encoding='utf-8'))

    for item in seed['entidades']:
        create_page(token, DATABASES['entidades'], build_entidade(item))
        print(f"Entidade criada: {item['nome']}")

    for item in seed['categorias']:
        create_page(token, DATABASES['categorias'], build_categoria(item))
        print(f"Categoria criada: {item['nome']}")

    for item in seed['clientes_projetos']:
        create_page(token, DATABASES['clientes_projetos'], build_cliente(item))
        print(f"Cliente/Projeto criado: {item['nome']}")


if __name__ == '__main__':
    main()
