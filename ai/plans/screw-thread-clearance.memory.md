# Memory: screw-thread-clearance

## Status
- Plan freigegeben: [screw-thread-clearance.md](./screw-thread-clearance.md)
- Branch `feature/screw-thread-clearance` angelegt.

## Entscheidungen
- `screw_length`: reale Schraubenlaenge.
- `nut_height`: Mutterhoehe.
- `nut_slot_overhang`: Ueberstand der Mutterntasche, Default 0.5 mm.
- `thread_clearance`: zusaetzlicher Freiraum hinter der Mutterntasche, Default 3.0 mm.
- Defaults fuer Screw-Werte sollen zentral in den allgemeinen FreeCAD-Einstellungen liegen.
- Einzelne Verbindungen bleiben nach der Default-Uebernahme editierbar.

## Todo
- [ ] TabProperties und Legacy-Migration
- [ ] Screw-Geometrie fuer getrennte Werte
- [ ] Screw-UI-Felder
- [ ] FreeCAD-Preferences erweitern
- [ ] Presets/README/Dokumentation aktualisieren
- [ ] Syntax-Checks
- [ ] FreeCAD-Manuelltest
