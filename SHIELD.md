# Shield: a modified version of LYNX SHARE

Shield is a rebranded fork of [LYNX SHARE](https://github.com/Ka1-S/LYNX-SHARE), the open-source DAW by Ka1-S.
LYNX SHARE is Copyright (C) 2026 Ka1-S and is licensed under the [GNU Affero General Public License v3.0](LICENSE).
Shield is distributed under the same licence. Its complete source code, including these modifications, is at
https://github.com/orugamba-ux/Shield. The third-party components and their licences are listed in
[THIRD_PARTY.md](THIRD_PARTY.md).

## What this fork changed (2026-11-06, from upstream LYNX SHARE 0.1.24, commit 2b77285)

- **Name.** The product is called **Shield** everywhere a user sees it: the window title, About box, installers,
  desktop entries, the macOS bundle name, the Windows version resource, menus and messages. The binaries are
  `Shield.exe`, `Shield.app` and `Shield`. Internal identifiers keep their upstream names: the `lynx_core` library, the
  `LYNX_*` environment variables, the CMake target `LYNX`, and the source and resource file names.
- **Icon.** The icon is original artwork: a leaf-shaped shield with imigongo zigzags over two crossed spears. It is
  drawn by `tools/rebrand/make_shield_icon.py`, which also makes the splash figure and the embedded logo.
- **Built-in plugins.** Upstream's "LYNX …" plugins are now "Shield …": Shield Tune, Shield Synth, Shield Soundfont,
  and the Shield Kick, Snare, Hat and Clap. The other plugin names are unchanged.
- **Settings and data folders.** These are now `Shield` (for example `%APPDATA%\Shield` and `~/Documents/Shield/Projects`),
  so Shield and LYNX SHARE can be installed side by side.
- **Bundle and app ids.** The macOS bundle id is `io.github.orugamba-ux.shield`, the AppStream id is
  `io.github.orugamba_ux.Shield`, and the Windows ProgIDs are `Shield.Project` and `Shield.FLProject`.
- **Updates.** The in-app update check and the AppImage update information point at this fork's GitHub releases.
- **Crash reports.** Shield has no default crash-report server, so nothing goes to upstream's `lynx-share.com`. Reports
  stay on disk, and *Help > Report a problem...* opens a GitHub issue on this fork. To use a server of your own, set
  `LYNX_CRASH_ENDPOINT`.
- **Microsoft Store.** The Store submission job in `.github/workflows/release.yml` is switched off, because it targets
  upstream's Store product.

## What stays compatible

- **Projects.** `.lynx` projects open in both apps. Projects store plugins by internal id (for example `lynxTune`), not
  by display name.
- **Presets and themes.** LYNX presets, themes and visualizer presets load in Shield, because their file headers are
  unchanged. Old names such as "LYNX Tune" in preset files and substitute tables are mapped to the new ones
  (`src/core/ShieldNames.h`).
- **Live sessions.** Live sessions use the same protocol and invite-code format as LYNX SHARE, and still connect
  through upstream's relay (`relay.lynx-share.com`). If you run your own relay, set `LYNX_RELAY_URL`. AGPL section 13
  applies to whoever operates a modified relay.

## Re-applying the rebrand to a newer LYNX release

```bash
git fetch upstream && git merge upstream/main     # resolve conflicts, then:
python tools/rebrand/shield_rebrand.py             # idempotent: names, URLs, packaging
python tools/rebrand/make_shield_icon.py           # needs Pillow
```
