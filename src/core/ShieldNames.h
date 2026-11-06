#pragma once

// Shield (a modified version of LYNX SHARE, Copyright (C) 2026 Ka1-S; GNU AGPL-3.0).
// The built-in plugins upstream calls "LYNX <x>" (LYNX Tune, LYNX Synth, LYNX Soundfont, LYNX Kick ...) are
// "Shield <x>" here. Saved projects name plugins by internal ids ("lynxTune"), so they are unaffected; files that name
// a plugin by its display name (preset files, substitute tables, upstream's preset banks) may still say "LYNX <x>".
// currentEngineName maps such an old name to the current one; any other name comes back unchanged.

#include <string>

namespace lynx
{
inline std::string currentEngineName (const std::string& name)
{
    if (name.size() > 5 && (name[0] == 'L' || name[0] == 'l') && (name[1] == 'Y' || name[1] == 'y')
        && (name[2] == 'N' || name[2] == 'n') && (name[3] == 'X' || name[3] == 'x') && name[4] == ' ')
        return "Shield " + name.substr (5);
    return name;
}
} // namespace lynx
