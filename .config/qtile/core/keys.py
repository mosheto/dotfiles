from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from extras import float_to_front
from utils import config

keys, mod, alt = [ ], 'mod4', 'mod1'
terminal = config['terminal'].copy()

if not terminal['main']:
  terminal['main'] = guess_terminal()

for key in [
  # Switch between windows
  ([mod], 'h', lazy.layout.left()),
  ([mod], 'l', lazy.layout.right()),
  ([mod], 'j', lazy.layout.down()),
  ([mod], 'k', lazy.layout.up()),

  # Move windows between columns
  ([mod, 'shift'], 'h', lazy.layout.shuffle_left()),
  ([mod, 'shift'], 'l', lazy.layout.shuffle_right()),
  ([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
  ([mod, 'shift'], 'k', lazy.layout.shuffle_up()),

  # Increase/decrease window size
  ([mod], 'i', lazy.layout.grow()),
  ([mod], 'm', lazy.layout.shrink()),

  # Window management
  ([mod, 'shift'], 'space', lazy.layout.flip()),
  ([mod], 'o', lazy.layout.maximize()),
  ([mod], 'n', lazy.layout.normalize()),
  ([mod], 'a', lazy.window.kill()),
  ([ ], 'F11', lazy.window.toggle_fullscreen()),

  # Floating window management
  # ([mod], 'space', lazy.window.toggle_floating()),
  ([mod], 'c', lazy.window.center()),
  ([mod], 'f', lazy.function(float_to_front)),

  # Toggle between layouts
  ([mod], 'Tab', lazy.next_layout()),

  # Qtile management
  ([mod, 'control'], 'r', lazy.reload_config()),
  
  ([mod, 'shift'], 'b', lazy.hide_show_bar()),
  ([mod, "shift"], "q", lazy.shutdown()),
  ([mod, "shift"], "r", lazy.restart()),
  ([mod, "shift"], "c", lazy.window.kill()),

  # Terminal
  ([mod], 'Return', lazy.spawn(terminal['main'])),

  # Rofi Launcher
  ([mod, 'shift'], 'p', lazy.spawn("rofi -show power")),
  ([mod, 'shift'], 'Return', lazy.spawn("rofi -show drun")),

  # Keyboard Layout
  ([mod], 'space', lazy.widget["keyboardlayout"].next_keyboard()),

  # Web Browser
  ([mod], 'b', lazy.spawn(config['browser'])),

  # Make screen on standby
  ([mod, 'shift'], 's', lazy.spawn('xset dpms force standby')),

  # Screenshot Tool
  ([ ], 'Print', lazy.spawn('scrot')),

  # Calculator
  ([ ], 'XF86Calculator', lazy.spawn('qalculate-gtk')),

  # Volume
  ([ ], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
  ([ ], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
  ([ ], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),

  # Player
  ([ ], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
  ([ ], 'XF86AudioPrev', lazy.spawn('playerctl previous')),
  ([ ], 'XF86AudioNext', lazy.spawn('playerctl next')),
]: keys.append(Key(*key)) # type: ignore
