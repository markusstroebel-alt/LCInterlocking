# Feature: Frei einstellbare Mutter- und Unterlegscheiben-Tasche

## Zweck
Beim Schraub-Verbindungstyp (T-Slot/"Screw") sind die Maße der Mutter-Tasche jetzt frei editierbar,
und es kann zusätzlich eine Tasche für eine Unterlegscheibe eingefügt werden — z.B. für eine
Vierkantmutter statt der bisherigen Standardmaße, oder für eine Unterlegscheibe unter der Mutter.

## Nutzung
In den Eigenschaften einer Screw-Verbindung (Panel "Slots" bzw. Tab-Eigenschaften) gibt es neue
Felder:
- **Nut flat to flat** / **Nut height**: Schlüsselweite und Höhe der Mutter-Tasche, frei editierbar
  (Vorschlagswert aus den Schraubenmaßen bzw. den zuletzt verwendeten Werten).
- **Use washer**: fügt eine runde Durchgangstasche für eine Unterlegscheibe direkt zwischen
  Schrauben-Loch und Mutter-Tasche ein.
- **Washer diameter** / **Washer thickness**: nur sichtbar wenn "Use washer" aktiv ist, ebenfalls
  frei editierbar mit Vorschlagswert.

Alle Werte gelten pro einzelner Schraubverbindung (Tab/Face). Beim Anlegen einer neuen
Schraubverbindung werden die zuletzt verwendeten Werte als Vorschlag vorbelegt.

## Relevante Dateien
- `lasercut/tabproperties.py` — neue Properties `nut_flat_flat`, `nut_height`, `use_washer`,
  `washer_diameter`, `washer_thickness`
- `lasercut/helper.py` — `get_washer_spec` (Vorschlagswerte nach ISO 7089)
- `lasercut/join.py` — Geometrieerzeugung in `screw_way_on_face`
- `panel/tab.py` / `panel/toolwidget.py` — UI-Felder im `TSlotWidget`
- `docs/interlocking.md` — Dokumentation
