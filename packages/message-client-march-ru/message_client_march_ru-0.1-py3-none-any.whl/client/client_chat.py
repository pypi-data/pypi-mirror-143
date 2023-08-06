import sys
import json
import logging
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, pyqtSignal, QObject

from client.client_chat_conv import Ui_ChatClientWindow
from common_client.variables import KEY_CTRL, KEY_ENTER

sys.path.append('../')
logger = logging.getLogger('client')


class ClientChatWindow(QMainWindow):
    '''
    Класс окна обмена сообщениями с контактом
    '''
    close_chat = pyqtSignal(str)

    def __init__(self, database, transport, current_chat, client_name):
        super().__init__()
        # основные переменные
        self.database = database
        self.transport = transport
        self.client_name = client_name

        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_ChatClientWindow()
        self.ui.setupUi(self)
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        # Кнопка "Выход"
        self.ui.menu_exit.triggered.connect(self.close_current_chat)

        # Кнопка отправить сообщение
        self.ui.btn_send.clicked.connect(self.send_message)

        # Дополнительные требующиеся атрибуты
        # self.contacts_model = None
        self.history_model = None
        self.messages_chat = QMessageBox()

        self.current_chat = current_chat
        self.ui.list_messages.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        # self.clients_list_update()
        self.set_disabled_input()
        self.ctrl_enter = 0

        self.show()

    def keyPressEvent(self, event):
        '''Отлавливание события отправки сообщения путем нажатия Ctrl+Enter'''

        if event.key() == KEY_CTRL and self.ctrl_enter == 0:
            self.ctrl_enter += 1
        if event.key() == KEY_ENTER and self.ctrl_enter == 1:
            self.ctrl_enter += 1
            self.send_message()
            self.ctrl_enter = 0

    def closeEvent(self, event):
        '''При закрытии текущего окна обмена сообщениями идет передача сигнала фукцции close_current_chat'''

        self.close_current_chat()
        event.accept()

    def close_current_chat(self):
        '''Отправка сигнала в класс основного окна для удаления текущего чата из списка активных чатов'''
        self.close_chat.emit(self.current_chat)
        self.close()

    def set_disabled_input(self):
        '''Деактивировать поля ввода'''
        # Надпись  - получатель.
        self.ui.label_new_message.setText(
            'Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        # Поле ввода и кнопка отправки неактивны до выбора получателя.
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

    def history_list_update(self):
        '''Обновление истории сообщений'''
        # Получаем историю сортированную по дате
        list = sorted(self.database.get_history(self.current_chat),
                      key=lambda item: item[3])
        # Если модель не создана, создадим.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        # Очистим от старых записей
        self.history_model.clear()
        # Берём не более 20 последних записей.
        length = len(list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        # Заполнение модели записями, так-же стоит разделить входящие и исходящие выравниванием и разным фоном.
        # Записи в обратном порядке, поэтому выбираем их с конца и не более 20
        for i in range(start_index, length):
            item = list[i]
            if item[1] == 'in':
                # Форматирование поля истории сообщений
                mess_sender = QStandardItem(f'{item[0]} :')
                mess_sender.setFont(
                    QtGui.QFont(
                        "Fantasy",
                        10,
                        QtGui.QFont.Bold))
                mess_sender.setEditable(False)
                mess_sender.setBackground(QBrush(QColor(255, 213, 213)))
                mess_sender.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess_sender)
                mess_time = QStandardItem(f'{item[3].replace(microsecond=0)}')
                mess_time.setFont(QtGui.QFont("Fantasy", 6))
                mess_time.setEditable(False)
                mess_time.setBackground(QBrush(QColor(255, 213, 213)))
                mess_time.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess_time)
                mess = QStandardItem(f'{item[2]}')
                mess.setFont(QtGui.QFont("Fantasy", 9))
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess_sender = QStandardItem(f'{self.client_name} :')
                mess_sender.setFont(
                    QtGui.QFont(
                        "Fantasy",
                        10,
                        QtGui.QFont.Bold))
                mess_sender.setEditable(False)
                mess_sender.setBackground(QBrush(QColor(204, 255, 204)))
                mess_sender.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(mess_sender)
                mess_time = QStandardItem(f'{item[3].replace(microsecond=0)}')
                mess_time.setFont(QtGui.QFont("Fantasy", 6))
                mess_time.setEditable(False)
                mess_time.setBackground(QBrush(QColor(204, 255, 204)))
                mess_time.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(mess_time)
                mess = QStandardItem(f'{item[2]}')
                mess.setFont(QtGui.QFont("Fantasy", 9))
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                mess.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def set_active_user(self):
        '''Метод активации чата с собеседником.'''
        # Запрашиваем публичный ключ пользователя и создаём объект шифрования
        try:
            self.current_chat_key = self.transport.key_request(
                self.current_chat)
            logger.debug(f'Загружен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            logger.debug(f'Не удалось получить ключ для {self.current_chat}')

        # Если ключа нет то ошибка, что не удалось начать чат с пользователем
        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return
        # Ставим надпись и активируем кнопки
        self.ui.label_new_message.setText(
            f'Введите сообщенние для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        # Заполняем окно историю сообщений по требуемому пользователю.
        self.history_list_update()

    def send_message(self):
        '''Функция отправки сообщения пользователю.'''
        # Текст в поле, проверяем что поле не пустое затем забирается сообщение
        # и поле очищается
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)
        try:
            response = self.transport.send_message(
                self.current_chat,
                message_text_encrypted_base64.decode('ascii'))
            pass
        except OSError as err:
            if err.errno:
                self.messages_chat.critical(
                    self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages_chat.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages_chat.critical(
                self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            if response:
                print(response)
                self.messages_chat.information(self, 'Упс!', response)
            else:
                self.database.save_message(
                    self.current_chat, 'out', message_text)
                logger.debug(
                    f'Отправлено сообщение для {self.current_chat}: {message_text}')
                self.history_list_update()
