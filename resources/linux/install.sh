#!/bin/sh
# Installs Shield for the current user (no root): the program in ~/.local/opt/Shield, a launcher in ~/.local/bin,
# the menu entry, the icon and the .lynx file type. Run it again to update; ./install.sh --uninstall removes it.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
data="${XDG_DATA_HOME:-$HOME/.local/share}"
opt="$HOME/.local/opt/Shield"
bin="$HOME/.local/bin"

if [ "$1" = "--uninstall" ]; then
    rm -rf "$opt" "$bin/Shield" "$data/applications/shield.desktop" "$data/icons/hicolor/256x256/apps/shield.png" "$data/mime/packages/lynx-mime.xml"
    command -v update-mime-database > /dev/null && update-mime-database "$data/mime" || true
    command -v update-desktop-database > /dev/null && update-desktop-database "$data/applications" || true
    echo "Shield removed (your settings stay in ${XDG_CONFIG_HOME:-$HOME/.config}/Shield)."
    exit 0
fi

mkdir -p "$opt" "$bin" "$data/applications" "$data/icons/hicolor/256x256/apps" "$data/mime/packages"
cp -r "$here"/. "$opt"/
ln -sf "$opt/Shield" "$bin/Shield"
sed "s|^Exec=.*|Exec=\"$opt/Shield\" %F|" "$here/shield.desktop" > "$data/applications/shield.desktop"
cp "$here/shield.png" "$data/icons/hicolor/256x256/apps/shield.png"
cp "$here/lynx-mime.xml" "$data/mime/packages/lynx-mime.xml"
command -v update-mime-database > /dev/null && update-mime-database "$data/mime" || true
command -v update-desktop-database > /dev/null && update-desktop-database "$data/applications" || true
command -v gtk-update-icon-cache > /dev/null && gtk-update-icon-cache -q "$data/icons/hicolor" 2> /dev/null || true
echo "Shield installed: start it from the applications menu or run $bin/Shield"
