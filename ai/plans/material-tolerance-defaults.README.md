# Feature: Vordefinierbare Material-Toleranzen

## Zweck
Die drei Toleranzwerte, die bisher immer aus der Materialdicke berechnet wurden
(`thickness_tolerance`, `laser_beam_diameter`, `hole_width_tolerance`), können jetzt zentral in den
FreeCAD-Einstellungen als feste, absolute Werte vordefiniert werden.

## Nutzung
Unter **Edit → Preferences → LCInterlocking** gibt es drei Felder:
- **Thickness tolerance** (mm)
- **Laser beam diameter** (mm)
- **Slot width tolerance** (mm)

Neu angelegte Materialien im Interlocking-Panel übernehmen diese Werte automatisch als Startwert
(weiterhin pro Material frei editierbar). Für bereits bestehende Materialien gibt es im
Material-Panel einen Button **"Reset tolerances to defaults"**, der die drei Felder auf die
aktuellen Einstellungswerte zurücksetzt.

## Relevante Dateien
- `lasercut/preferences.py` — Lesen/Schreiben der Einstellungswerte
- `panel/preferencespage.py` — Preferences-Seite
- `InitGui.py` — Registrierung der Preferences-Seite
- `lasercut/material.py` — Defaults für neue Materialien
- `panel/partmat.py` — Reset-Button
- `docs/interlocking.md` — Dokumentation
