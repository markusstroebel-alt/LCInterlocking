# Memory: material-tolerance-defaults

## Status
- Plan finalisiert: [material-tolerance-defaults.md](./material-tolerance-defaults.md)
- Branch `feature/material-tolerance-defaults` angelegt (basiert auf `feature/connection-presets`,
  welches auf `feature/nut-slot-shape`, welches auf `develop` basiert).

## Todo
- [x] `lasercut/preferences.py` (neu): ParamGet-Zugriff für die drei Default-Werte
- [x] `panel/preferencespage.py` (neu): Preferences-Seite (loadSettings/saveSettings)
- [x] `InitGui.py`: Preferences-Seite registriert
- [x] `lasercut/material.py`: Defaults aus `lasercut.preferences` statt fester Formeln
- [x] `panel/partmat.py`: "Reset tolerances to defaults"-Button
- [x] `docs/interlocking.md`: Dokumentation ergänzt
- [ ] Manuell in FreeCAD testen (FreeCAD hier nicht verfügbar)
- [x] Feature-README finalisiert

## Entscheidungen/Notizen
- Preferences-Gruppe: `User parameter:BaseApp/Preferences/Mod/LCInterlocking`
- Keys (Vorschlag): `ThicknessTolerance`, `LaserBeamDiameter`, `HoleWidthTolerance` (jeweils Float,
  in mm, absolute Werte).
- Start-Fallback-Werte, falls Preferences noch nie gesetzt wurden: 0.1mm / 0.1mm / 0.0mm
  (willkürlicher Startwert, da absolute Werte jetzt unabhängig von thickness sind — Nutzer soll sie
  in den Preferences an die eigene Maschine/Material anpassen).
- Reset-Button wirkt nur auf das aktuell im Panel bearbeitete Material (setzt die drei
  Eingabefelder auf die aktuellen Preference-Werte; Übernahme erfolgt wie bei jeder Feldänderung
  erst beim Bestätigen/OK des Panels).
