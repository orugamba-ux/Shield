#!/usr/bin/env python3
# Shield rebrand of LYNX SHARE (https://github.com/Ka1-S/LYNX-SHARE).
# Copyright (C) 2026 Ka1-S (LYNX SHARE); rebrand script (C) 2026 the Shield authors. GNU AGPL-3.0.
#
# Re-runnable: apply it to a fresh upstream checkout to bring a newer LYNX release under the Shield brand.
#   python tools/rebrand/shield_rebrand.py [--check]
#
# Rules, deliberately narrow:
# - only names the user sees change; internal ids stay ("lynx_core", LYNX_* env vars, the .lynx extension,
#   saved-project ids such as "lynxTune", the CMake target LYNX, resource file names);
# - file-format headers stay ("LYNX preset", "LYNX theme", "LYNX visualizer", "LYNX-SF-INDEX", the live-session
#   protocol tag and invite-code prefix), so Shield keeps reading what LYNX wrote and stays session-compatible;
# - in C/C++ only string literals are touched; comments that describe the upstream history are left alone;
# - copyright notices and licence files are never touched.
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW_REPO = "orugamba-ux/Shield"

# tokens hidden from every rule (format headers, protocol tags, ids)
PROTECT = [
    # attribution to the original authors (About box, version resources, CMake, store-job note): never rebranded
    r"modified version of LYNX SHARE", r"Ka1-S \(LYNX SHARE[^)]*\)", r"[Bb]ased on LYNX SHARE", r"upstream LYNX SHARE", r"LYNX SHARE by Ka1-S",
    r"LYNX SHARE live host v1", r"LYNX SHARE live session",  # crypto AD / salt: session-compatible with LYNX
    r"LYNX preset", r"LYNX theme", r"LYNX visualizer", r"LYNX-SF-INDEX", r"LYNX-ABCDE",
    r"LYNXvp1", r"LYNX\|RComp", r"LYNX\.LYNX_8wekyb3d8bbwe", r"X-LYNX-", r"LYNX_[A-Za-z0-9_]+",
    r"\"LYNX-\"",  # live-session invite-code prefix (LiveCrypto, LiveSessionUi)
    r"LYNX-[0-9A-Z]{5}-[0-9A-Z]{5}-",  # an invite code itself ("LYNX-2SYQ7-5E66T-..."; tests)
]

COMMON = [
    (r"https://api\.github\.com/repos/Ka1-S/LYNX-SHARE", f"https://api.github.com/repos/{NEW_REPO}"),
    (r"https://github\.com/Ka1-S/LYNX-SHARE/", f"https://github.com/{NEW_REPO}/"),
    (r"LYNX SHARE", "Shield"),
    (r"LYNX%20SHARE", "Shield"),  # URL-encoded (GitHub issue links)
    (r"(?<![/.])LYNX-SHARE/", "Shield/"),  # HTTP user agent
    (r"\bLYNX(\.exe|\.pdb|\.app)\b", r"Shield\1"),
    (r"\bLYNX-(updater|update|cache|sandbox-|ui-session|plugin-thumbs-|symbols|only)", r"Shield-\1"),
    (r"\bLYNX-(?=\d|\$|\{)", "Shield-"),  # release asset names: LYNX-0.1.24-..., LYNX-$VERSION, LYNX-${{ }}
    (r"\bLYNX (Tune|Soundfont|Synth|Kick|Snare|Hat|Clap|Dance|Projects)\b", r"Shield \1"),
    (r"\(LYNX\)", "(Shield)"),
    (r"\bLYNX\.(Project|FLProject)\b", r"Shield.\1"),  # Windows ProgIDs (FileTypes.cpp and the NSIS installer agree)
    (r"Icon=lynx\b", "Icon=shield"),  # the .desktop entry FileTypes.cpp writes on Linux ("\nIcon=": no \b)
    (r"\blynx\.(png|desktop)\b", r"shield.\1"),  # Linux icon / menu entry names (the packages install these)
    (r"\b(To|From) LYNX\b", r"\1 Shield"),
    (r"\bLYNX ASIO\b", "Shield ASIO"),  # the bundled ASIO driver (with its own CLSID: asio/LynxAsio.cpp)
    (r"\blynx-asio", "shield-asio"),  # shield-asio.dll, shield-asio32.dll, the .def file and the build script
]
ASIO_RULES = COMMON[-2:]
# build files where only the ASIO driver is renamed (the rest of them is internal: the LYNX target, lynx_core ...)
ASIO_FILES = ["CMakeLists.txt", "scripts/build-shield-asio.sh", "scripts/build-windows-zig.sh",
              "asio/shield-asio.def", "asio/Register Shield ASIO.bat", "asio/Unregister Shield ASIO.bat"]

