#!/usr/bin/env bash 

lxsession &

picom &

conky -c $HOME/.config/conky/qtile/doom-one-01.conkyrc

nm-applet &

blueman-tray &

nitrogen --restore &
