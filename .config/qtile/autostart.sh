#!/bin/sh

# Autostart script for Qtile

cmd_exist() {
  unalias "$1" >/dev/null 2>&1
  command -v "$1" >/dev/null 2>&1
}
__kill() { kill -9 "$(pidof "$1")" >/dev/null 2>&1; }
__start() { sleep 1 && "$@" >/dev/null 2>&1 & }
__running() { pidof "$1" >/dev/null 2>&1; }

# Set the wallpaper using either feh or nitrogen

if cmd_exist feh; then
  __kill feh
  __start feh --bg-fill ~/Imagens/pane-pos.png
fi

# restore wallpaper

if cmd_exist nitrogen; then
  __kill nitrogen
  __start nitrogen --restore
fi

# Notification daemon

if cmd_exist dunst; then
  __kill dunst
  __start dunst
fi

# Unclutter

if cmd_exist unclutter; then
  __kill unclutter
  __start unclutter
fi

# picom compositor

#if cmd_exist picom; then
#  __kill picom
#  __start picom --config ~/.config/picom/picom.conf
#fi
