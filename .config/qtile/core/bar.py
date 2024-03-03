import os
import subprocess

from libqtile.lazy import lazy
from libqtile import bar, widget
from libqtile.widget import base

from qtile_extras.widget import modify
from qtile_extras import widget as extras_widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

from core.colors import colors

class Volume(base._TextBox):
  orientations = base.ORIENTATION_HORIZONTAL
  defaults = [
    ('padding', 5, 'Padding left and right. Calculated if None.'),
    ('update_interval', 0.2, 'Update time in seconds.'),
  ]

  def __init__(self, commands: dict, text = '0%', width = bar.CALCULATED, **config):
    super().__init__(text, width, **config)
    self.add_defaults(Volume.defaults)
    self.vol_commands = commands
    self.volume = None

    self.add_callbacks(
      {
        'Button1': self.mute,
        'Button4': self.increase,
        'Button5': self.decrease,
      }
    )

  def timer_setup(self):
    self.timeout_add(self.update_interval, self.update)

  def button_press(self, x, y, button):
    super().button_press(x, y, button)
    self.draw()

  def get_volume(self):
    try:
      command = self.vol_commands['get']
      output = self.call_process(command, shell = True)
      if 'muted' in output.lower():
        output = 'M'
      return output.strip()
    except subprocess.CalledProcessError:
      return -1

  def update(self):
    volume = self.get_volume()
    if volume != self.volume:
      self.volume = volume
      if self.volume == -1:
        self.text = 'M'
      else:
        self.text = self.volume
      self.bar.draw()
    self.timeout_add(self.update_interval, self.update)

  def mute(self):
    if 'mute' in self.vol_commands:
      subprocess.call(self.vol_commands['mute'], shell = True)

  def increase(self):
    if 'increase' in self.vol_commands:
      subprocess.call(self.vol_commands['increase'], shell = True)

  def decrease(self):
    if 'decrease' in self.vol_commands:
      subprocess.call(self.vol_commands['decrease'], shell = True)

class Clock(widget.clock.Clock):
  defaults = [
    (
      'long_format',
      '%A %d %B %Y | %H:%M',
      'Format to show when widget is clicked.',
    ),
  ]

  def __init__(self, **config):
    super().__init__(**config)
    self.add_defaults(Clock.defaults)
    self.short_format = self.format
    self.toggled = False
    self.add_callbacks(
      { 'Button1': self.toggle }
    )

  def toggle(self):
    if self.toggled:
      self.format = self.short_format
    else:
      self.format = self.long_format

    self.toggled = not self.toggled
    self.update(self.poll())

powerline = {
    "decorations": [
        PowerLineDecoration()
    ]
}

defaults = {
  'font': 'SauceCodePro Nerd Font Medium',
  'fontsize': 10,
  'padding': None,
}

def base(bg: str, fg: str) -> dict:
  return {
    'background': bg,
    'foreground': fg,
  }

def decoration(side: str = '') -> dict:
  return { 'decorations': [
    RectDecoration(
      filled = True,
      radius = {
        'left': [8, 0, 0, 8],
        'right': [0, 8, 8, 0]
      }.get(side, 8),
      use_widget_background = True,
    )
  ]}

def iconFont(size = 15) -> dict:
  return {
    'font': 'SauceCodePro Nerd Font',
    'fontsize': size
  }

def powerline(path: str | list, size = 9) -> dict:
  return { 'decorations': [
    PowerLineDecoration(
      path = path,
      size = size,
    )
  ]}

def sep(fg: str, offset = 0, padding = 8) -> extras_widget.TextBox:
  return extras_widget.TextBox(
    **base(None, fg),
    **iconFont(),
    offset = offset,
    padding = padding,
    text = '',
  )

def logo(bg: str, fg: str) -> widget.TextBox:
  return modify(
    widget.TextBox,
    **base(bg, fg),
    **decoration(),
    **iconFont(),
    mouse_callbacks = { 'Button1': lazy.restart() },
    padding = 14,
    text = 'M',
  )

def groups(bg: str) -> extras_widget.GroupBox2:
  return extras_widget.GroupBox2(
    **iconFont(),
    background = bg,
    borderwidth = 1,
    colors = [
      colors['cyan'], colors['magenta'], colors['yellow'],
      colors['red'], colors['blue'], colors['green'],
    ],
    highlight_color = colors['bg'],
    highlight_method = 'line',
    inactive = colors['black'],
    invert = True,
    padding = 7,
    rainbow = True,
  )

def volume(bg: str, fg: str) -> list:
  return [
    modify(
      widget.TextBox,
      **base(bg, fg),
      **decoration('left'),
      **iconFont(),
      text = '',
      x = 4,
    ),
    modify(
      Volume,
      **base(bg, fg),
      **powerline('arrow_right'),
      commands = {
        'decrease': 'pactl set-sink-volume @DEFAULT_SINK@ -5%',
        'increase': 'pactl set-sink-volume @DEFAULT_SINK@ +5%',
        'get': '~/.local/bin/volume',
        'mute': 'pactl set-sink-mute @DEFAULT_SINK@ toggle',
      },
      update_interval = 0.1,
    ),
  ]

