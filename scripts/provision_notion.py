#!/usr/bin/env python3
import json
import os
from pathlib import Path

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.notion'
NOTION_VERSION = '2022-06-28'


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


def create_database(token: str, parent_page_id: str, title: str, properties: dict):
    payload = {
        'parent': {'type': 'page_id', 'page_id': parent_page_id},
        'title': [{'type': 'text', 'text': {'content': title}}],
        'properties': properties,
    }
    res = requests.post('https://api.notion.com/v1/databases', headers=headers(token), data=json.dumps(payload), timeout=60)
    res.raise_for_status()
    return res.json()


def title_prop(name='Nome'):
    return {name: {'title': {}}}


def main():
    env = load_env(ENV_FILE)
    token = env.get('NOTION_TOKEN')
    parent_page_id = '34c56dc3d76c8004a991ef414ef9b828'
    if not token:
        raise SystemExit('NOTION_TOKEN ausente em .env.notion')

    schemas = {
        'Entidades': {
            'Nome': {'title': {}},
            'Tipo': {'select': {'options': [{'name': 'Pessoa'}, {'name': 'Empresa'}, {'name': 'Unidade'}]}},
            'Status': {'select': {'options': [{'name': 'Ativa'}, {'name': 'Inativa'}]}},
            'Moeda': {'select': {'options': [{'name': 'BRL'}]}},
            'Timezone': {'rich_text': {}},
            'Observações': {'rich_text': {}},
        },
        'Lançamentos': {
            'Descrição': {'title': {}},
            'Tipo': {'select': {'options': [{'name': 'Receita'}, {'name': 'Despesa'}, {'name': 'Transferência'}, {'name': 'Ajuste'}]}},
            'Status': {'select': {'options': [{'name': 'Previsto'}, {'name': 'Pago'}, {'name': 'Recebido'}, {'name': 'Conciliado'}, {'name': 'Cancelado'}]}},
            'Valor': {'number': {'format': 'real'}},
            'Data de competência': {'date': {}},
            'Data de vencimento': {'date': {}},
            'Data de liquidação': {'date': {}},
            'Centro de custo': {'rich_text': {}},
            'Forma de pagamento': {'select': {'options': [{'name': 'Pix'}, {'name': 'TED'}, {'name': 'Boleto'}, {'name': 'Cartão'}, {'name': 'Dinheiro'}, {'name': 'Outro'}]}},
            'Origem': {'select': {'options': [{'name': 'Manual'}, {'name': 'Banco'}, {'name': 'Sistema'}, {'name': 'Cartão'}]}},
            'ID transação bancária': {'rich_text': {}},
            'Conciliado?': {'checkbox': {}},
            'Observações': {'rich_text': {}},
        },
        'Contas Bancárias': {
            'Nome da conta': {'title': {}},
            'Banco': {'rich_text': {}},
            'Tipo': {'select': {'options': [{'name': 'Corrente'}, {'name': 'Poupança'}, {'name': 'Pagamento'}, {'name': 'Cartão'}]}},
            'Saldo inicial': {'number': {'format': 'real'}},
            'Saldo atual': {'number': {'format': 'real'}},
            'Ativa?': {'checkbox': {}},
            'Provider': {'select': {'options': [{'name': 'Pierre'}, {'name': 'Outro'}]}},
            'Account ID externo': {'rich_text': {}},
            'Observações': {'rich_text': {}},
        },
        'Categorias': {
            'Nome': {'title': {}},
            'Tipo': {'select': {'options': [{'name': 'Receita'}, {'name': 'Despesa'}]}},
            'Categoria pai': {'rich_text': {}},
            'Ativa?': {'checkbox': {}},
            'Observações': {'rich_text': {}},
        },
        'Clientes/Projetos': {
            'Nome': {'title': {}},
            'Tipo': {'select': {'options': [{'name': 'Cliente'}, {'name': 'Projeto'}]}},
            'Status': {'select': {'options': [{'name': 'Ativo'}, {'name': 'Pausado'}, {'name': 'Encerrado'}]}},
            'Cliente principal': {'rich_text': {}},
            'Valor previsto': {'number': {'format': 'real'}},
            'Início': {'date': {}},
            'Fim': {'date': {}},
            'Observações': {'rich_text': {}},
        },
    }

    created = {}
    for name, props in schemas.items():
        db = create_database(token, parent_page_id, name, props)
        created[name] = {'id': db['id'], 'url': db.get('url')}
        print(f'Criada: {name} -> {db["id"]}')

    print(json.dumps(created, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
