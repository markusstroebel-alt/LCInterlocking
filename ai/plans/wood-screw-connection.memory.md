# Memory: wood-screw-connection

## Status
- Plan finalisiert: [wood-screw-connection.md](./wood-screw-connection.md)
- Branch `feature/wood-screw-connection` angelegt (basiert auf
  `feature/material-tolerance-defaults` -> `feature/connection-presets` -> `feature/nut-slot-shape`
  -> `develop`).

## Todo
- [ ] `lasercut/tabproperties.py`: `TYPE_WOOD_SCREW = 'WoodScrew'`
- [ ] `lasercut/join.py`: gemeinsame Zapfenlogik extrahieren, `make_wood_screw_tab_join` +
  Dispatch-Eintrag
- [ ] `panel/tab.py`: `WoodScrewWidget` + Verdrahtung in `createWidgetFromTabProperties`
- [ ] `panel/treepanel.py`: Dropdown-Liste erweitern
- [ ] `docs/interlocking.md`: neuen Typ dokumentieren
- [ ] Manuell in FreeCAD testen (FreeCAD hier nicht verfügbar)
- [ ] Feature-README finalisieren

## Entscheidungen/Notizen
- `TYPE_WOOD_SCREW = 'WoodScrew'` (kein Leerzeichen, passend zu 'Tab'/'Screw'/'Continuous').
- Rundes Loch (`screw_way_on_plane`) beim `part_interactor`, gleiche Position wie beim
  bestehenden "Screw"-Typ.
- `WoodScrewWidget` = `BaseTabWidget`-Felder + `half_tab_ratio` + `screw_diameter` (kein
  `screw_length`, keine Mutter-/Washer-Felder).
- Keine Ausfräsung (`screw_way_on_face`) für Schraube/Mutter/Washer bei diesem Typ.
