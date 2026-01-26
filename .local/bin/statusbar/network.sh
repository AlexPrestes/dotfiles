#!/bin/bash

function ShowInfo {
  if [ "$(networkctl list enp3s0f1 | grep -oh "\w*routable\w*")" == "routable" ]; then
    wan=$(dig +short txt ch whoami.cloudflare @1.0.0.1)
    connection="LAN IP: $(ip addr show enp3s0f1 primary | grep 'inet\ ' | awk '{print $2}') - WAN IP: $wan"
  elif [ "$(networkctl list wlan0 | grep -oh "\w*routable\w*")" == "routable" ]; then
    wan=$(dig +short txt ch whoami.cloudflare @1.0.0.1)
    connection="LAN IP: $(ip addr show wlan0 primary | grep 'inet\ ' | awk '{print $2}') - WAN IP: $wan"
  else
    connection="No active connection."
  fi
  dunstify -i "network-idle" "$connection" -r 123
}

function IconUpdate() {
  if [ "$(networkctl list enp3s0f1 | grep -oh "\w*routable\w*")" == "routable" ]; then
    icon="󰌘 "
  elif [ "$(networkctl list wlan0 | grep -oh "\w*routable\w*")" == "routable" ]; then
    icon="󰖩 "
  else
    icon="󰌙 "
  fi
  printf "%s" "$icon"
}

if [ "$1" = "ShowInfo" ]; then
  ShowInfo
else
  IconUpdate
fi
