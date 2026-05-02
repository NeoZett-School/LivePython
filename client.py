import system.network as network
from system.processes import set_appid, redirect_except
import logging
import asyncio
import sys, os
import socket
import json

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

APP_CONFIG = r'config\app_config.json'

app_config = json.load(open(APP_CONFIG, "r"))

LOG_FILE = r'log\client_log.txt'
CONFIG_FILE = r'config\client_config.json'
APP_ID = fr'PythonLive.{app_config["app_name"]}.Client.{app_config["app_version"]}'

logging.basicConfig(
    filename=LOG_FILE, 
    filemode="a", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
redirect_except()
set_appid(APP_ID)

pygame.init()

client_config = json.load(open(CONFIG_FILE, "r"))

pygame.display.set_caption(app_config['window_title'])
pygame.display.set_icon(pygame.image.load(app_config['window_icon']))
screen = pygame.display.set_mode(tuple(app_config['screen_dimensions'].values()))

fill_color = app_config["fill_color"]

async def main():
    client = network.Client()
    await client.connect(client_config["host"], client_config["port"], family=socket.AF_INET)

    running = True
    target = 1 / 60
    last_time = asyncio.get_event_loop().time()

    while running:
        now = asyncio.get_event_loop().time()
        delta_time = now - last_time
        last_time = now

        sleep_time = target - delta_time
        await asyncio.sleep(max(0, sleep_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                await client.disconnect()
                running = False

        async for event in client.get_events():
            ...

        screen.fill(fill_color)

        pygame.display.flip()

if __name__ == "__main__":
    asyncio.run(main())

logging.info("Client closed")

pygame.quit()
sys.exit()