#!/usr/bin/env bash

mkdir -p data
cd data || exit 1

# TODO run prefetch.sh

# quickget create unattended
quickget --create-config windows ./windows/Win10_22H2_English_x64v1.iso

# TODO:
#
# ansible setup to manage windows post install setup
# scoop > chocolatey > winget
# create users, programs, services etc.
#
# christitus winutil cli
# tweaks
# hyperv
# wsl
# nixos-wsl
#
# do system updates somehow
# wuauclt.exe /detectnow /updatenow ?? also https://superuser.com/questions/1061931
#
# quickemu has some snapshot functionality
# use it for backups, before mbr2gpt
#
# eject option which runs: mbr2gpt
#
# script to flash image to sda
#
# gparted script to auto fill unallocated space in disk
#
# script to do msa keys
