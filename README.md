# WireguardAutoConfinguration
Для успешной работы необходимо:
Файл секретов .env в корне проекта с содержимым

PublicKey=[Ваш паблик ключ сервера]
Endpoint=[Адресс вашего сервера]
DNS=[Адресс вашего ДНС сервера]
AllowedIPs=[разрешенные адресса например - 0.0.0.0/0]
PersistentKeepalive=[индивидуальный параметр, например 22]


Установленный pip install python-dotenv для считывания переменных из файла .env

Развёрнутый сервер Wireguard. Для поднятия использовалась статья https://www.linuxbabe.com/ubuntu/wireguard-vpn-server-ubuntu