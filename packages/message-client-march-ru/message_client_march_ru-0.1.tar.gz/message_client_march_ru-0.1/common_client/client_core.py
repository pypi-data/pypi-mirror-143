import argparse
import binascii
import hashlib
import hmac
import socket
import sys
import time
import logging
import json
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from common_client.utils import get_message, send_message
from common_client.variables import *
from common_client.errors import ServerError
from common_client.decos import log

# Логер и объект блокировки для работы с сокетом.
logger = logging.getLogger('client')
socket_lock = threading.Lock()


@log
def arg_parser(listen_address, default_port, name, password):
    """
    Парсер командной строки при запуске приложения
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=listen_address, nargs='?')
    parser.add_argument('port', default=default_port, type=int, nargs='?')
    if name:
        parser.add_argument('-n', '--name', default=name, nargs='?')
    else:
        parser.add_argument('-n', '--name', default='', nargs='?')
    if password:
        parser.add_argument('-p', '--password', default=password, nargs='?')
    else:
        parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name, client_passwd


# Класс - Траннспорт, отвечает за взаимодействие с сервером
class ClientTransport(threading.Thread, QObject):
    """
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    """
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    connection_lost = pyqtSignal()
    message_205 = pyqtSignal()

    def __init__(self,
                 port,
                 ip_address,
                 database,
                 username,
                 passwd,
                 keys):
        # Вызываем конструктор предка
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Пароль
        self.password = passwd
        # Сокет для работы с сервером
        self.transport = None
        # Набор ключей для шифрования
        self.keys = keys
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                logger.critical('Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            logger.critical('Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    # Функция инициализации соединения с сервером
    @log
    def connection_init(self, port, ip):
        """Метод отвечающий за установку соединения с сервером.
        :param port - порт сервера
        :param ip - ip адрес сервера"""
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True если
        # удалось
        connected = False
        for i in range(5):
            logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        logger.debug('Установлено соединение с сервером')

        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        logger.debug(f'Passwd hash ready: {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Посылаем серверу приветственное сообщение и получаем ответ что всё
        # нормально или ловим исключение.
        with socket_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            logger.debug(f"Presense message = {presense}")
            try:
                send_message(self.transport, presense)
                ans = get_message(self.transport)
                logger.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ServerError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash_data = hmac.new(
                            passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash_data.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.transport, my_ans)
                        self.process_server_ans(get_message(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                logger.debug('Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    # Функция обрабатывающяя сообщения от сервера. Ничего не возращает.
    # Генерирует исключение при ошибке.

    @log
    def process_server_ans(self, message):
        """Метод обработчик поступающих сообщений с сервера."""
        logger.debug(f'Разбор сообщения от сервера: {message}')
        # Если это подтверждение чего-либо
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                logger.error(
                    f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу, даём сигнал о
        # новом сообщении
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and SENDER in message \
                and DESTINATION in message \
                and MESSAGE_TEXT in message \
                and message[DESTINATION] == self.username:
            logger.debug(
                f'Получено сообщение от пользователя {message[SENDER]}:{message[MESSAGE_TEXT]}')
            # self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
            self.new_message.emit(message)

    # Функция обновляющая контакт - лист с сервера
    @log
    def contacts_list_update(self):
        """Метод обновляющий с сервера список контактов."""
        self.database.contacts_clear()
        logger.debug(f'Запрос контакт листа для пользователя {self.name}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {req}')
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            logger.error('Не удалось обновить список контактов.')

    # Функция обновления таблицы известных пользователей.
    @log
    def user_list_update(self):
        """Метод обновляющий с сервера список пользователей."""
        logger.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей.')

    @log
    def key_request(self, user):
        """Метод запрашивающий с сервера публичный ключ пользователя."""
        logger.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            logger.error(f'Не удалось получить ключ собеседника {user}.')

    # Функция сообщающая на сервер о добавлении нового контакта
    @log
    def add_contact(self, contact):
        """Метод отправляющий на сервер сведения о добавлении контакта."""
        logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_server_ans(get_message(self.transport))

    # Функция удаления клиента на сервере
    @log
    def remove_contact(self, contact):
        """Метод отправляющий на сервер сведения о удалении контакта."""
        logger.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_server_ans(get_message(self.transport))

    # Функция закрытия соединения, отправляет сообщение о выходе.
    @log
    def transport_shutdown(self):
        """Метод уведомляющий сервер о завершении работы клиента."""
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                pass
        logger.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    # Функция отправки сообщения на сервер
    @log
    def send_message(self, dest, message):
        """Метод отправляющий на сервер сообщения для пользователя."""
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: dest,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with socket_lock:
            send_message(self.transport, message_dict)
            try:
                self.process_server_ans(get_message(self.transport))
                logger.info(f'Отправлено сообщение для пользователя {dest}')
            except ServerError as err:
                logger.critical(err.text)
                return err.text

    @log
    def run(self):
        """Метод содержащий основной цикл работы транспортного потока."""
        logger.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать тут задержку, то отправка может достаточно долго
            # ждать освобождения сокета.
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        logger.critical('Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    logger.debug('Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                # Если сообщение получено, то вызываем функцию обработчик:

                finally:
                    self.transport.settimeout(5)
            if message:
                logger.debug(f'Принято сообщение с сервера: {message}')
                self.process_server_ans(message)