# Shield's names for upstream's own effect engines (display names only; projects keep the internal ids such as
# "apexLimiter", and src/core/ShieldNames.h maps the old names in files LYNX wrote). Keep in sync with ShieldNames.h.
PLUGIN_RENAMES = {
    "Apex Limiter": "Bulwark Limiter", "Crest Compressor": "Spearhead Compressor",
    "Prism Multiband": "Mosaic Multiband", "Sentry Gate": "Gatekeeper", "Facet EQ": "Weave EQ",
    "Ridge Strip": "Highland Strip", "Hush De-esser": "Whisper De-esser", "Glow Leveler": "Hearth Leveler",
    "Quell Denoiser": "Calm Denoiser", "Gemini Doubler": "Twin Doubler", "Ember Saturator": "Forge Saturator",
    "Kiln Channel": "Clay Channel", "Aether": "Breath", "Epoch Verb": "Season Verb", "Atrium": "Great Hall",
    "Foil Plate": "Iron Plate", "Nebula": "Night Sky", "Halo": "Sunrise", "Horizon": "Savanna",
    "Echoform": "Echo Drum", "Spiral Echo": "Whirlwind Echo", "Orbit": "Drift", "Lattice Mod": "Weave Mod",
}
PLUGIN_RULES = [(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"(?![A-Za-z0-9_-])", new) for old, new in PLUGIN_RENAMES.items()]
COMMON += PLUGIN_RULES

RAW_RULES = [r for r in COMMON if r[0].startswith(r"\bLYNX (Tune")] + PLUGIN_RULES

CPP_ONLY = [
    (r'^"LYNX/', '"Shield/'),
    (r'^"LYNX"$', '"Shield"'),
    (r'^"LYNX "$', '"Shield "'),
]

CPP_EXT = {".cpp", ".h", ".inc", ".mm", ".c", ".hpp"}
TEXT_EXT = {".txt", ".keys"}
CPP_DIRS = ["src", "tests", "asio"]
I18N_DIR = "resources/i18n"
# (StorePackage.h's "LYNX" is the MSIX <Application Id>; it follows the manifest, which is rebranded too)
CPP_SKIP = {"src/core/ShieldNames.h"}  # the old-name -> new-name table must keep the old names

STRING_RE = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def mask(text):
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return f"\x00{len(saved) - 1}\x00"

    for p in PROTECT:
        text = re.sub(p, keep, text)
    return text, saved


def unmask(text, saved):
    return re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], text)


def apply(rules, s):
    for pat, rep in rules:
        s = re.sub(pat, rep, s)
    return s


def rebrand_literal(lit):
    if "LYNX" not in lit and "lynx." not in lit and "lynx-asio" not in lit and "Icon=lynx" not in lit and not any(o in lit for o in PLUGIN_RENAMES):
        return lit
    masked, saved = mask(lit)
    masked = apply(COMMON, masked)
    masked = apply(CPP_ONLY, masked)
    return unmask(masked, saved)


def rebrand_cpp(text):
    out, i = [], 0
    n = len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(text[i:j]); i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(text[i:j]); i = j
        elif c == "'":
            m = re.compile(r"'(?:[^'\\\n]|\\.)*'").match(text, i)
            j = m.end() if m else i + 1
            out.append(text[i:j]); i = j
        elif c == '"':
            if i > 0 and text[i - 1] == "R":
                # raw string (preset banks, substitute tables): only the plugin names, which those tables look up
                open_paren = text.find("(", i)
                closing = ")" + text[i + 1:open_paren] + '"'
                j = text.find(closing, open_paren)
                j = n if j < 0 else j + len(closing)
                out.append(apply(RAW_RULES, text[i:j])); i = j
                continue
            m = STRING_RE.match(text, i)
            if not m:
                out.append(c); i += 1
                continue
            out.append(rebrand_literal(m.group(0))); i = m.end()
        else:
            j = i + 1
            while j < n and text[j] not in "/\"'":
                j += 1
            out.append(text[i:j]); i = j
    return "".join(out)


