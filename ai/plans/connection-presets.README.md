# Feature: Verbindungs-Presets (Dropdown-Auswahl)

## Zweck
Bei allen Verbindungs-/Tab-Eigenschaften (Tab, Screw/T-Slot, Continuous, Flex) können jetzt
komplette Werte-Sätze als benanntes Preset gespeichert und über ein Dropdown wieder ausgewählt
werden, anstatt jedes Feld einzeln neu einzutragen.

## Nutzung
Oberhalb der bestehenden Eigenschaften-Felder gibt es eine neue Zeile:
- **Preset-Dropdown**: zeigt alle gespeicherten Presets für den aktuellen Verbindungstyp. Auswahl
  überträgt sofort alle passenden Werte in die Felder (weiterhin frei editierbar danach).
- **Save as...**: speichert die aktuellen Feldwerte unter einem neuen (oder bestehenden) Namen.
- **Delete**: löscht das aktuell ausgewählte Preset.

Presets werden global (projektübergreifend) in einer JSON-Datei im FreeCAD-Benutzerverzeichnis
gespeichert und gelten je nach Verbindungstyp (ein Screw-Preset erscheint nicht im Dropdown für
normale Tabs, etc.).

## Relevante Dateien
- `lasercut/presets.py` — Laden/Speichern/Verwalten der Presets
- `panel/toolwidget.py` — generische Preset-UI in `ParamWidget`
- `docs/interlocking.md` — Dokumentation
