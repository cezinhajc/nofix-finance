from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import requests


@dataclass
class PierreClient:
    api_key: str
    base_url: str = 'https://www.pierre.finance/tools/api'

    @property
    def headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.api_key}',
        }

    def get_credit_card_transactions_month(self, start_date: str, end_date: str) -> dict:
        response = requests.get(
            f'{self.base_url}/get-transactions',
            headers=self.headers,
            params={
                'startDate': start_date,
                'endDate': end_date,
                'accountType': 'CREDIT',
                'accountSubtype': 'CREDIT_CARD',
                'format': 'structured',
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def current_month_range() -> tuple[str, str]:
        today = date.today()
        return today.replace(day=1).isoformat(), today.isoformat()
