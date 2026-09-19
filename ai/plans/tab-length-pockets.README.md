# Feature: Einstellbare Zapfenlaenge und verdeckte Taschen

## Zweck
Zapfen koennen als Durchgangszapfen oder mit einer frei einstellbaren absoluten Laenge erzeugt
werden. Im zweiten Fall wird im Gegenmaterial automatisch eine passende Tasche gefraest.

## Nutzung
In den Eigenschaften aller Tab-Verbindungen stehen:
- **Through tabs**: aktiv erzeugt Zapfen durch die gesamte Gegenplatte (Default).
- **Tab length**: absolute Zapfenlaenge in Millimetern, wenn "Through tabs" deaktiviert ist;
	dann wird im Gegenmaterial automatisch eine Tasche mit derselben Tiefe erzeugt.

Die Option gilt fuer Tab, Screw, WoodScrew und Continuous.

## Relevante Dateien
- `lasercut/tabproperties.py` — neue Properties
- `lasercut/join.py` — Zapfenlaenge
- `lasercut/helper.py` — passende Gegen-Tasche
- `panel/tab.py` — UI
- `docs/interlocking.md` — Dokumentation
