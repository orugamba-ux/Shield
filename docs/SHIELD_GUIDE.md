# Shield user guide

This guide covers installing Shield, finding your way around it, making a first beat, and adding instruments,
effects and third-party plugins. It ends with what every built-in effect does and when to reach for it.

---

## 1. Install

| System | File | How |
|---|---|---|
| **Windows 10 / 11** | `Shield-<version>-setup-x64.exe` | Run it. It installs for your user only, no admin rights. If SmartScreen says "Windows protected your PC", choose **More info → Run anyway** (the build isn't code-signed yet). |
| Windows, no install | `Shield-<version>-windows-x64.zip` | Unzip it anywhere and run `Shield.exe`. |
| **macOS 11 or newer** (Apple Silicon and Intel) | `Shield-<version>-macos-universal.dmg` | Open it and drag **Shield** to **Applications**. The first time, Control-click (right-click) Shield in Applications, choose **Open**, then **Open** again. On macOS 15 or newer, go to **System Settings → Privacy & Security → Open Anyway** instead. |
| **Linux** (x86_64; Ubuntu 22.04+, Debian 12+, Fedora 36+, Arch) | `Shield-<version>-x86_64.AppImage` | Make it executable (`chmod +x Shield-*.AppImage`), then double-click or run it. |
| Linux, per-user install | `Shield-<version>-linux-x86_64.tar.gz` | Extract it and run `./install.sh`. Shield then appears in your applications menu. `./install.sh --uninstall` removes it. |

### First start

A short **setup wizard** opens the first time. You can skip it and reopen it later from **Options → Setup wizard...**.
It:

1. picks the language,
2. tests your audio device (you should hear a short sound),
3. lists your plugin folders and scans them in the background.

The installers also include a demo song, `Demo.lynx`. Open it with **File → Open...** and press **Space** to hear it.

---

## 2. The five windows

| Key | Window | What it's for |
|---|---|---|
| **F6** | **Channel Rack** | Your sounds (instruments and samples), one row each, plus the step sequencer for drums. |
| **F7** | **Piano Roll** | Draw melodies, chords and basslines for the selected channel. |
| **F5** | **Playlist** | Arrange the song: place patterns, audio and automation clips in time. |
| **F9** | **Mixer** | Volume, pan and **effects** for every track, and the routing between them. |
| **Alt+F8** | **Browser** | Samples, presets, plugins and the parts of your project. Drag things from here. |
| **F8** | **Plugin picker** | Every instrument and effect, grouped in tabs. Press F8 again to close it. |

**Pattern or song.** **PAT** mode loops the current pattern, which is good while you build a beat. **SONG** mode plays
the Playlist arrangement. Press **L** to switch.

---

## 3. Make your first beat (5 minutes)

1. **File → New** (Ctrl+N). Set the tempo in the toolbar, for example 120 BPM, or 100–110 for Afrobeat.
2. Press **F6** to open the Channel Rack. A new project starts with five channels: **Kick**, **Clap**, **Hat** and
   **Snare** (Shield's built-in drums) and **Synth** (Shield Synth).
3. **Click the steps** to switch them on. Each step is a 16th note. A simple start:
   - Kick on steps 1, 5, 9, 13 (four on the floor);
   - Clap on 5 and 13;
   - Hat on 3, 7, 11, 15.
4. Press **Space** to play. Change the steps while it plays.
5. **Add a bassline:** select the **Synth** row, press **F7** and draw notes in the Piano Roll (left-click draws,
   right-click deletes). For more instruments, use the **Add** menu or press **F8**.
6. **Arrange:** press **F5**, switch to **SONG** mode (**L**), and click in the Playlist to place your pattern. Make a
   second pattern with **F4** (the next empty pattern) for a variation, and place them one after the other.
7. **Save** with **Ctrl+S**. Projects are `.lynx` files, and Shield also autosaves.
8. **Export** with **Ctrl+R**: WAV, FLAC or OGG, the whole song or the pattern.

> Tip: **Ctrl+T** turns your computer keyboard into a piano (the `Z`…`M` and `Q`…`P` rows) for the selected channel.

---

## 4. Instruments

Add an instrument with **Add**, with **F8** (the plugin picker), or by dragging one from the Browser onto the Channel Rack.

| Instrument | What it is |
|---|---|
| **Shield Synth** | A 3-oscillator synth with filter, envelopes, LFOs, FM, ring mod, mono and portamento. Good for basses, leads and pads. |
| **Shield Soundfont** | Plays SF2/SF3 SoundFont files, with a preset search across all your SoundFonts. Pianos, strings, guitars, brass. |
| **Shield Kick / Snare / Hat / Clap** | Built-in drum synths, tweakable in their windows. |
| **Sampler** | Drop any audio file on a channel. It supports zones, slices and time-stretch that follows the tempo. |
| FL Studio-compatible generators (3x Osc, FL Keys, …) | Used when you open FL projects, and available for new channels too. |

Click a channel's name to open its window (sound settings and the instrument's controls).

---

## 5. Effects: how to add them

Effects live on **Mixer tracks** ("inserts"). Every insert has **10 effect slots**, processed from top to bottom.

1. **Send a channel to a mixer track.** In the Channel Rack, every channel has a small number box (its mixer insert).
   Drag on it, or select the channel, then the insert in the Mixer. The channel's sound now goes through that track.
2. Press **F9** to open the Mixer and click the track.
3. **Click an empty slot** on the right of the Mixer and pick an effect (or select the track and press **F8**).
4. The effect's window opens. Turn the knobs while the music plays.
5. Each slot has an **on/off** switch and a **mix** knob (dry/wet). Drag slots to change their order.

**Typical order on a vocal or instrument track:** Gatekeeper (noise gate) → Weave EQ (clean up) → Spearhead Compressor
(even out) → Whisper De-esser (tame "s" sounds) → Forge Saturator (warmth) → Echo Drum / Season Verb (space).

**On the Master track** (the last stage before export): Weave EQ (gentle tone) → Mosaic Multiband (glue) →
**Bulwark Limiter** last (loudness and no clipping).

**Sends** (one reverb for many tracks): put a reverb on its own mixer track and set its mix to 100 %. Select a source
track, then click the small send switch at the bottom of the reverb's track. The send level sets how much goes in.
A send at level 0 is a **sidechain**, which is how you make a bass duck when the kick hits (put Spearhead Compressor on
the bass and choose the kick's track as its side-chain input).

---

## 6. Third-party plugins (VST3, CLAP)

Shield hosts **VST3** and **CLAP** plugins on every system, plus **VST2** on Windows and Linux, **Audio Units** on macOS
and **LV2** on Linux.

1. **Install the plugin** with its own installer. It goes into the standard folder:

   | System | VST3 | CLAP |
   |---|---|---|
   | Windows | `C:\Program Files\Common Files\VST3` | `C:\Program Files\Common Files\CLAP` |
   | macOS | `/Library/Audio/Plug-Ins/VST3` (or `~/Library/...`) | `/Library/Audio/Plug-Ins/CLAP` |
   | Linux | `~/.vst3` or `/usr/lib/vst3` | `~/.clap` or `/usr/lib/clap` |

2. In Shield, open **Options → Plugin manager...**:
   - **Plugin folders...** adds a folder if your plugin is somewhere else;
   - **Scan for plugins** finds the new ones (it runs in the background).
3. The plugin now appears in the **F8** plugin picker and the Browser's **Plugin database** (**Shift+F8**). An
   instrument goes on the **Channel Rack**; an effect goes in a **Mixer slot**, exactly like the built-in ones.
4. Mark favourites in the picker to find them quickly.

**If a plugin crashes:** in **Options → General settings...**, switch on *Run plugins in a separate process*. A crashing
plugin then goes silent instead of closing Shield (Windows and Linux).

**Opening a project from someone else:** if a plugin is missing, Shield tells you which one. For many popular commercial
effects it automatically uses the closest **built-in Shield effect** (the table below lists which), and keeps the
original's settings for when you install it.

---

## 7. What each built-in effect does

### Dynamics: level and punch

| Effect | What it does | Use it for |
|---|---|---|
| **Bulwark Limiter** | A transparent mastering limiter: look-ahead, a true-peak ceiling and four styles. | Last on the Master: makes the mix loud without clipping. Set the ceiling to about −1 dB. |
| **Spearhead Compressor** | A style compressor with 11 characters, knee, look-ahead, a side-chain EQ and a live gain-reduction graph. | Drums, vocals, bass, the mix bus, and sidechain pumping. |
| **Mosaic Multiband** | 4-band dynamics: compresses or expands each frequency range separately. | Glue on the Master, controlling a boomy low end, de-harshing. |
| **Gatekeeper** | A gate and expander that cuts sound below a threshold (five styles, hold, side-chain filters). | Removing background noise between vocal phrases; tightening drums. |
| **Hearth Leveler** | A smooth "optical" leveler: gentle, musical compression. | Vocals and bass that need evening out without sounding squashed. |
| **Whisper De-esser** | Turns down harsh "s" and "sh" sounds only. | Vocals after compression. |

### EQ and channel

| Effect | What it does | Use it for |
|---|---|---|
| **Weave EQ** | A precise 8-band EQ: bells, shelves, notches and steep cuts, with zero latency. | Cutting mud (200–400 Hz), removing rumble (high-pass under 30–80 Hz), adding presence. |
| **Highland Strip** | A console channel strip: filters, 4-band EQ, compressor and gate in one. | A complete track in one plugin, with an analog-desk feel. |
| **Clay Channel** | A console channel with six console models, drive and noise. | Analog colour on many tracks. |
| **Breath** | An "air" EQ: a broad high shelf plus a harmonic exciter. | Making vocals and hats sparkle. |
| **Parametric EQ** | A 7-band EQ you drag on a graph (FL-compatible). | Everyday EQ. |

### Colour and saturation

| Effect | What it does | Use it for |
|---|---|---|
| **Forge Saturator** | Tube, tape, transistor and fuzz saturation, up to four bands, with auto gain. | Warmth on bass and drums, grit on vocals, making 808s audible on small speakers. |

### Reverb: space

| Effect | What it does | Use it for |
|---|---|---|
| **Season Verb** | 22 vintage-digital reverb algorithms (halls, plates, rooms, chorused spaces) with 1970s, 1980s or modern colour. | An all-round lush reverb. |
| **Great Hall** | Rooms and chambers with separate early and late reflections. | Realistic rooms for drums and live instruments. |
| **Iron Plate** | A bright plate reverb that speaks at once. | Classic vocal and snare reverb. |
| **Night Sky** | Huge delay and reverb networks with feedback, density and warp. | Ambient pads, long tails, sound design. |
| **Sunrise** | A shimmer reverb that pitch-shifts the tail up or down. | Dreamy, angelic pads and intros. |
| **Savanna** | Echo going into, or after, a reverb: tape, analog, reverse and octave echoes. | Big atmospheric vocal throws and transitions. |
| **Reeverb 2**, **LuxeVerb** | FL-compatible algorithmic reverbs. | Everyday reverb, and FL projects. |

### Delay and modulation: movement

| Effect | What it does | Use it for |
|---|---|---|
| **Echo Drum** | A multi-mode echo: tape, bucket brigade, analog, digital, pitch and reverse, tempo-synced. | Vocal echoes on the beat, dub delays, slap-back. |
| **Whirlwind Echo** | Each repeat is frequency-shifted, spiralling up or down. | Psychedelic risers and FX. |
| **Drift** | A modulation machine: flangers, choruses, doubler, ensemble. | Widening synths and guitars, movement. |
| **Weave Mod** | A multi-tap modulated delay (1–16 taps) with detune, diffusion and drive. | Thick stereo textures and chorus-like spreads. |
| **Fruity Delay 3** | An analog-style delay (FL-compatible). | Everyday delay. |

### Voice

| Effect | What it does | Use it for |
|---|---|---|
| **Shield Tune** | Real-time pitch correction: key and scale, retune speed from natural to the hard "robot" effect, formant preserve, MIDI target notes. | Tuning vocals, or the Afrobeats and trap auto-tune effect (fast retune, the song's key). |
| **Twin Doubler** | Two extra voices with their own delay, detune, pan and an octave-down switch. | Thick, wide vocals and hooks from one take. |
| **Calm Denoiser** | A one-knob noise remover; **Listen** plays what it takes away. | Fan or room hiss on home recordings. |

### Utilities

**Utility** (gain and pan), **Stereo Shaper** (width and mid/side), **Wave Candy** (meters, spectrum and
oscilloscope), **Tuner**, **Visualizer** (audio-reactive video you can export), **Gross Beat** (stutters, gates, tape
stops), **Patcher** (wire several effects and instruments into one chain), and **Hardware Insert** (send audio to
outboard gear).

---

## 8. Record audio and MIDI

- **MIDI keyboard:** plug it in. **Options → MIDI settings...** (F10) lists it. Select a channel and play. Press **R**
  (record on), then **Space**, and the notes go into the pattern.
- **Microphone or guitar:** **Options → Audio settings...** chooses the input. In the Mixer, select a track and use
  **Tools → One-click audio recording: arm the selected insert...**. Press **R**, then **Space**. In SONG mode each take
  becomes an audio clip in the Playlist.
- **Metronome:** Ctrl+M. **Count-in:** Ctrl+P.

### Low latency on Windows: Shield ASIO

**Options → Audio settings...** → driver **ASIO** → device **Shield ASIO** works with any sound card and gives low
latency for recording. **Driver settings...** chooses shared mode (other apps keep playing) or exclusive mode (lowest
latency). To use Shield ASIO in other programs too, run **Register Shield ASIO.bat** from Shield's install folder
(`%LOCALAPPDATA%\Programs\Shield`). It asks for admin rights.

---

## 9. FL Studio projects

**File → Open...** an `.flp`. Shield converts the channels, samples, patterns, arrangement, automation and mixer, and
most of FL's native plugins with their settings. A report lists anything approximated or left out. If FL Studio is
installed on the same PC, Shield also finds its samples and plugins.

---

## 10. Make it yours

- **Theme:** **Options → Theme (colors, background)...**. The default is **Shield** gold on navy, and **Crimson**,
  **Ocean**, **Emerald**, **Amber**, **Violet** and **Graphite** are built in. You can pick your own accent, background
  or wallpaper image.
- **Language:** 15 languages, including English, French and Portuguese, in **Options → General settings...**.
- **Shortcuts:** every key can be changed in the settings.

---

## 11. Shortcuts

| Key | Action |
|---|---|
| Space | Play / stop |
| L | Pattern / song mode |
| F5 / F6 / F7 / F9 | Playlist / Channel Rack / Piano Roll / Mixer |
| F8 | Plugin picker (Alt+F8: Browser, Shift+F8: plugin database) |
| F4 | Next empty pattern |
| R | Recording on/off |
| Ctrl+M / Ctrl+P | Metronome / count-in |
| Ctrl+T | Computer keyboard as a piano |
| Ctrl+Z / Ctrl+Y | Undo / redo |
| Ctrl+N / Ctrl+O / Ctrl+S | New / open / save |
| Ctrl+R | Export audio |
| F12 | Close all plugin and tool windows |

---

## 12. Troubleshooting

| Problem | Fix |
|---|---|
| No sound | **Options → Audio settings...**: choose your output device. On Windows, try **Shield ASIO** or *Windows Audio*. |
| Crackles or dropouts | Raise the buffer size in Audio settings (256 or 512 samples), or switch on **Tools → Switch smart disable for all plugins**. |
| A plugin is missing | **Options → Plugin manager... → Scan for plugins**. Check that the plugin is VST3 or CLAP, 64-bit, and in a listed folder. |
| A plugin crashes Shield | Switch on *Run plugins in a separate process* in **Options → General settings...**. |
| macOS says Shield "is damaged" or "can't be opened" | Control-click → **Open**, or run `xattr -dr com.apple.quarantine /Applications/Shield.app` in Terminal. |
| Something else | **Help → Report a problem...** opens a GitHub issue with the details filled in. |

---

<sub>Shield is free software under the GNU AGPL-3.0, based on LYNX SHARE by Ka1-S. FL Studio is a trademark of
Image-Line Software; Shield is not affiliated with it.</sub>
