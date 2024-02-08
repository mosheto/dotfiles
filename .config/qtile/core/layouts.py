from libqtile import layout
from libqtile.config import Match

from core.colors import colors

_config = {
  'border_focus': colors['magenta'],
  'border_normal': colors['bg'],
  'border_width': 3,
  'margin': 10,
  'single_border_width': 0,
  'single_margin': 10,
}

def createGeneralLayouts():
  return [
    layout.MonadTall(
      **_config,
      change_ratio = 0.02,
      min_ratio = 0.30,
      max_ratio = 0.70,
    ),

    layout.Max(**_config),
  ]

def createFloatingLayout():
  return layout.Floating(
    border_focus = colors['white'],
    border_normal = colors['bg'],
    border_width = 0,
    fullscreen_border_width = 0,

    float_rules = [
      *layout.Floating.default_float_rules,
      Match(wm_class = [
        'confirmreset',
        'gnome-screenshot',
        'lxappearance',
        'makebranch',
        'maketag',
        'psterm',
        'ssh-askpass',
        'thunar',
        'Xephyr',
        'xfce4-about',
        'wm',
      ]), # type: ignore

      Match(title = [
        'branchdialog',
        'File Operation Progress',
        'minecraft-launcher',
        'Open File',
        'pinentry',
        'wm',
        'Qalculate!'
      ]), # type: ignore
    ],
  )
