"""kettle"""
# import sqlite3
# import time
import configparser
import asyncio

from contextlib import suppress
from threading import *
from multiprocessing import Process
from loguru import logger

logger.add("debug.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="10MB")
# compression="zip"
# логгер


class Kettle:
    """ класс чайник """
    max_volume = 1.0
    # на сколько чайник заполнен
    time = 0
    # время которое он кипит
    temperature = 100
    # температура пока кипит
    time_boil = 10
    # on or off
    status = False

    def __init__(self, volume=0.0):
        # можем задаем воду
        self.volume = volume

    @logger.catch
    def boil(self):
        """boil"""
        # run_task_boil = self.boil_func()
        asyncio.run(self.boil_func())

    @logger.catch
    async def boil_func(self):
        """boil_func"""
        logger.info("start boil")
        check = False
        while self.time != self.time_boil:
            if (self.status) and self.volume != 0.0:
                self.time += 1
                await asyncio.sleep(1)
                if self.time == self.time_boil:
                    check = True
            else:
                logger.info("Kettle not boil")
                self.time = self.time_boil
                check = False
        if check:
            self.time = 0
            logger.info("vskipel")
        else:
            self.time = 0

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
            logger.error("Not enough water in the kettle")
        else:
            self.volume -= volume

    @logger.catch
    def water(self):
        """water in kettle """
        logger.info(f'water = {self.volume}')

    @logger.catch
    def set_config(self):
        """take param from config.txt"""
        config = configparser.ConfigParser()
        config.read("config.ini")
        cfg_param = config["Params"]
        if cfg_param["max_volume"]:
            self.max_volume = cfg_param["max_volume"]
        else:
            self.max_volume = 1.0

        if cfg_param["temperature"]:
            self.temperature = cfg_param["temperature"]
        else:
            self.temperature = 100

        if cfg_param["time_boil"]:
            self.time_boil = cfg_param["time_boil"]
        else:
            self.time_boil = 10

    @logger.catch
    def out_param(self):
        """output param"""
        logger.info(f'\ntemperature = {self.temperature}\n'
                    f'max_volume = {self.max_volume}\n'
                    f'time_boil = {self.time_boil}\n'
                    f'volume = {self.volume}\n'
                    f'status = {self.status}')

    @logger.catch
    async def temper(self):
        """kittle out temp"""
        while self.status is True:
            await asyncio.sleep(1)
            logger.info(
                f'temperature = {self.temperature/self.time_boil*self.time}')

    @logger.catch
    async def main(self):
        """create task"""
        asyncio.create_task(self.temper())
        while self.status is True:
            await asyncio.sleep(1)

    @logger.catch
    def onoff(self):
        """on or off kettle"""
        if not self.status:
            self.status = True
            logger.info("Kettle ON")
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.temper())
            loop.stop()
        else:
            self.status = False
            logger.info("Kettle off")

if __name__ == '__main__':
    k = Kettle(0.4)
    k.out_param()
    k.onoff()
    k.boil()
    #k.onoff()
