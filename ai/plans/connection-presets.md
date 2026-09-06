# Plan: Presets für Schraub-/Mutter-/Washer-Verbindungen (Dropdown-Auswahl)

## Ziel/Beschreibung
Aktuell müssen Schrauben-, Mutter- und Washer-Maße (`screw_diameter`, `screw_length`,
`screw_length_tol`, `nut_flat_flat`, `nut_height`, `use_washer`, `washer_diameter`,
`washer_thickness`) bei jeder Verbindung einzeln eingetragen werden (mit Vorschlag aus den zuletzt
verwendeten Werten, siehe Feature `nut-slot-shape`). Der Nutzer möchte stattdessen komplette,
benannte Presets anlegen können (z.B. "M3 Vierkantmutter + Unterlegscheibe"), die er über ein
Dropdown im `TSlotWidget` auswählen kann, um alle zugehörigen Werte auf einen Schlag zu übernehmen.

## Betroffene Dateien/Module (vorläufig)
- Neues Modul, z.B. `lasercut/connectionpresets.py` — Laden/Speichern/Verwalten der Presets.
- `panel/tab.py` (`TSlotWidget`) — Dropdown zur Preset-Auswahl, Buttons zum Speichern/Löschen.
- ggf. `panel/toolwidget.py` — falls neue generische UI-Bausteine nötig sind.
- `docs/interlocking.md` — Dokumentation der neuen Funktion.

## Offene Fragen (bitte vor Umsetzung beantworten)
1. **Umfang eines Presets**: Sollen Presets nur die Schrauben-/Mutter-/Washer-Maße enthalten
   (`screw_diameter`, `screw_length`, `screw_length_tol`, `nut_flat_flat`, `nut_height`,
   `use_washer`, `washer_diameter`, `washer_thickness`), oder auch andere Tab-Eigenschaften wie
   `tabs_number`, `tabs_width`, `dog_bone` etc.?
2. **Speicherort**: Sollen Presets projektübergreifend gelten (z.B. als JSON-Datei im
   FreeCAD-Benutzerverzeichnis, ähnlich Materialien/Makros), oder nur innerhalb des aktuellen
   FreeCAD-Dokuments gespeichert werden (wie die bestehende `PropertiesList`-Serialisierung)?
3. **Verwaltung**: Reicht ein reines "Preset auswählen und anwenden"-Dropdown, oder soll die UI
   auch "aktuelle Werte als neues Preset speichern" und "Preset löschen/umbenennen" anbieten?
4. **Mitgelieferte Presets**: Sollen ein paar Standard-Presets (z.B. für gängige M3/M4/M5-Schrauben
   mit Sechskantmutter) von Anfang an mitgeliefert werden, oder startet die Liste leer und der
   Nutzer legt alles selbst an?
5. **Geltungsbereich der Auswahl**: Gilt das Dropdown nur für den Screw/T-Slot-Verbindungstyp
   (`TSlotWidget`), oder soll ein generisches Preset-System für alle Tab-Typen entstehen?

## Nächster Schritt
Sobald die offenen Fragen beantwortet sind, wird der Plan konkretisiert (Datenformat, UI-Ablauf,
betroffene Dateien) und erneut zur Freigabe vorgelegt, bevor Branch/Umsetzung beginnt.
