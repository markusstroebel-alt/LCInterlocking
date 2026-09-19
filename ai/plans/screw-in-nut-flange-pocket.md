# Plan: ScrewInNut Randfraesung

## Ziel
Der Verbindungstyp `ScrewInNut` erhaelt auf derselben Plattenseite wie die bestehende
Eindrehmutter-Tasche eine optionale, koaxiale Randfraesung. Sie nimmt den Bund/Rand von
Einschraubmuttern auf und besitzt einen separat einstellbaren Durchmesser sowie eine eigene Tiefe.

## Abgrenzung
- Die neue Randfraesung wird nur im `ScrewInNut`-Pfad erzeugt.
- Sie wird mit der bestehenden runden Eindrehmutter-Tasche vereinigt und startet an derselben
  Plattenoberflaeche.
- Sie veraendert weder `screw_length`, `screw_channel_length`, `washer_thickness`, `nut_depth`,
  `thread_clearance`, die Kopf-Tasche noch `head_clearance`.
- Ohne aktivierte Randfraesung bleibt die bisherige Geometrie unveraendert.

## Vorgehen
1. `lasercut/tabproperties.py`: drei rueckwaertskompatible Eigenschaften aufnehmen:
   `use_nut_flange_pocket` (Standard `False`), `nut_flange_diameter` und
   `nut_flange_depth`.
2. `lasercut/preferences.py` und `panel/preferencespage.py`: globale Standardwerte fuer die
   neuen Masse ergaenzen.
3. `panel/tab.py`: Checkbox und die abhaengigen Eingabefelder `Flange pocket diameter` und
   `Flange pocket depth` im `ScrewInNutWidget` anbieten.
4. `lasercut/presets.py`: die neuen Eigenschaften in globalen Presets speichern und editierbar
   machen.
5. `lasercut/join.py`: bei aktivierter Checkbox einen zweiten Zylinder auf der Mutterseite
   erzeugen. Er beginnt an der gleichen Aussenflaeche wie die Muttertasche, hat den neuen
   Durchmesser/die neue Tiefe und wird als zusaetzliche Entfernung registriert.
6. `docs/interlocking.md` sowie die ScrewInNut-Plan-README aktualisieren.
7. Python-Syntax und `git diff --check` ausfuehren; anschliessend die Geometrie manuell in
   FreeCAD pruefen.

## Betroffene Dateien
- `lasercut/tabproperties.py`
- `lasercut/preferences.py`
- `panel/preferencespage.py`
- `panel/tab.py`
- `lasercut/presets.py`
- `lasercut/join.py`
- `docs/interlocking.md`
- `ai/plans/screw-in-nut-flange-pocket.memory.md`
- `ai/plans/screw-in-nut-flange-pocket.README.md`

## Annahmen und offene Fragen
- Die Randfraesung liegt auf der bereits fuer die Eindrehmutter verwendeten Plattenseite.
- Durchmesser und Tiefe sind absolute Werte in Millimetern.
- Die Tiefe wird nicht automatisch aus `nut_depth` abgeleitet.
- Die bestehende Branch `feature/screw-in-nut` wird nach Freigabe weiterverwendet.