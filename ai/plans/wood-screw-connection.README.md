# Feature: Verbindungstyp "WoodScrew"

## Zweck
Neuer Verbindungstyp für Holzschrauben, die direkt ins Material greifen (ohne Mutter). Erzeugt nur
Zapfen (wie "Tab") plus ein rundes Loch für den Schraubenschaft im Gegenstück — ohne die
Ausfräsung für Schraube, Mutter und Unterlegscheibe des "Screw"-Typs.

## Nutzung
Bei der Auswahl des Verbindungstyps ("Tab"/"Screw"/"Continuous") steht jetzt zusätzlich
**"WoodScrew"** zur Verfügung. Parameter: "Half tab ratio" und "Screw diameter" (steuern Position
und Größe des runden Lochs), sonst wie bei "Tab".

## Relevante Dateien
- `lasercut/tabproperties.py` — `TYPE_WOOD_SCREW`
- `lasercut/join.py` — `make_wood_screw_tab_join`
- `panel/tab.py` — `WoodScrewWidget`
- `panel/treepanel.py` — Dropdown-Liste
- `docs/interlocking.md` — Dokumentation
