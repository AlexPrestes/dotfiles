from libqtile.config import Key
from libqtile.lazy import lazy
from settings import mod, terminal, terminal_gpu, browser, home

keys = [
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key(
        [mod, "shift"],
        "left",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "right",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [mod, "control"],
        "left",
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "right",
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    # Toggle Fullscreen
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        lazy.hide_show_bar(position="all"),
        desc="Toggle fullscreen and the bars",
    ),
    Key(
        [mod],
        "Return",
        lazy.spawn(terminal),
        desc="Launch terminal",
    ),
    Key([mod, "shift"], "Return", lazy.spawn(f"{home}/.local/bin/terminal_gpu.sh"), desc="Launch terminal GPU"),
    Key([mod], "w", lazy.spawn(f"{browser}"), desc="Launch browser"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    # Qtile system keys
    Key(
        [mod, "shift", "control"],
        "l",
        lazy.spawn("betterlockscreen -l"),
        desc="Lock screen",
    ),
    Key([mod], "q", lazy.spawn(f"{terminal} setsid spf"), desc="File Manager"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Rofi
    Key(
        [mod],
        "d",
        lazy.spawn("rofi -show drun"),
        desc="Launch Rofi menu",
    ),
    # ------------ Hardware Configs ------------
    # Volume
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn(f"{home}/.local/bin/pulsemixer --toggle-mute"),
        desc="Mute audio",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn(f"{home}/.local/bin/pulsemixer --change-volume -1"),
        desc="Volume down",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn(f"{home}/.local/bin/pulsemixer --change-volume +1"),
        desc="Volume up",
    ),
    # Brightness
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn(f"{home}/.local/bin/statusbar/brightnesscontrol down"),
        desc="Brightness down",
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn(f"{home}/.local/bin/statusbar/brightnesscontrol up"),
        desc="Brightness up",
    ),
    # Screenshots
    # Save screen to clipboard
    Key(
        [],
        "Print",
        lazy.spawn("/usr/bin/flameshot gui --clipboard"),
        desc="Save screen to clipboard",
    ),
    # Save screen to screenshots folder
    Key(
        [mod],
        "Print",
        lazy.spawn("/usr/bin/flameshot gui --path /tmp/"),
        desc="Save screen to screenshots folder",
    ),
]
