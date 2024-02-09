from libqtile.config import Screen

from core.bar import mainBar, secondBar, myBar

def createScreens():
  return [
    Screen(
      top = myBar,
    )
  ]
