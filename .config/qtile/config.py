from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.layout.floating import Floating
from libqtile.layout import Columns
from libqtile.lazy import lazy
from typing import List
import re
import subprocess

from keys import keys as keys_conf
from screens import screens as screens_conf
from screens import extension_defaults as extension_defaults_conf
from settings import mod, BLUE, BLACK
from hooks import *

keys = keys_conf.copy()
screens = screens_conf.copy()
extension_defaults = extension_defaults_conf.copy()


def get_monitors():
    try:
        output = subprocess.check_output("xrandr --query", shell=True).decode()
        return sum(1 for line in output.splitlines() if " connected" in line)
    except Exception:
        return 1


monitors = get_monitors()

# Groups with matches

workspaces = [
    {
        "name": "1",
        "key": "1",
    },  # "matches": [Match(wm_class='firefox')], "layout": "monadtall"},
    {
        "name": "2",
        "key": "2",
    },  # "matches": [Match(wm_class='kitty'), Match(wm_class='ranger')], "layout": "monadtall"},
    {
        "name": "3",
        "key": "3",
    },  # "matches": [Match(wm_class='vim')], "layout": "monadtall"},
    {
        "name": "4",
        "key": "4",
    },  # "matches": [Match(wm_class='telegram-desktop'), Match(wm_class='weechat')], "layout": "monadtall"},
    {
        "name": "5",
        "key": "5",
    },  # "matches": [Match(wm_class='gimp-2.10')], "layout": "monadtall"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    workspaces_layouts = workspace["layout"] if "layout" in workspace else None
    groups.append(Group(workspace["name"], matches=None, layout=workspaces_layouts))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(
        Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"]))
    )


for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i), lazy.window.toscreen(i))])

layout_theme = {
    # "border_width": 1,
    "margin": [0, 1, 2, 1],
    "border_focus": BLUE,
    "border_normal": BLACK,
}

layouts: list[Columns] = [
    Columns(**layout_theme, single_border_width=0, ratio=0.48),
]
# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules: list[dict] = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False


floating_layout = Floating(
    float_rules=[
        Match(title="Quit and close tabs?"),
        Match(title="Please Confirm..."),
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="Conky"),
        Match(wm_class="Firefox"),
        Match(wm_class="file_progress"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title=re.compile(r".*(DEBUG)")),
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Qalculate!"),  # qalculate!
        Match(title="Lista de amigos"),  # steam
        Match(title="Steam — Novidades"),  # steam
        Match(title="Controle de volume do PulseAudio"),  # pulseaudio
        Match(title="Tracker"),  # Tracker
        Match(title="nmtui"),  # nmtui
        Match(title="IRPF 2023"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "Qtile"
