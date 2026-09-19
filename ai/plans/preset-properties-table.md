# Plan: Globale Presets tabellarisch anzeigen und bearbeiten

## Ziel/Beschreibung
Die global gespeicherten Presets liegen aktuell in `LCInterlocking_presets.json` und sind nur ueber
das Preset-Dropdown sowie "Save as..."/"Delete" im jeweiligen Tab-Widget verwaltbar. In der
allgemeinen FreeCAD-Preferences-Seite soll zusaetzlich eine Tabelle erscheinen, in der alle
Presets sichtbar und direkt editierbar sind.

Die bestehende JSON-Struktur bleibt erhalten:
`{tab_type: [{name: ..., values: {...}}, ...]}`.

## Geplantes Vorgehen
1. `lasercut/presets.py` um eine robuste Verwaltungsfunktion erweitern:
   - alle Presets flach fuer die Tabelle liefern (`tab_type`, `name`, Property-Werte),
   - geaenderte Tabellenzeilen wieder in die bestehende gruppierte JSON-Struktur schreiben,
   - Namen und Verbindungstypen validieren, doppelte Namen innerhalb eines Typs verhindern.
2. `panel/preferencespage.py` um einen Bereich **Global connection presets** erweitern:
   - `QTableWidget` mit einer Zeile pro Preset,
   - Spalten fuer Verbindungstyp, Preset-Name und die bekannten Properties
     (Screw-/Tab-/Washer-/Taschen-Werte),
   - leere Zellen fuer Properties, die zu einem anderen Tab-Typ nicht gehoeren,
   - editierbare Zellen fuer Namen und Werte,
   - Buttons fuer "Add preset", "Delete selected" und "Save presets".
3. Beim Laden der Preferences werden die JSON-Presets in die Tabelle uebernommen.
4. Beim Speichern der Preferences werden die Tabellenwerte validiert und global in die JSON-Datei
   geschrieben. Fehlende optionale Werte bleiben im jeweiligen Preset unveraendert/leer.
5. Das bestehende Dropdown in `ParamWidget` bleibt kompatibel und liest nach dem Speichern die
   aktualisierten globalen Werte.
6. `docs/interlocking.md` und die Feature-README um die Tabellenverwaltung erweitern.

## Betroffene Dateien/Module
- `lasercut/presets.py`
- `panel/preferencespage.py`
- `docs/interlocking.md`
- `ai/plans/connection-presets.README.md`
- `ai/plans/connection-presets.memory.md`

## Annahmen
- Die Tabelle verwaltet alle gespeicherten Presets aller Tab-Typen, nicht nur Screw-Presets.
- Verbindungstyp und Preset-Name sind editierbar; numerische Werte werden als Dezimalwerte
  gespeichert, boolesche Werte als `true`/`false`.
- Die Tabelle ist Teil der bestehenden nativen FreeCAD-Preferences-Seite.

## Nächster Schritt
Vor der Umsetzung Feature-Branch `feature/preset-properties-table` anlegen und die Umsetzung
feingranular committen.
