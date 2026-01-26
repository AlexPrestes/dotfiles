import os
import subprocess

from libqtile.config import Screen
from libqtile import bar, widget
from libqtile.lazy import lazy
from settings import terminal, home, GREEN, RED, WHITE, CYAN

from widgets.ollama import OllamaWidget

extension_defaults = dict(
    font="UbuntuMono Nerd Font Regular",
    fontsize=14,
    padding=2,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                widget.GroupBox(
                    borderwidth=2,
                    inactive="969696",
                    this_current_screen_border="eee8d5",
                    this_screen_border="eee8d5",
                    highlight_method="line",
                    highlight_color=["00000000", "00000000"],
                    **extension_defaults,
                ),
                widget.Prompt(**extension_defaults),
                widget.Spacer(),
                widget.Clock(format="%A %d %B %H:%M", **extension_defaults),
                widget.Spacer(),
                widget.Systray(),
                widget.Spacer(length=5),
                widget.CheckUpdates(
                    **extension_defaults,
                    update_interval=300,
                    custom_command="(checkupdates; yay -Qua) | cat",
                    display_format=" {updates}",
                    colour_have_updates=GREEN,
                ),
                widget.Spacer(length=5),
                OllamaWidget(
                    update_interval=5,
                    active_color=CYAN,
                    inactive_color=WHITE,
                ),
                widget.Spacer(length=5),
                widget.CPU(format="󰍛 {load_percent:.0f}%", **extension_defaults),
                widget.Spacer(length=5),
                widget.Memory(format=" {MemPercent:.0f}%", **extension_defaults),
                widget.Spacer(length=5),
                widget.DF(
                    partition="/",
                    format=" {r:.0f}%",
                    visible_on_warn=False,
                    **extension_defaults,
                ),
                widget.Spacer(length=5),
                widget.Backlight(
                    backlight_name="intel_backlight",
                    step=2,
                    **extension_defaults,
                    fmt='󰃞 {}',
                    change_command="brightnessctl --device=intel_backlight set {0}%",
                ),
                widget.Spacer(length=5),
                widget.Volume(
                    **extension_defaults,
                    step=1,
                    fmt='󰕾 {}',
                    mouse_callbacks={
                        'Button3': lazy.spawn(
                            f"{terminal} --class dialog -e {home}/.local/bin/pulsemixer --color 1"
                        ),
                    }
                ),
                widget.Spacer(length=5),
                widget.Battery(
                    **extension_defaults,
                    show_short_text=True,
                    charge_char="󱁐",
                    discharge_char="󰂀",
                    full_char="󰂄",
                    format="{char} {percent:2.0%}",
                    low_foreground=GREEN,
                    update_interval=30,
                ),
                widget.Spacer(length=5),
                widget.GenPollText(
                    update_interval=5,
                    **extension_defaults,
                    func=lambda: subprocess.check_output(
                        os.path.expanduser(f"{home}/.local/bin/statusbar/network.sh")
                    ).decode(),
                    mouse_callbacks={
                        "Button1": lazy.spawn(
                            os.path.expanduser(f"{home}/.local/bin/statusbar/network.sh ShowInfo")
                        ),
                        "Button3": lazy.spawn(f"{terminal} --class dialog -e impala"),
                    },
                ),
                widget.Spacer(length=5),
                widget.TextBox(
                    "󰐦",
                    **extension_defaults,
                    mouse_callbacks={
                        "Button1": lazy.spawn(
                            os.path.expanduser(f"{home}/.local/bin/powermenu")
                        )
                    },
                ),
                widget.Spacer(length=10),
            ],
            28,
            background="#000000",
            margin=[1, 1, 1, 1],
        ),
    ),
]

