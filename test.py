from PyQt5.QtCore import QObject, QTimer
import socketio
import datetime
import time

from constant.remote_control import RemoteControl
from utils.write_log import writeExceptionToFile, writeExecutionSteps
from controllers.threads.thread_remote_control import ThreadRemoteControl
from current_main_controller import CurrentMainController

class MainController(QObject):

    def __init__(self):
        super().__init__()
        self.__timer = QTimer()
       
        self.__timer.start(60000)
        self.__socket = None
        self.__initSocket()
        CurrentMainController.current_main_controller = self
        self.__thread_remote_control = ThreadRemoteControl(self.__socket, self.__timer)
        self.__count_socket_reconnect = 0


    def __initSocket(self):
        try:
            self.__socket = socketio.Client()
            self.__socket.on('connect', self.__connected)
            self.__socket.on('disconnect', self.__disconnected)
            self.__socket.on('connect_error', self.__connectError)
            self.__socket.connect(RemoteControl.SOCKET_URL)
        except Exception:
            writeExceptionToFile()

    def setScreen(self, screen):
        self.__thread_remote_control.setScreen(screen)
        
    def requestRemoteControl(self):
        try:
            self.__thread_remote_control.start()
        except Exception:
            writeExceptionToFile()

    def stopRemoteControl(self):
        self.__timer.stop()
        self.__socket.disconnect()
        self.__thread_remote_control.stopThread()
        
    def __connected(self):
        writeExecutionSteps('connection established ' + str(datetime.datetime.now()))

    def __disconnected(self):
        writeExecutionSteps('disconnected from server ' + str(datetime.datetime.now()))

    def __connectError(self, error):
        try:
            writeExecutionSteps("The connection failed!" + str(error) if error is not None else "")
            time.sleep(2)
            self.__socket.disconnect()
            self.__socket.connect(RemoteControl.SOCKET_URL)
        except Exception:
            writeExceptionToFile()