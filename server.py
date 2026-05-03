import system.network as network
from system.processes import set_appid, redirect_except
import logging
import asyncio
import sys, os
import socket
import json
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

MAX_EVENTS_PER_TICK = 50

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
    dt = 1 / 60
    accumulator = 0.0
    last_time = time.perf_counter()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                await server.stop()
                running = False
        
        for _ in range(MAX_EVENTS_PER_TICK):
            try:
                event = server.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            
            if event.type == "disconnect":
                if event.conn in server.clients:
                    server.clients.remove(event.conn)
        
        now = time.perf_counter()
        frame_time = min(now - last_time, 0.25)
        last_time = now

        accumulator += frame_time

        while accumulator >= dt:

            # Update your game state using dt

            accumulator -= dt

        screen.fill(fill_color)

        alpha = accumulator / dt

        # Render the game state

        pygame.display.flip()

        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())

logging.info("Server closed")

pygame.quit()
sys.exit()