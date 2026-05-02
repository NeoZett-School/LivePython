import system.network as network
from system.processes import set_appid, redirect_except
import logging
import asyncio
import sys, os
import socket
import json

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

LOG_FILE = r'log\server_log.txt'
CONFIG_FILE = r'config\server_config.json'
APP_CONFIG = r'config\app_config.json'

app_config = json.load(open(APP_CONFIG, "r"))

APP_ID = fr'PythonLive.{app_config["app_name"]}.Server.{app_config["app_version"]}'

logging.basicConfig(
    filename=LOG_FILE, 
    filemode="a", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
redirect_except()
set_appid(APP_ID)

pygame.init()

server_config = json.load(open(CONFIG_FILE, "r"))

pygame.display.set_caption(server_config['window_title'])
pygame.display.set_icon(pygame.image.load(app_config['window_icon']))
screen = pygame.display.set_mode(tuple(app_config['screen_dimensions'].values()))

fill_color = app_config["fill_color"]

async def main():
    server = network.Server()
    await server.start(server_config["host"], server_config["port"], reuse_address=True, family=socket.AF_INET)

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
                await server.stop()
                running = False
        
        async for event in server.get_events():
            ...
        
        screen.fill(fill_color)
        
        pygame.display.flip()

if __name__ == "__main__":
    asyncio.run(main())

logging.info("Server closed")

pygame.quit()
sys.exit()