def updates(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -1,
      text = '',
      x = -5,
    ),
    extras_widget.CheckUpdates(
      **base(bg, fg),
      **powerline('arrow_right'),
      colour_have_updates = fg,
      colour_no_updates = fg,
      display_format = '{updates} updates',
      distro = 'Arch_checkupdates',
      initial_text = 'No updates',
      no_update_string = 'No updates',
      padding = 5,
      update_interval = 3600,
    ),
  ]

def track_info(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -1,
      text = '',
      x = -5,
    ),
    extras_widget.Mpris2(
      **base(bg, fg),
      **decoration('right'),
      objname = 'org.mpris.MediaPlayer2.spotify',
      display_metadata = ["xesam:title", "xesam:artist"],
    ),
  ]

def window_name(bg: str, fg: str) -> object:
  return widget.WindowName(
    **base(bg, fg),
    format = '{name}',
    max_chars = 60,
    width = bar.CALCULATED,
  )

def cpu(bg: str, fg: str) -> list:
  return [
    modify(
      widget.TextBox,
      **base(bg, fg),
      **iconFont(),
      offset = 3,
      text = '',
      x = 5,
    ),
    extras_widget.CPU(
      **base(bg, fg),
      **powerline('arrow_right'),
      format = '{load_percent:.0f}%',
    )
  ]

def ram(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -2,
      padding = 5,
      text = '﬙',
      x = -2,
    ),
    extras_widget.Memory(
      **base(bg, fg),
      **powerline('arrow_right'),
      measure_mem = "G",
      format = '{MemUsed: .0f}{mm} ',
      padding = -1,
    ),
  ]

def root_disk(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -1,
      text = '',
      x = -5,
    ),
    extras_widget.DF(
      **base(bg, fg),
      **decoration('right'),
      format = 'root: {uf} GB  ',
      padding = 5,
      partition = '/',
      visible_on_warn = False,
      warn_color = fg,
    ),
  ]

def extra_things_disk(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -1,
      text = '',
      x = -5,
    ),
    extras_widget.DF(
      **base(bg, fg),
      **powerline('arrow_right'),
      format = 'extra-things: {uf} GB  ',
      padding = 5,
      partition = '/mnt/ExtraThings',
      visible_on_warn = False,
      warn_color = fg,
    ),
  ]

def things_disk(bg: str, fg: str) -> list:
  return [
    extras_widget.TextBox(
      **base(bg, fg),
      **iconFont(),
      offset = -1,
      text = '',
      x = -5,
    ),
    extras_widget.DF(
      **base(bg, fg),
      **powerline('arrow_right'),
      format = 'things: {uf} GB  ',
      padding = 5,
      partition = '/mnt/Things',
      visible_on_warn = False,
      warn_color = fg,
    ),
  ]

def clock(bg: str, fg: str) -> list:
  return [
    modify(
      extras_widget.TextBox,
      **base(bg, fg),
      **decoration('left'),
      **iconFont(),
      offset = 2,
      text = '',
      x = 4,
    ),
    modify(
      Clock,
      **base(bg, fg),
      **decoration('right'),
      format = '%A - %I:%M %p ',
      long_format = '%B %-d, %Y ',
      padding = 6,
    ),
  ]

def systray() -> list:
  return [
    extras_widget.Systray(
      padding = 5
    ),
  ]

def keyboard_layout(bg: str, fg: str) -> list:
  return [
    modify(
      extras_widget.TextBox,
      **base(bg, fg),
      **iconFont(),
      offset = 2,
      text = ' ',
      x = 4,
    ),
    extras_widget.KeyboardLayout(
      **base(bg, fg),
      **powerline('arrow_right'),
      fmt = '{}',
      padding = 5,
      display_map = {
        'us': 'EN',
        'ara': 'AR'
      },
      configured_keyboards = ["us", "ara"] 
    ),
  ]

def layout_name(bg: str, fg: str) -> list:
  return [
    extras_widget.CurrentLayoutIcon(
      **base(bg, fg),
      **decoration('left'),
      custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
      padding = 5,
      scale = 0.7
    ),
    extras_widget.CurrentLayout(
      **base(bg, fg),
      **powerline('arrow_right'),
      padding = 5
    ),
  ]

