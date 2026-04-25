#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
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


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    payload = {
        'properties': {
            'Valor total da fatura': {'number': {'format': 'real'}},
            'Competência da fatura': {'rich_text': {}},
            'Valor a pagar': {'number': {'format': 'real'}},
            'Origem do cartão': {'select': {'options': [{'name': 'API'}, {'name': 'Manual'}]}},
        }
    }
    res = requests.patch(f'https://api.notion.com/v1/databases/{CARTOES_DB_ID}', headers=headers(token), json=payload, timeout=60)
    res.raise_for_status()
    print(json.dumps({'status': 'ok', 'added_properties': ['Valor total da fatura', 'Competência da fatura', 'Valor a pagar', 'Origem do cartão']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
