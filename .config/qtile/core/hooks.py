import os
import asyncio
import subprocess
from libqtile import hook

from core.bar import bar

margin = sum(bar.margin) if bar else -1

@hook.subscribe.startup
def startup():
  if margin == 0:
    bar.window.window.set_property(
      name = 'WM_NAME',
      value = 'QTILE_BAR',
      type = 'STRING',
      format = 8,
    )

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# @hook.subscribe.client_new
# async def client_new(client):
#   await asyncio.sleep(0.5)
#   if client.name == 'Spotify':
#     client.togroup('6')
