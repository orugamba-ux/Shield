#!/usr/bin/env bash
# Linux packages of a built Shield binary: an AppImage (one file, runs on most distributions) and a .tar.gz
# (folder with install.sh for a per-user install). Both carry the .desktop entry, the icon and the .lynx file type.
#
# usage: scripts/package-linux.sh <Shield binary> <label> <output folder> [Demo.lynx]
# Variables: APPIMAGETOOL (path to appimagetool; downloaded into ~/opt when missing), ARCH (default x86_64)
set -euo pipefail
cd "$(dirname "$0")/.."

BIN="$1"; LABEL="$2"; OUTDIR="$3"; DEMO="${4:-}"
ARCH="${ARCH:-x86_64}"
NAME="Shield-$LABEL-linux-$ARCH"            # .tar.gz
APPIMAGE="Shield-$LABEL-$ARCH.AppImage"     # AppImage names leave out "linux" (all AppImages are for Linux)
APPID=io.github.orugamba_ux.Shield                 # AppStream component id = desktop file name inside the AppImage
APPIMAGETOOL_VERSION=1.9.0
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$OUTDIR"

# --- folder for the .tar.gz --------------------------------------------------------------------------------
PKG="$WORK/$NAME"
mkdir -p "$PKG"
install -m 755 "$BIN" "$PKG/Shield"
strip --strip-unneeded "$PKG/Shield" 2> /dev/null || true
./scripts/fetch-onnxruntime.sh linux "$PKG"
install -m 644 resources/linux/shield.desktop resources/linux/lynx-mime.xml LICENSE THIRD_PARTY.md PRIVACY.md "$PKG/"
install -m 644 resources/shield_icon_256.png "$PKG/shield.png"
install -m 755 resources/linux/install.sh "$PKG/install.sh"
[[ -n "$DEMO" && -f "$DEMO" ]] && install -m 644 "$DEMO" "$PKG/Demo.lynx"
tar -C "$WORK" -czf "$OUTDIR/$NAME.tar.gz" "$NAME"

# --- AppImage ----------------------------------------------------------------------------------------------
APPDIR="$WORK/Shield.AppDir"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps" \
    "$APPDIR/usr/share/mime/packages" "$APPDIR/usr/share/metainfo"
install -m 755 "$PKG/Shield" "$PKG"/libonnxruntime.so.* "$APPDIR/usr/bin/"
install -m 644 resources/linux/shield.desktop "$APPDIR/usr/share/applications/$APPID.desktop"
install -m 644 resources/linux/shield.desktop "$APPDIR/$APPID.desktop"
# AppStream metadata with this build's version and date (validated by appimagetool when appstreamcli is installed)
RELDATE="$(git log -1 --format=%cs 2> /dev/null || date -u +%F)"
sed -e "s/@VERSION@/$LABEL/" -e "s/@DATE@/$RELDATE/" resources/linux/$APPID.appdata.xml > "$APPDIR/usr/share/metainfo/$APPID.appdata.xml"
for d in resources/icons/hicolor/*/; do install -D -m 644 "$d/apps/shield.png" "$APPDIR/usr/share/icons/hicolor/$(basename "$d")/apps/shield.png"; done
install -m 644 resources/shield_icon_256.png "$APPDIR/shield.png"
ln -sf shield.png "$APPDIR/.DirIcon"
install -m 644 resources/linux/lynx-mime.xml "$APPDIR/usr/share/mime/packages/lynx-mime.xml"
for f in LICENSE THIRD_PARTY.md PRIVACY.md; do install -m 644 "$f" "$APPDIR/usr/share/$f"; done
cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/sh
here="$(dirname "$(readlink -f "$0")")"
exec "$here/usr/bin/Shield" "$@"
EOF
chmod 755 "$APPDIR/AppRun"

TOOL="${APPIMAGETOOL:-$HOME/opt/appimagetool-$APPIMAGETOOL_VERSION-x86_64.AppImage}"
if [[ ! -x "$TOOL" ]]; then
    mkdir -p "$(dirname "$TOOL")"
    curl -fsSL -o "$TOOL" "https://github.com/AppImage/appimagetool/releases/download/$APPIMAGETOOL_VERSION/appimagetool-x86_64.AppImage"
    chmod +x "$TOOL"
fi
# no FUSE needed to run the tool itself (containers, CI)
# update information (AppImageUpdate): the newest release of orugamba-ux/Shield, pre-releases included; appimagetool writes
# the matching .zsync next to the AppImage, and the release job attaches it with the other files in dist/
UPDATE_INFO="${UPDATE_INFO-gh-releases-zsync|orugamba-ux|Shield|latest-all|Shield-*-$ARCH.AppImage.zsync}"
APPIMAGE_EXTRACT_AND_RUN=1 ARCH="$ARCH" "$TOOL" ${UPDATE_INFO:+-u "$UPDATE_INFO"} "$APPDIR" "$OUTDIR/$APPIMAGE" \
    > "$WORK/appimagetool.log" 2>&1 || { cat "$WORK/appimagetool.log"; exit 1; }
if [[ -n "$UPDATE_INFO" && ! -f "$OUTDIR/$APPIMAGE.zsync" ]]; then
    [[ -f "$APPIMAGE.zsync" ]] && mv "$APPIMAGE.zsync" "$OUTDIR/"
    # appimagetool only writes the .zsync when zsyncmake is installed (the release job installs it)
    [[ -f "$OUTDIR/$APPIMAGE.zsync" ]] || ! command -v zsyncmake > /dev/null \
        || { echo "no $APPIMAGE.zsync written"; cat "$WORK/appimagetool.log"; exit 1; }
fi
chmod 755 "$OUTDIR/$APPIMAGE"
# issue #48 (Gear Lever, AppImageUpdate): what they read must stay right. The embedded update information is ours,
# the release asset name matches its file pattern, and the .zsync points at the AppImage beside it.
if [[ -n "$UPDATE_INFO" ]]; then
    if command -v readelf > /dev/null; then
        embedded="$(readelf --string-dump=.upd_info --wide "$OUTDIR/$APPIMAGE" | sed -n 's/^ *\[ *0\] *//p' | sed 's/ *$//')"
        [[ "$embedded" == "$UPDATE_INFO" ]] || { echo "update information is '$embedded', not '$UPDATE_INFO'"; exit 1; }
    fi
    # shellcheck disable=SC2254
    case "$APPIMAGE.zsync" in ${UPDATE_INFO##*|}) ;; *) echo "$APPIMAGE.zsync does not match ${UPDATE_INFO##*|}"; exit 1 ;; esac
    if [[ -f "$OUTDIR/$APPIMAGE.zsync" ]]; then
        url="$(head -c 4096 "$OUTDIR/$APPIMAGE.zsync" | sed -n 's/^URL: //p' | head -1)"
        [[ "$url" == "$APPIMAGE" ]] || { echo "$APPIMAGE.zsync points at '$url'"; exit 1; }
    fi
fi
ls -la "$OUTDIR/$NAME.tar.gz" "$OUTDIR/$APPIMAGE"*
