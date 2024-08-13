import httpx
from typing import List, Dict, Any, Optional

class FrigateProxyAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://frigate-proxy.ru/ru/api"
        self.api_key = api_key
        self.client = httpx.Client(follow_redirects=True)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to make GET requests."""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = self.client.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to make POST requests."""
        if data is None:
            data = {}
        data['api_key'] = self.api_key
        response = self.client.post(f"{self.base_url}/{endpoint}", data=data)
        response.raise_for_status()
        return response.json()

    def get_categories(self) -> Dict[str, Any]:
        """Запрос на получение категорий (для какого сайта нужны прокси)."""
        return self._get("types")

    def get_countries(self) -> Dict[str, Any]:
        """Запрос на получение списка стран."""
        return self._get("countries")

    def get_operators(self) -> Dict[str, Any]:
        """Запрос на получение списка операторов."""
        return self._get("operators")

    def get_cities(self) -> Dict[str, Any]:
        """Запрос на получение списка городов."""
        return self._get("cities")

    def get_periods(self) -> Dict[str, Any]:
        """Запрос на получение списка периодов аренды."""
        return self._get("periods")

    def create_order(self, site: int, country: int, operator: int | None, city: int | None, qty: int, period: int) -> Dict[str, Any]:
        """Формирование заказа на прокси."""
        params = {
            "site": site,
            "country": country,
            "operator": operator,
            "city": city,
            "qty": qty,
            "period": period
        }
        return self._get("buy", params=params)

    def pay_order(self, order_id: int, coupon: Optional[str] = None) -> Dict[str, Any]:
        """Оплата заказа."""
        params = {"order_id": order_id}
        if coupon:
            params["coupon"] = coupon
        return self._get("pay", params=params)

    def get_order_proxies(self, order_id: int) -> Dict[str, Any]:
        """Получение списка прокси в заказе."""
        return self._get("order", params={"id": order_id})

    def get_proxy_info(self, proxy_ids: List[int]) -> Dict[str, Any]:
        """Вывод информации о конкретных прокси."""
        params = {"ids[]": proxy_ids}
        return self._get("proxy", params=params)

    def prolong_order(self, proxy_ids: List[int], period: int) -> Dict[str, Any]:
        """Продление аренды прокси."""
        params = {"ids[]": proxy_ids, "period": period}
        return self._get("prolong", params=params)

    def get_available_proxies(self, site_type: int, country: Optional[int] = None) -> Dict[str, Any]:
        """Запрос на доступность прокси для конкретного типа."""
        params = {"type": site_type}
        if country:
            params["country"] = country
        return self._get("available_mobile_proxy", params=params)

    def set_ip_auth(self, proxy_ids: List[int], ip_auth: str) -> Dict[str, Any]:
        """Установка авторизации по IP для прокси."""
        params = {"ids[]": proxy_ids, "ip_auth": ip_auth}
        return self._get("ip_auth", params=params)

    def delete_ip_auth(self, proxy_ids: List[int]) -> Dict[str, Any]:
        """Удаление авторизации по IP для прокси."""
        params = {"ids[]": proxy_ids}
        return self._get("ip_auth", params=params)

    def get_balance(self) -> Dict[str, Any]:
        """Запрос на получение баланса."""
        return self._get("balance")

    def get_prices(self) -> Dict[str, Any]:
        """Запрос на получение цен."""
        return self._get("prices")

    def add_to_basket(self, site: int, country: int, operator: int, city: int, qty: int, period: int) -> Dict[str, Any]:
        """Добавление заказа в корзину."""
        params = {
            "site": site,
            "country": country,
            "operator": operator,
            "city": city,
            "qty": qty,
            "period": period
        }
        return self._get("basket", params=params)

    def get_basket_list(self) -> Dict[str, Any]:
        """Получение списка заказов из корзины."""
        return self._get("basketlist")

    def change_login_password(self, proxy_ids: List[int]) -> Dict[str, Any]:
        """Смена логина и пароля на прокси."""
        params = {"act": "change_login_pwd", "ids[]": proxy_ids}
        return self._get("orders_items", params=params)

    def export_all_proxy_data(self) -> Dict[str, Any]:
        """Выгрузка всех данных прокси."""
        return self._get("proxys")

    def close(self):
        """Закрытие HTTP-клиента."""
        self.client.close()
