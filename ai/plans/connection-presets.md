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

## Geplantes Vorgehen (konkretisiert nach Antworten)
1. Neues Modul `lasercut/presets.py`:
   - `get_presets_file_path()` — JSON-Datei im FreeCAD-Benutzerverzeichnis
     (`FreeCAD.getUserAppDataDir() + "LCInterlocking_presets.json"`), projektübergreifend.
   - `load_presets()` / `save_presets(presets)` — Laden/Schreiben der kompletten Datei.
   - Datenformat: `{"<tab_type>": [{"name": "...", "values": {"<property>": <value>, ...}}, ...]}`,
     gruppiert nach `tab_type` (z.B. `TabProperties.TYPE_T_SLOT`), damit nur zum jeweiligen
     Verbindungstyp passende Presets angezeigt werden.
   - `add_or_update_preset(tab_type, name, values)`, `delete_preset(tab_type, name)`,
     `get_presets_for_type(tab_type)`.
2. `panel/toolwidget.py` (`ParamWidget`, generisch für alle Tab-Typen — einfacher als
   typ-spezifische Lösung und automatisch für `TabWidget`, `TSlotWidget`,
   `TabContinuousWidget`, `TabFlexWidget` nutzbar):
   - Neue Preset-Zeile oberhalb der bestehenden Felder: Dropdown (Presets für den aktuellen
     `tab_type`), Button "Save as..." (Name abfragen, aktuelle Feldwerte als neues Preset
     speichern/überschreiben), Button "Delete" (aktuell gewähltes Preset löschen).
   - Beim Auswählen eines Presets: alle in `values` enthaltenen Properties auf die entsprechenden
     Widgets übertragen (nur wenn der Widget-Name im aktuellen `widget_list` existiert — andere
     Tab-Typen mit anderen Feldern werden dadurch automatisch ignoriert) und Sichtbarkeit
     aktualisieren (`listchangeIndex`). Werte bleiben danach normal editierbar (kein Lock).
   - Presets speichern *alle* aktuell sichtbaren Felder des Widgets (nicht nur
     Schrauben-/Mutter-/Washer-Werte), gemäß Antwort zu Frage 1.
3. `docs/interlocking.md` um Kurzbeschreibung der Preset-Funktion ergänzen.

## Betroffene Dateien/Module
- `lasercut/presets.py` (neu)
- `panel/toolwidget.py`
- `docs/interlocking.md`

## Entschiedene Punkte (vom Nutzer beantwortet)
1. **Umfang**: Presets enthalten alle Felder des jeweiligen Widgets, bleiben nach Auswahl weiter
   editierbar.
2. **Speicherort**: global (JSON-Datei im FreeCAD-Benutzerverzeichnis, projektübergreifend).
3. **Verwaltung**: volle UI-Verwaltung (auswählen/anwenden, speichern, löschen).
4. **Mitgelieferte Presets**: Liste startet leer, Nutzer legt eigene Presets an.
5. **Geltungsbereich**: generische Lösung auf Ebene von `ParamWidget`, funktioniert für alle
   Tab-Typen gleichermaßen (einfacher als typ-spezifische Implementierung).

## Nächster Schritt
Freigabe durch Nutzer abwarten, dann Feature-Branch `feature/connection-presets` anlegen und
feingranular umsetzen.
