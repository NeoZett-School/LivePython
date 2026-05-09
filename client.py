import system.network as network
from system.processes import set_appid, redirect_except
import logging
import asyncio
import sys, os
import socket
import json
import time

import win32event
import win32api
import winerror

import warnings
warnings.simplefilter("always")

import psutil

def is_local_address(ip_to_check):
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.address == ip_to_check:
                return True
    return False

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

MAX_EVENTS_PER_TICK = 50

LOG_FILE = r'log\client_log.txt'
CONFIG_FILE = r'config\client_config.json'
APP_CONFIG = r'config\app_config.json'

with open(APP_CONFIG, "r") as f:
    app_config = json.load(f)

APP_ID = fr'PythonLive.{app_config["app_name"]}.Client.{app_config["app_version"]}'

logging.basicConfig(
    filename=LOG_FILE, 
    filemode="a", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
redirect_except()
set_appid(APP_ID)

mutex = win32event.CreateMutex(None, False, APP_ID)
last_error = win32api.GetLastError()
has_another_client = last_error == winerror.ERROR_ALREADY_EXISTS

pygame.init()

with open(CONFIG_FILE, "r") as f:
    client_config = json.load(f)

is_device_server = is_local_address(client_config["host"])

is_device_instance = not (has_another_client or is_device_server) # Useful for overlapping sounds

pygame.display.set_caption(app_config['window_title'])
pygame.display.set_icon(pygame.image.load(app_config['window_icon']))
screen = pygame.display.set_mode(tuple(app_config['screen_dimensions'].values()))

fill_color = app_config["fill_color"]

def quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))

async def main():
    client = network.Client(
        ws_port=client_config["ws_port"]
    )
    await client.connect(
        host=client_config["host"], 
        port=client_config["port"], 
        family=socket.AF_INET
    )

    running = True

    delta_time = 1 / 60
    accumulator = 0.0
    last_time = time.perf_counter()

    frame_counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                await client.disconnect()
                running = False
            
            # Handle pygame events

        for _ in range(MAX_EVENTS_PER_TICK):
            try:
                event = client.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            # Handle network events
        
        now = time.perf_counter()
        frame_time = min(now - last_time, 0.25)
        last_time = now

        accumulator += frame_time

        while accumulator >= delta_time:

            # Update your game state using delta_time

            accumulator -= delta_time

        screen.fill(fill_color)

        alpha = accumulator / delta_time

        # Render the game state

        pygame.display.flip()

        await asyncio.sleep(0)
        frame_counter += 1

if __name__ == "__main__":
    asyncio.run(main())

logging.info("Client closed")

pygame.quit()
sys.exit()