myBar = bar.Bar(
    [
        widget.Spacer(length = 2),
        logo(colors['blue'], colors['bg']),
        sep(colors['black'], offset = -8),
        groups(None),
        sep(colors['black'], offset = 4, padding = 4),
        *volume(colors['magenta'], colors['bg']),
        *updates(colors['red'], colors['bg']),
        *track_info(colors['magenta'], colors['bg']),

        widget.Spacer(),
        window_name(None, colors['fg']),
        widget.Spacer(),

        *systray(),
        sep(colors['black']),
        *layout_name(colors['yellow'], colors['bg']),
        *keyboard_layout(colors['green'], colors['bg']),
        *ram(colors['yellow'], colors['bg']),
        *extra_things_disk(colors['cyan'], colors['bg']),
        *things_disk(colors['green'], colors['bg']),
        *root_disk(colors['cyan'], colors['bg']),
        sep(colors['black']),
        *clock(colors['magenta'], colors['bg']),
        widget.Spacer(length = 2),
    ],
    background= colors['bg'],
    border_color= colors['bg'],
    border_width= 4,
    margin= [10, 10, 0, 10],
    opacity= 1,
    size= 18
)

color_list = [
	"#1E1E2E",
	"#CDD6F4",
	"#B4BEFE",
	"#00000000"
]

mainBar = bar.Bar([
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Clock(
        background=color_list[0],
        foreground=color_list[1],
        format="   %d.%m.%Y"
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.CPU(
        background=color_list[0],
        foreground=color_list[1],
        format='   {load_percent}%',
        update_interval=30.0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Memory(
        background=color_list[0],
        foreground=color_list[1],
        format='   {MemPercent}%',
        update_interval=30.0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.WindowName(
        background=color_list[-1],
        foreground=color_list[0],
        format="{name}",
    ),
    widget.Spacer(
        length=bar.STRETCH
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.GroupBox(
        background=color_list[0],
        foreground=color_list[1],
        spacing=6,
        fontsize=14,
        margin=3,
        borderwidth=1,
        inactive=color_list[1],
        active=color_list[1],
        this_current_screen_border='#6C7086',
        highlight_method='block',
        rounded=True,
        
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=bar.STRETCH
    ),
    widget.Systray(
        
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.CheckUpdates(
        background=color_list[0],
        foreground=color_list[1],
        distro='Arch_checkupdates',
        display_format='!    {updates}',
        no_update_string='',
        update_interval=300,
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Volume(
        background=color_list[0],
        foreground=color_list[1],
        emoji=True,
        emoji_list=['', '', '', ''],
        volume_app="pavucontrol",
    ),
    widget.Volume(
        background=color_list[0],
        foreground=color_list[1],
        volume_app="pavucontrol",
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0,
    ),
    widget.Clock(
        background=color_list[0],
        foreground=color_list[1],
        format="   %H:%M",
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    )],
    24,
    background=color_list[-1],
    margin=[4, 6, 2, 6],
    border_width=[0, 0, 0, 0],  # Draw top and bottom borders
    border_color=[color_list[-1], color_list[-1], color_list[-1], color_list[-1]]  # Borders are magenta
)

secondBar = bar.Bar([
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Clock(
        background=color_list[0],
        foreground=color_list[1],
        format="   %d.%m.%Y"
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.CPU(
        background=color_list[0],
        foreground=color_list[1],
        format='   {load_percent}%',
        update_interval=30.0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Memory(
        background=color_list[0],
        foreground=color_list[1],
        format='   {MemPercent}%',
        update_interval=30.0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.WindowName(
        background=color_list[-1],
        foreground=color_list[0],
        format="{name}",
    ),
    widget.Spacer(
        length=bar.STRETCH
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.GroupBox(
        background=color_list[0],
        foreground=color_list[1],
        spacing=6,
        fontsize=14,
        margin=3,
        borderwidth=1,
        inactive=color_list[1],
        active=color_list[1],
        this_current_screen_border='#6C7086',
        highlight_method='block',
        rounded=True,       
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=bar.STRETCH
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.CheckUpdates(
        background=color_list[0],
        foreground=color_list[1],
        distro='Arch_checkupdates',
        display_format='!    {updates}',
        no_update_string='',
        update_interval=300,
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Volume(
        background=color_list[0],
        foreground=color_list[1],
        emoji=True,
        emoji_list=['', '', '', ''],
        volume_app="pavucontrol",
    ),
    widget.Volume(
        background=color_list[0],
        foreground=color_list[1],
        volume_app="pavucontrol",
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    ),
    widget.Spacer(
        length=20
    ),
    widget.TextBox(
        text="\ue0b6",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0,
    ),
    widget.Clock(
        background=color_list[0],
        foreground=color_list[1],
        format="   %H:%M",
    ),
    widget.TextBox(
        text="\ue0b4",
        font="Roboto Mono",
        foreground=color_list[0],
        fontsize=17,
        padding=0
    )],
    24,
    background=color_list[-1],
    margin=[4, 6, 2, 6],
    border_width=[0, 0, 0, 0],  # Draw top and bottom borders
    border_color=[color_list[-1], color_list[-1], color_list[-1], color_list[-1]]  # Borders are magenta
)