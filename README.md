# WireguardAutoConfiguration

## Описание
WireguardAutoConfiguration — это инструмент для автоматической настройки клиентской конфигурации [WireGuard VPN](https://www.wireguard.com/).

## Требования
>Убедитесь, что у вас развернут сервер WireGuard. Для поднятия сервера вы можете воспользоваться статьей [LinuxBabe: Установка WireGuard VPN на Ubuntu](https://www.linuxbabe.com/ubuntu/wireguard-vpn-server-ubuntu).

## Установка и использование
### Установка
*Для успешной работы необходимо выполнить следующие шаги:*

1. Создайте файл секретов `.env` в корне проекта с содержимым:  
```
PublicKey=[Ваш паблик ключ сервера]
Endpoint=[Адрес вашего сервера]
DNS=[Адрес вашего ДНС сервера]
AllowedIPs=[разрешенные адреса, например - 0.0.0.0/0]
PersistentKeepalive=[индивидуальный параметр, например 22
Code
```

1. Установите библиотеку `python-dotenv` для считывания переменных из файла `.env`:

```bash
pip install python-dotenv
pip install qrcode[pil]
```
### Использование
