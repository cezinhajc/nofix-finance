#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
COMPRAS_DB_ID = '34d56dc3-d76c-818a-8f32-c8266272e728'
PARCELAS_DB_ID = '34d56dc3-d76c-81d9-bb68-d69a74ef659c'
PAGAR_DB_ID = '34d56dc3-d76c-816a-823a-c3e07e93eec6'
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


def patch_database(token: str, database_id: str, properties: dict):
    res = requests.patch(
        f'https://api.notion.com/v1/databases/{database_id}',
        headers=headers(token),
        json={'properties': properties},
        timeout=60,
    )
    res.raise_for_status()
    return res.json()


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    results = {}

    results['compras'] = patch_database(token, COMPRAS_DB_ID, {
        'Cartão Rel': {
            'relation': {
                'database_id': CARTOES_DB_ID,
                'type': 'single_property',
                'single_property': {}
            }
        },
        'Parcelas Rel': {
            'relation': {
                'database_id': PARCELAS_DB_ID,
                'type': 'dual_property',
                'dual_property': {}
            }
        }
    })

    results['parcelas'] = patch_database(token, PARCELAS_DB_ID, {
        'Compra Rel': {
            'relation': {
                'database_id': COMPRAS_DB_ID,
                'type': 'single_property',
                'single_property': {}
            }
        },
        'Conta a Pagar Rel': {
            'relation': {
                'database_id': PAGAR_DB_ID,
                'type': 'single_property',
                'single_property': {}
            }
        }
    })

    results['pagar'] = patch_database(token, PAGAR_DB_ID, {
        'Parcela Rel': {
            'relation': {
                'database_id': PARCELAS_DB_ID,
                'type': 'single_property',
                'single_property': {}
            }
        }
    })

    print(json.dumps({
        'status': 'ok',
        'updated': ['Compras no Cartão', 'Parcelas do Cartão', 'Contas a Pagar']
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
