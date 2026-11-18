# NovaOS

A Debian GNU/Linux 12 (bookworm) based live system with its own name, login
banner and an animated boot splash (Plymouth theme). This folder is a
`live-build` project, the official Debian tool for making custom Debian ISOs.

NovaOS is an independent project based on Debian. It is not affiliated with or
endorsed by the Debian Project.

## Folder map

```
novaos-build/
├── build.sh                      builds the ISO (run on Debian 12 / debian:bookworm)
├── .github/workflows/build-iso.yml   builds the ISO for free on GitHub
├── assets/generate_assets.py     regenerates all splash artwork (needs Pillow)
└── config/
    ├── package-lists/novaos.list.chroot     packages inside the ISO
    ├── includes.chroot/                     files copied into the OS
    │   ├── etc/os-release, issue, issue.net, lsb-release
    │   └── usr/share/plymouth/themes/novaos/   boot splash theme
    │   └── usr/share/backgrounds/novaos/       wallpaper
    └── hooks/normal/0100-set-novaos-plymouth-theme.hook.chroot
```

## Option A: build on GitHub (no server needed)

1. Create a GitHub repo and upload everything in this folder. Include the
   hidden `.github` folder.
2. Open the repo's **Actions** tab, choose **Build NovaOS ISO**, click
   **Run workflow**.
3. After roughly 30-60 minutes, open the finished run and download the
   **novaos-iso** artifact. It expires after 14 days, so attach the ISO to a
   GitHub Release if you want a permanent link.

## Option B: build on Debian 12

```
sudo apt-get update
sudo apt-get install -y live-build debootstrap squashfs-tools xorriso \
  syslinux syslinux-common isolinux syslinux-utils grub-efi-amd64-bin \
  grub-pc-bin mtools dosfstools cpio zip
sudo ./build.sh
```

This produces `novaos-1.0-amd64.iso`.

## Trying the ISO

- **VirtualBox / QEMU / VMware:** create a Linux (Debian 64-bit) VM, attach the
  ISO as its CD, 2 GB RAM or more, and start it. The NovaOS splash shows during boot.
- **USB stick:** write the ISO with Rufus (DD mode) or balenaEtcher.
- The ISO boots as a **live system** (nothing is installed to disk). The live
  login is user `user`, password `live`.

## Customizing

- **Desktop:** uncomment `task-xfce-desktop` (or GNOME / KDE) in
  `config/package-lists/novaos.list.chroot`.
- **More software:** add package names, one per line, to the same file.
- **Splash colors/text:** edit `assets/generate_assets.py`, run it from the
  `assets/` folder, then copy the new `logo.png`, `wordmark.png`, `dot.png`,
  `progress.png` and `background.png` into
  `config/includes.chroot/usr/share/plymouth/themes/novaos/`.
- **Installer:** this ISO has no installer. To add one, look at adding the
  Calamares installer to the package list.

## Honest status

This kit has not been test-built yet. The first build may need small fixes;
if a build fails, the error text in the log shows what to change.
