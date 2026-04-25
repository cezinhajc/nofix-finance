#!/usr/bin/env python3
import json
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'
PAGE_ID = '34c56dc3-d76c-8004-a991-ef414ef9b828'

DATABASE_LINKS = {
    'Entidades': 'https://www.notion.so/34c56dc3d76c81b6a0b6c370cbc2c647',
    'Lançamentos': 'https://www.notion.so/34c56dc3d76c81cbbed8dad6c5cc3d64',
    'Contas Bancárias': 'https://www.notion.so/34c56dc3d76c819c90eff2e1f945f7f6',
    'Categorias': 'https://www.notion.so/34c56dc3d76c814786c9e11913ee76a5',
    'Clientes/Projetos': 'https://www.notion.so/34c56dc3d76c8135953ee3c666be38c3',
    'Contas a Pagar': 'https://www.notion.so/34d56dc3d76c816a823ac3e07e93eec6',
    'Contas a Receber': 'https://www.notion.so/34d56dc3d76c819eaf93c4ceafd0d482',
    'Cartões': 'https://www.notion.so/34d56dc3d76c8104bde4caa30af4a2f1',
    'Compras no Cartão': 'https://www.notion.so/34d56dc3d76c818a8f32c8266272e728',
    'Parcelas do Cartão': 'https://www.notion.so/34d56dc3d76c81d9bb68d69a74ef659c',
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


def append_blocks(token: str, page_id: str, children: list[dict]):
    res = requests.patch(f'https://api.notion.com/v1/blocks/{page_id}/children', headers=headers(token), json={'children': children}, timeout=60)
    res.raise_for_status()
    return res.json()


def heading(text: str, level: int = 2):
    key = f'heading_{level}'
    return {
        'object': 'block',
        'type': key,
        key: {'rich_text': [{'type': 'text', 'text': {'content': text}}]}
    }


def paragraph(text: str):
    return {
        'object': 'block',
        'type': 'paragraph',
        'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}
    }


def bullet(text: str, url: str | None = None):
    rich_text = [{'type': 'text', 'text': {'content': text, 'link': {'url': url} if url else None}}]
    return {
        'object': 'block',
        'type': 'bulleted_list_item',
        'bulleted_list_item': {'rich_text': rich_text}
    }


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    children = [
        heading('Home Operacional do Nofix Finance', 1),
        paragraph('Central de navegação e operação do Nofix Finance.'),
        heading('Operação diária', 2),
        bullet('Novo lançamento manual'),
        bullet('Nova conta a pagar'),
        bullet('Nova conta a receber'),
        bullet('Nova compra no cartão'),
        bullet('Ver parcelas do cartão'),
        heading('Bases principais', 2),
    ]
    for name, url in DATABASE_LINKS.items():
        children.append(bullet(name, url))

    children += [
        heading('Fluxos recomendados', 2),
        bullet('Contas a pagar: cadastrar, acompanhar vencimento e marcar pagamento'),
        bullet('Contas a receber: cadastrar, acompanhar recebimento e marcar quitação'),
        bullet('Cartão de crédito: cadastrar compra, gerar parcelas e acompanhar impactos futuros'),
    ]

    result = append_blocks(token, PAGE_ID, children)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
