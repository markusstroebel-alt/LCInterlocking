# Plan: Vordefinierbare Material-Toleranzen (Einstellungen)

## Ziel/Beschreibung
Aktuell werden `thickness_tolerance` (Default `0.1 * thickness`), `laser_beam_diameter` (Default
`thickness / 15`) und `hole_width_tolerance` (Default `0.0`) in `lasercut/material.py`
(`MaterialProperties.__init__`) immer aus fest einprogrammierten Formeln/Werten berechnet, sobald
ein neues Material/Teil angelegt wird. Der Nutzer möchte diese drei Standardwerte selbst in den
Einstellungen vordefinieren können, sodass neue Materialien direkt seine bevorzugten Werte
verwenden statt der einprogrammierten Defaults.

## Betroffene Dateien/Module (vorläufig)
- Neues Modul oder Erweiterung von `lasercut/presets.py` bzw. eigenes `lasercut/settings.py` für
  die Persistenz der Standardwerte.
- `lasercut/material.py` (`MaterialProperties.__init__`) — Defaults aus den Einstellungen lesen
  statt der festen Formeln.
- UI: neue Einstellungsmöglichkeit (z.B. eigener Dialog/Menüpunkt in `InitGui.py`/`panel/`, oder
  FreeCADs natives Preferences-System unter Edit → Preferences).

## Geplantes Vorgehen (konkretisiert nach Antworten)
1. Neues Modul `lasercut/preferences.py`:
   - `get_param_group()` — `FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/LCInterlocking")`.
   - `get_default_thickness_tolerance()`, `get_default_laser_beam_diameter()`,
     `get_default_hole_width_tolerance()` — lesen absolute Werte aus dem ParamGet, mit
     Fallback-Startwert (z.B. `0.1mm`, `0.1mm`, `0.0mm`), falls noch nichts eingestellt wurde.
   - `set_defaults(thickness_tolerance, laser_beam_diameter, hole_width_tolerance)` zum Schreiben.
2. `panel/preferencespage.py` (neu): `LCInterlockingPreferencesPage(QtGui.QWidget)` mit
   `loadSettings()`/`saveSettings()` (FreeCADs Standard-Mechanismus für Preference-Seiten), je ein
   `QDoubleSpinBox` für die drei absoluten Werte.
3. `InitGui.py`: Seite via `FreeCADGui.addPreferencePage(LCInterlockingPreferencesPage,
   "LCInterlocking")` registrieren, damit sie unter Edit → Preferences → LCInterlocking erscheint.
4. `lasercut/material.py` (`MaterialProperties.__init__`): Defaults für `thickness_tolerance`,
   `laser_beam_diameter`, `hole_width_tolerance` aus `lasercut.preferences` lesen statt der
   bisherigen Formeln (`0.1 * thickness`, `thickness / 15`, `0.0`).
5. `panel/partmat.py` (`Part`-Widget): neuer Button "Reset tolerances to defaults", der die drei
   Felder des *aktuell bearbeiteten* Materials auf die Einstellungswerte zurücksetzt (deckt Punkt 4
   der Fragen ab: nachträgliches Zurücksetzen bestehender Materialien).
6. `docs/interlocking.md` um Hinweis auf die neue Preferences-Seite ergänzen.

## Betroffene Dateien/Module
- `lasercut/preferences.py` (neu)
- `panel/preferencespage.py` (neu)
- `InitGui.py`
- `lasercut/material.py`
- `panel/partmat.py`
- `docs/interlocking.md`

## Entschiedene Punkte (vom Nutzer beantwortet)
1. **Wo einstellen**: FreeCADs natives Preferences-System (Edit → Preferences → LCInterlocking).
2. **Art der Werte**: feste absolute Werte (kein Verhältnis zur Dicke mehr).
3. **Geltungsbereich**: alle drei Felder (`thickness_tolerance`, `laser_beam_diameter`,
   `hole_width_tolerance`).
4. **Bestehende Materialien**: zusätzlicher "Reset tolerances to defaults"-Button im
   Material-Panel, um bestehende Materialien nachträglich auf die Einstellungswerte zu setzen.

## Nächster Schritt
Freigabe durch Nutzer abwarten, dann Feature-Branch `feature/material-tolerance-defaults` anlegen
und feingranular umsetzen.
