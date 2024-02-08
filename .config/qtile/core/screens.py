from libqtile.config import Screen

from core.bar import mainBar

def createScreens():
  return [
    Screen(
      top = mainBar,
    )
  ]
