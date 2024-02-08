import os
import subprocess

from libqtile import hook

from core.keys import createGlobalKeys
from core.groups import createGroups, createGroupsKeys
from core.layouts import createFloatingLayout, createGeneralLayouts
from core.mouse import createMouseEvents
from core.screens import createScreens


##################
# Keys setup
#################
keys = createGlobalKeys() + createGroupsKeys()

##################
# Groups setup
#################
groups = createGroups()

##################
# Layouts setup
#################
layouts = createGeneralLayouts()
floating_layout = createFloatingLayout()

##################
# Mouse setup
#################
mouse = createMouseEvents()

##################
# Screens setup
#################
screens = createScreens()

##################
# Hooks setup
#################
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


##################
# Misc setup
#################

widget_defaults = dict(
    font="Roboto Mono",
    fontsize=12,
    padding=5,
)

auto_fullscreen = True

auto_minimize = False

bring_front_click = False

cursor_warp = False

dgroups_key_binder = None

dgroups_app_rules = [ ]

follow_mouse_focus = True

focus_on_window_activation = 'smart'

reconfigure_screens = True

wl_input_rules = None

wmname = "LG3D"
