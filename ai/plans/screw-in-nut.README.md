# Feature: ScrewInNut (Eindrehmutter)

## Zweck
Neuer Verbindungstyp fuer eine Eindrehmutter, die von der Innenseite in die Aussenplatte geschraubt
wird. Die Schraubenlaenge wird eingegeben; die benoetigte Schraubenkanallaenge wird automatisch
berechnet.

## Berechnung
```text
	screw_channel_length = screw_length - washer_thickness - nut_depth

The thread clearance is separate blind-hole reserve and is not part of the screw length.
```

## Neue Eingaben
- Screw diameter
- Screw length
- Nut outer diameter
- Nut depth
- Thread clearance
- Optional Use washer mit Washer diameter/thickness

## Relevante Dateien
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `panel/tab.py`
- `panel/treepanel.py`
- `lasercut/preferences.py`
- `panel/preferencespage.py`
- `docs/interlocking.md`