def rebrand_text(text):
    masked, saved = mask(text)
    return unmask(apply(COMMON, masked), saved)


# Packaging files (installers, desktop entries, CI): every bare "LYNX" word is the product here, except file names
# inside the repo, version macros and the .lynx file type.
PACKAGING = [
    "scripts/package-linux.sh", "scripts/package-macos.sh", "scripts/make-installer.sh",
    "resources/installer/LYNX.nsi", "resources/LYNX.rc", "resources/msix/AppxManifest.xml.in",
    "resources/linux/shield.desktop", "resources/linux/io.github.orugamba_ux.Shield.appdata.xml",
    "resources/linux/install.sh", "resources/linux/lynx-mime.xml", ".github/workflows/release.yml",
    "scripts/make-msix-layout.py",
]
PACKAGING_PROTECT = [
    r"project\(LYNX", r"\bLYNX(?=\.(?:ico|rc|res|manifest|nsi)\b)", r"LYNX_doc",
    r"x-lynx-project", r"lynx-mime", r"\.lynx\b", r"lynx_(?!share)[a-z0-9_]+", r"Copyright \(C\) 2026 Ka1-S",
    r"juce_add_gui_app\(LYNX", r"--target LYNX\b", r"LYNX_artefacts",
]
PACKAGING_RULES = [
    (r"com\.lynx_share\.LYNX", "io.github.orugamba_ux.Shield"),
    (r"com\.lynx_share", "io.github.orugamba_ux"),
    (r"Ka1-S\|LYNX-SHARE\|", "orugamba-ux|Shield|"),
    (r"Ka1-S/LYNX-SHARE(?![\w)])", NEW_REPO),
    (r"(github\.com|githubusercontent\.com)/Ka1-S/LYNX-SHARE", rf"\1/{NEW_REPO}"),
    (r"\bIcon=lynx\b", "Icon=shield"), (r'(name|stock)(=?"?>?)lynx\b', r"\1\2shield"),
    (r"\blynx\.(png|desktop)\b", r"shield.\1"),
    (r"\bLYNX\b", "Shield"),
]


def rebrand_packaging(text):
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return f"\x00{len(saved) - 1}\x00"

    for p in PROTECT + PACKAGING_PROTECT:
        text = re.sub(p, keep, text)
    text = apply(PACKAGING_RULES[:-1] + COMMON + PACKAGING_RULES[-1:], text)
    return unmask(text, saved)


def main():
    check = "--check" in sys.argv
    changed = []
    for rel in ASIO_FILES:
        p = ROOT / rel
        old = p.read_bytes().decode("utf-8")
        new = apply(ASIO_RULES, old)
        if new != old:
            changed.append(rel)
            if not check:
                p.write_bytes(new.encode("utf-8"))
    for rel in PACKAGING:
        p = ROOT / rel
        old = p.read_bytes().decode("utf-8")
        new = rebrand_packaging(old)
        if new != old:
            changed.append(rel)
            if not check:
                p.write_bytes(new.encode("utf-8"))
    for d in CPP_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            rel = p.relative_to(ROOT).as_posix()
            if p.suffix not in CPP_EXT or rel in CPP_SKIP or not p.is_file():
                continue
            old = p.read_bytes().decode("utf-8", errors="surrogateescape")
            new = rebrand_cpp(old)
            if new != old:
                changed.append(rel)
                if not check:
                    p.write_bytes(new.encode("utf-8", errors="surrogateescape"))
    for p in sorted((ROOT / I18N_DIR).glob("*")):
        if p.suffix not in TEXT_EXT:
            continue
        old = p.read_bytes().decode("utf-8")
        new = rebrand_text(old)
        if new != old:
            changed.append(p.relative_to(ROOT).as_posix())
            if not check:
                p.write_bytes(new.encode("utf-8"))
    print(("would change" if check else "changed"), len(changed), "files")
    for c in changed:
        print("  ", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
