#pragma once

// Shield's names for the built-in engines. Saved projects name plugins by internal ids ("apexLimiter", "lynxTune"),
// so a rename never breaks them; files that name a plugin by its display name (preset files, substitute tables,
// banks written by the upstream engine) may still use an older name. currentEngineName maps such a name to the current
// one (case-insensitive); any other name comes back unchanged. Keep in sync with tools/rebrand/shield_rebrand.py.

#include <algorithm>
#include <cctype>
#include <string>
#include <utility>

namespace lynx
{
inline std::string currentEngineName (const std::string& name)
{
    static const std::pair<const char*, const char*> renamed[] = {
        { "Apex Limiter", "Bulwark Limiter" },   { "Crest Compressor", "Spearhead Compressor" },
        { "Prism Multiband", "Mosaic Multiband" }, { "Sentry Gate", "Gatekeeper" },
        { "Facet EQ", "Weave EQ" },              { "Ridge Strip", "Highland Strip" },
        { "Hush De-esser", "Whisper De-esser" }, { "Glow Leveler", "Hearth Leveler" },
        { "Quell Denoiser", "Calm Denoiser" },   { "Gemini Doubler", "Twin Doubler" },
        { "Ember Saturator", "Forge Saturator" }, { "Kiln Channel", "Clay Channel" },
        { "Aether", "Breath" },                  { "Epoch Verb", "Season Verb" },
        { "Atrium", "Great Hall" },              { "Foil Plate", "Iron Plate" },
        { "Nebula", "Night Sky" },               { "Halo", "Sunrise" },
        { "Horizon", "Savanna" },                { "Echoform", "Echo Drum" },
        { "Spiral Echo", "Whirlwind Echo" },     { "Orbit", "Drift" },
        { "Lattice Mod", "Weave Mod" },
    };
    const auto lower = [] (std::string s) {
        std::transform (s.begin(), s.end(), s.begin(), [] (unsigned char c) { return (char) std::tolower (c); });
        return s;
    };
    const auto wanted = lower (name);
    for (const auto& [from, to] : renamed)
        if (wanted == lower (from))
            return to;
    if (wanted.size() > 5 && wanted.compare (0, 5, "lynx ") == 0) // "LYNX Tune" -> "Shield Tune"
        return "Shield " + name.substr (5);
    return name;
}
} // namespace lynx
