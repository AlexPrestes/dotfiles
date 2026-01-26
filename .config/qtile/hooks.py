from libqtile import qtile, hook
from settings import home
from groups import groups
import subprocess
import time


@hook.subscribe.screen_change
def set_screens(event=None):
    subprocess.run(["autorandr", "--change"])
    # NÃO chame restart() ou cmd_reload_config() aqui — causam recursão


#@hook.subscribe.screen_change
#def restart_on_randr(event):
#    qtile.cmd_reload_config()


@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[
                group.name
            ]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break

#@homeok.subscribe.client_killed
#def fallback(window):
#    if window.group.windows != [window]:
#        return
#    idx = qtile.groups.index(window.group)
#    for group in qtile.groups[idx - 1 :: -1]:
#        if group.windows:
#            qtile.current_screen.toggle_group(group)
#            return
#    qtile.current_screen.toggle_group(qtile.groups[0])

@hook.subscribe.client_new
def slight_delay(*args, **kwargs):
    time.sleep(0.04)


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([home + "/.config/qtile/autostart.sh"])
