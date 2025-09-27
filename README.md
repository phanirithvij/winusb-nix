## Goal

- Manage a windows system on an external drive, as of now an external 256gb sata
  ssd
  - Ideally System Updates, WSL etc. everything should work
  - Along with the possibility to strip it down via tiny11/nano11/ameleorated
    etc.
- I need a windows system to
  - not lose touch with scoop
  - ideally ansible managed
  - gog games, like hollowknight silksong
    - it doesn't work properly via heroic + linux
    - has a rare video playback issue
  - need a proper windows to experience a proper nixos wsl workflow
    - side note: ofcourse there is the on-demand gha windows available but its
      slow, stateless (remote ephemeral)
  - crazy things like btrfs via windows, etc.
  - almost impossible and questionably useful things like nix on windows
    - I mean why? windows, macos are not worth investing in
    - now that I think about it neither is Android as of 2025
    - maybe to make money?
  - ensure I can run cross platform foss software on windows
    - go
    - zig
    - flutter, android studio etc.
    - tailscale
    - yaclibrary
    - jellyfin (it is windows first)
  - win specific foss/proprietrary useful
    - cdisplayex

### Resources

- https://b.agaric.net/page/usb-win
- https://allthings.how/create-a-stripped-down-windows-11-iso-with-nano11-builder/
  - https://github.com/ntdevlabs/nano11
    - https://archive.org/details/nano11_25h2
- https://github.com/ntdevlabs/tiny11builder
- https://github.com/ElliotKillick/Mido
  - https://github.com/physics-enthusiast/mido-nix
  - https://github.com/phanirithvij/mido-nix
- https://github.com/ElliotKillick/qvm-create-windows-qube
