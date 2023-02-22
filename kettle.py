"""kettle"""
import sqlite3
import time

from threading import *
from multiprocessing import Process
from loguru import logger

logger.add(
    "debug.log", format="{time} {level} {message}", level="DEBUG", rotation="100MB")
#compression="zip" 
# логгер


class Kettle:
    """ класс чайник """

    max_volume = 1.0
    # на сколько чайник заполнен
    time = 0
    # время которое он кипит
    temperature = 100

    time_boil = 10

    # температура пока кипит

    def __init__(self, status=False, volume=0):
        # инициализация включаем и задаем воду
        self.status = status
        self.volume = volume

    @logger.catch
    def boil(self):
        """кипение"""
        check = 0
        # logger.info(
        #     f'temperature = {Kettle.temperature/Kettle.time_boil*Kettle.time}')
        while Kettle.time != Kettle.time_boil:
            if self.status and self.volume!=0:
                Kettle.time += 1
                logger.info(
                    f'temperature = {Kettle.temperature/Kettle.time_boil*Kettle.time}'
                )
                time.sleep(1)
                if Kettle.time == Kettle.time_boil:
                    check = 1
            else:
                logger.info("Kettle off")
                Kettle.time = Kettle.time_boil
                check = 0
        if check == 1:
            Kettle.time = 0
            self.status = False
            logger.info("vskipel")
            logger.info("off")
        else:
            Kettle.time = 0

    @logger.catch
    def input_water(self, vol):
        """вливаем воду"""
        if vol > 1.0:
            logger.error("volume > 1.0")
        elif vol < 0.0:
            logger.error("volume < 0.0")
        else:
            self.volume += vol

    @logger.catch
    def output_water(self, volume):
        """Выливаем воду"""
        if volume > self.volume:
            logger.error("There is not enough water in the kettle")
        else:
            self.volume -= volume

    @logger.catch
    def on_ket(self):
        """ставим статус"""
        if not self.status:
            self.status = True
            logger.info("Kettle ON")
            Kettle.boil(self)
        else:
            logger.error("Kettle is already off", self.status)

    @logger.catch
    def off_ket(self):
        """STOP Kettle"""
        if self.status:
            self.status = False
            logger.info("stop")
        else:
            logger.error("Kettle is already off")

    @logger.catch
    def water(self):
        """water in kettle """
        logger.info(f'water = {self.volume}')