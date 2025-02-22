# WireguardAutoConfiguration

## Описание / Description
WireguardAutoConfiguration — это инструмент для автоматической настройки клиентской конфигурации [WireGuard VPN](https://www.wireguard.com/).
WireguardAutoConfiguration is a tool for automatically configuring the client configuration of WireGuard VPN.

## Требования / Requirements
>Убедитесь, что у вас развернут сервер WireGuard. Для поднятия сервера вы можете воспользоваться статьей [LinuxBabe: Установка WireGuard VPN на Ubuntu](https://www.linuxbabe.com/ubuntu/wireguard-vpn-server-ubuntu).
>Make sure you have a WireGuard server set up. You can set up a server by following


## Установка и использование / Installation and Usage
### Установка / Installation
*Для успешной работы необходимо выполнить следующие шаги / To ensure successful operation, please follow these steps:*

1. Создайте файл секретов `.env` в корне проекта с содержимым / Create a secrets file named .env in the root of the project with the following content:
```
PublicKey=[Ваш паблик ключ сервера]
Endpoint=[Адрес вашего сервера]
DNS=[Адрес вашего ДНС сервера]
AllowedIPs=[разрешенные адреса, например - 0.0.0.0/0]
PersistentKeepalive=[индивидуальный параметр, например 22
Code

PublicKey=[Your server's public key]
Endpoint=[Your server's address]
DNS=[Your DNS server's address]
AllowedIPs=[allowed addresses, e.g., 0.0.0.0/0]
PersistentKeepalive=[custom parameter, e.g., 22]
```

1. Установите зависимости из `requirements.txt` / Install the depentions from `requirements.txt`:

```bash
pip install -r requirements.txt
```
### Использование
