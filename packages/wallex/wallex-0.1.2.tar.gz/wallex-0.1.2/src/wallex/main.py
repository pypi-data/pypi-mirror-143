import inspect

import requests
from simplejson import JSONDecodeError
import json

from .exceptions import *


def validate_response(response: dict) -> bool:
    return response.get('success') or str(response.get('success')).lower() == 'true'


def get_token(email: str, password: str, remember: bool = False) -> str:
    _ = locals()
    func_name = inspect.currentframe().f_code.co_name

    payload = json.dumps({
        "email": email,
        "password": password,
        'remember': remember
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        r = requests.post('https://api.wallex.ir/auth/login/email', headers=headers, data=payload, timeout=5)
    except Exception as e:
        raise RequestsExceptions(func_name, e, _)

    status_code = r.status_code

    if 200 <= status_code < 300:
        try:
            resp = r.json()
        except JSONDecodeError as e:
            raise JsonDecodingError(func_name, r.text, _)

        if validate_response(resp):
            return resp.get('result').get('token')
        else:
            raise JsonDecodingError(func_name, r.text, _)
    else:
        raise StatusCodeError(func_name, status_code, r.text, _)


class Wallex:
    def __init__(self, token: str, timeout: int = 5, verify: Union[bool, None] = None):
        self.base_url = "https://api.wallex.ir/v1/"
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
        }

    def all_market_stats(self):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'markets',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def symbol_market_stats(self, symbol: str):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'markets',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result').get('symbols').get(symbol.upper())
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def order_book(self, symbol: str):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + f'depth?symbol={symbol.upper()}',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def all_balances(self):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result').get('balances')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def coin_balance(self, coin: str):
        _ = locals()
        coin = coin.upper()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result').get('balances').get(coin)
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def coin_available_balance(self, coin: str):
        _ = locals()
        coin = coin.upper()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                _ = resp.get('result').get('balances').get(coin)
                return float(_.get('value')) - float(_.get('locked'))
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def create_order(self, price: str, quantity: str, side: str, symbol: str, type_: str, client_id: str = None):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        try:
            payload = {
                "price": price,
                "quantity": quantity,
                "side": side.lower(),
                "symbol": symbol.upper(),
                "type": type_.lower(),
            }
            if client_id:
                payload.update({'client_id': client_id})
            payload = json.dumps(payload)

            r = self.session.post(self.base_url + 'account/orders', data=payload,
                                  timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def cancel_order(self, client_id: str):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        try:
            payload = json.dumps({
                "clientOrderId": client_id
            })
            r = self.session.delete(self.base_url + 'account/orders', data=payload,
                                    timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def open_orders(self, symbol: str = None):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        url = f'account/openOrders'
        if symbol is not None:
            url += f'?symbol={symbol.upper()}'

        try:
            r = self.session.get(self.base_url + url, timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result').get('orders')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def open_orders_by_side(self, symbol: str, side: str):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        try:
            r = self.session.get(self.base_url + f'account/openOrders?symbol={symbol.upper()}',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                all_orders = resp.get('result').get('orders')
                __ = []
                for order in all_orders:
                    order: dict
                    if order.get('side').lower() == side.lower():
                        __.append(order)
                return __

            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def user_recent_trades(self, symbol: str = None, side: str = None, active: bool = None):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        params = {}

        if symbol:
            params.update({'symbol': symbol.upper()})
        if side:
            params.update({'side': side.lower()})
        if active:
            params.update({'active': active})

        try:
            r = self.session.get(self.base_url + f'account/trades', params=params,
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result').get('AccountLatestTrades')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def get_order_by_id(self, order_id: str):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        try:
            r = self.session.get(self.base_url + f'account/orders/{order_id}',
                                 timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)

    def withdraw(self, coin: str, client_unique_id: str, network: str, amount: str, address: str, memo: str = None):
        _ = locals()
        func_name = inspect.currentframe().f_code.co_name

        try:
            payload = {
                "coin": coin.upper(),
                "client_unique_id": str(client_unique_id),
                "network": network,
                "value": str(amount),
                "wallet_address": address,
            }
            if memo:
                payload.update({'memo': memo})
            payload = json.dumps(payload)
            r = self.session.post(self.base_url + f'account/crypto-withdrawal', data=payload,
                                  timeout=self.timeout, verify=self.verify)
        except Exception as e:
            raise RequestsExceptions(func_name, e, _)

        status_code = r.status_code

        if 200 <= status_code < 300:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, r.text, _)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text, _)

        else:
            raise StatusCodeError(func_name, status_code, r.text, _)
