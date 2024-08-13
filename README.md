
# FrigateProxyAPI

Обертка для API [https://frigate-proxy.ru](https://frigate-proxy.ru). Написана для автоматической закупки и продления прокси. На 13.08.24 сервис предоставляет покупку через API только мобильных прокси. Серверные IPv4 через API не купить.

## Получение API ключа

Получить `api_key` можно здесь: [https://frigate-proxy.ru/ru/develops](https://frigate-proxy.ru/ru/develops).

## Установка

Установите зависимости командой:

```bash
pip install -r req.txt
```

## Использование

### Создание инстанса

```python
from api import FrigateProxyAPI

api_key = 'your_api_key'
instance = FrigateProxyAPI(api_key)
```

### Пример получения всех прокси и их продления если аренда закончится менее чем через 5 дней

```python
all_proxies = instance.export_all_proxy_data()
balance = int(instance.get_balance().get('balance'))

for proxy in all_proxies['proxies']:
    if int(proxy.get("days_left")) < 5:
        order = instance.prolong_order(proxy_ids=[int(proxy.get("id"))], period=4)
        prolong_order_id = order.get('order_id')
        prolong_cost = int(order.get('cost_total'))
        if prolong_cost > balance:
            print('Не хватит денег :(')
        else:
            print('Продлеваем прокси...')
            res_pay = instance.pay_order(order_id=int(prolong_order_id))
            print(res_pay)
```

## Доступные методы

- **`get_categories()`**: Возвращает категории.
- **`get_countries()`**: Возвращает список стран.
- **`get_operators()`**: Возвращает список мобильных операторов.
- **`get_cities()`**: Возвращает список городов.
- **`get_periods()`**: Возвращает доступные периоды аренды.
- **`create_order(site, country, operator, city, qty, period)`**: Создаёт заказ на прокси.
- **`pay_order(order_id, coupon=None)`**: Оплачивает заказ.
- **`get_order_proxies(order_id)`**: Возвращает список прокси в заказе.
- **`get_proxy_info(proxy_ids)`**: Возвращает информацию о конкретных прокси.
- **`prolong_order(proxy_ids, period)`**: Продлевает срок аренды прокси.
- **`get_available_proxies(site_type, country=None)`**: Проверяет наличие прокси.
- **`set_ip_auth(proxy_ids, ip_auth)`**: Устанавливает IP-аутентификацию для прокси.
- **`delete_ip_auth(proxy_ids)`**: Удаляет IP-аутентификацию для прокси.
- **`get_balance()`**: Возвращает баланс аккаунта.
- **`get_prices()`**: Возвращает цены.
- **`add_to_basket(site, country, operator, city, qty, period)`**: Добавляет заказ в корзину.
- **`get_basket_list()`**: Возвращает список заказов в корзине.
- **`change_login_password(proxy_ids)`**: Изменяет логин и пароль для прокси.
- **`export_all_proxy_data()`**: Выгружает все данные о прокси.
