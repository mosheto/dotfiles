from libqtile.config import Group, Key, Match
from libqtile.lazy import lazy

from core.keys import mod

_groups = (
  ('1', '1', 'monadtall', [ ]),
  ('2', '2', 'monadtall', [ ]),
  ('3', '3', "monadtall", [ ]),
  ('4', '4', 'monadtall', [ ]),
  ('5', '5', 'monadtall', [ ]),
  ('6', '6', 'monadtall', [ ]),
  ('7', '7', 'monadtall', [ ]),
  ('8', '8', 'monadtall', [ ]),
  ('9', '9', 'monadtall', [ ]),
)

def createGroups():
  return [Group(name = group[0], label=group[1], layout=group[2], matches=group[3]) for group in _groups]

def createGroupsKeys():
  return (
      # mod1 + letter of group = switch to group
      [ Key([mod], name, lazy.group[name].toscreen(toggle = True)) for name, *rest in _groups]

      # mod1 + shift + letter of group = move focused window to group
      + [ Key([mod, 'shift'], name, lazy.window.togroup(name)) for name, *rest in _groups ]

      # This will toggle between the current and the previous group.
      + [ Key([mod], 'Tab', lazy.screen.toggle_group()) ]
  )