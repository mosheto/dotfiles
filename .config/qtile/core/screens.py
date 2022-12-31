from libqtile.config import Screen

from core.bar import bar
from utils import config

screens = [
  Screen(
    top = bar,
  )
]
