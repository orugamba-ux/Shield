<p align="center">
  <img src="resources/shield_icon_256.png" alt="Shield icon: a shield with imigongo patterns over two crossed spears" width="128" height="128">
</p>

<h1 align="center">Shield</h1>

<p align="center"><strong>A lightweight music production studio for Windows, macOS and Linux.</strong><br>
Channel Rack, Piano Roll, Playlist and Mixer, with built-in instruments and effects, and it opens FL Studio projects.</p>

---

## Features

- **Channel Rack:** a step sequencer with patterns, swing, cut groups and an arpeggiator. The PC keyboard plays as a piano.
- **Piano Roll:** snap, chords and scales, note colours, quantize, slide and porta notes, and `.mid` import and export.
- **Playlist:** pattern, audio and automation clips across arrangements.
- **Mixer:** up to 127 inserts, sends, 10 effect slots per track, sidechain and delay compensation.
- **FL Studio projects:** opens `.flp` files, including their channels, samples, patterns, arrangement, automation and mixer.
- **Plugins:** hosts VST3 and CLAP, and on Windows comes with its own **Shield ASIO** driver for low-latency audio
  on any device.
- **Live sessions:** make music with someone else over the internet, end-to-end encrypted.

## Built-in plugins

| Kind | Shield plugins |
|---|---|
| Dynamics | Bulwark Limiter · Spearhead Compressor · Mosaic Multiband · Gatekeeper · Hearth Leveler · Whisper De-esser |
| EQ and channel | Weave EQ · Highland Strip · Clay Channel |
| Colour | Forge Saturator · Breath |
| Reverb | Season Verb · Great Hall · Iron Plate · Night Sky · Sunrise · Savanna |
| Delay and modulation | Echo Drum · Whirlwind Echo · Drift · Weave Mod |
| Voice | Shield Tune · Twin Doubler · Calm Denoiser |
| Instruments | Shield Synth · Shield Soundfont · Shield Kick, Snare, Hat and Clap |

Shield also includes clean-room versions of FL Studio's native plugins, so imported FL projects sound the same.
They keep FL Studio's names so that imports can match them.

## Download

Installers for Windows (setup or portable zip), macOS (universal `.dmg`) and Linux (`.AppImage` or `.tar.gz`) are on
the [Releases](https://github.com/orugamba-ux/Shield/releases) page. Every build is also attached to its run of the
**Release** workflow on the [Actions](https://github.com/orugamba-ux/Shield/actions) tab.

The Windows build is not code-signed yet. If SmartScreen says "Windows protected your PC", choose
**More info → Run anyway**.

## Building

The **Release** workflow (`.github/workflows/release.yml`) builds all three platforms: run it from the Actions tab.

To build locally with CMake 3.22 or newer and a C++20 compiler:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

- **Windows:** use Visual Studio 2022 Build Tools ("Desktop development with C++") with
  `-G "Visual Studio 17 2022" -A x64`, or cross-compile from Linux/WSL with `scripts/build-windows-zig.sh`.
- **macOS:** needs the Xcode command line tools. Add `-DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"` for a universal app.
- **Linux:** the packages to install are listed in [docs/LYNX_SHARE_README.md](docs/LYNX_SHARE_README.md#linux).

The core tests need no JUCE: `./scripts/build-local.sh`.

---

## Credits and licence

Shield is based on [LYNX SHARE](https://github.com/Ka1-S/LYNX-SHARE) by Ka1-S, Copyright (C) 2026 Ka1-S. The changes
are © 2026 the Shield contributors and are listed in [SHIELD.md](SHIELD.md). The original project's documentation is
in [docs/](docs/LYNX_SHARE_README.md).

Shield is free software under the [GNU Affero General Public License v3.0](LICENSE). You may use, study, modify and
share it, as long as you share its source code under the same licence. It comes WITHOUT ANY WARRANTY. Third-party
components and their licences are listed in [THIRD_PARTY.md](THIRD_PARTY.md).

FL Studio is a registered trademark of Image-Line Software. VST is a registered trademark of Steinberg Media
Technologies GmbH. Shield is not affiliated with either.
