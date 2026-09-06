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

## Offene Fragen (bitte vor Umsetzung beantworten)
1. **Wo einstellen**: Sollen die Werte in FreeCADs nativem Preferences-Dialog (Edit → Preferences →
   eigene LCInterlocking-Seite) liegen, oder in einem eigenen Dialog/Menüpunkt innerhalb des
   Workbenches (ähnlich der neuen Presets-Funktion)?
2. **Art der Werte**: Sollen die Vorgaben feste absolute Werte sein (z.B. immer
   `laser_beam_diameter = 0.15mm`, unabhängig von der Dicke), oder weiterhin ein Verhältnis zur
   Dicke, das der Nutzer nur konfigurierbar macht (z.B. `thickness / X`, `X` einstellbar)?
   Aktuell: `thickness_tolerance = 0.1 * thickness`, `laser_beam_diameter = thickness / 15`.
3. **Geltungsbereich**: Gelten die vordefinierten Werte für alle drei Felder
   (`thickness_tolerance`, `laser_beam_diameter`, `hole_width_tolerance`) gleichermaßen, oder gibt
   es Unterschiede (z.B. `hole_width_tolerance` bleibt bei 0.0 als Standard)?
4. **Bestehende Materialien**: Wirken sich neue Standardwerte nur auf neu angelegte Materialien
   aus (wie bisher das `hasattr`-Verhalten), oder soll es auch eine Möglichkeit geben, bestehende
   Materialien nachträglich auf die neuen Standardwerte zurückzusetzen?

## Nächster Schritt
Sobald die offenen Fragen beantwortet sind, wird der Plan konkretisiert (Datenformat, UI-Ablauf,
betroffene Dateien) und zur Freigabe vorgelegt, bevor ein Feature-Branch angelegt wird.
