"""Main"""
from kettle import *
import asyncio

k = Kettle(0.4)
k.out_param()
k.onoff()
print("dalshe idet")
k.boil()
k.onoff()
