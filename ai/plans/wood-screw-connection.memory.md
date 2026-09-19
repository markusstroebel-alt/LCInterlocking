# Memory: wood-screw-connection

## Status
- Plan finalisiert: [wood-screw-connection.md](./wood-screw-connection.md)
- Branch `feature/wood-screw-connection` angelegt (basiert auf
  `feature/material-tolerance-defaults` -> `feature/connection-presets` -> `feature/nut-slot-shape`
  -> `develop`).

## Todo
- [x] `lasercut/tabproperties.py`: `TYPE_WOOD_SCREW = 'WoodScrew'`
- [x] `lasercut/join.py`: gemeinsame Zapfenlogik extrahiert, `make_wood_screw_tab_join` +
  Dispatch-Eintrag
- [x] `panel/tab.py`: `WoodScrewWidget` + Verdrahtung in `createWidgetFromTabProperties`
- [x] `panel/treepanel.py`: Dropdown-Liste erweitert
- [x] `docs/interlocking.md`: neuen Typ dokumentiert
- [ ] Manuell in FreeCAD testen (FreeCAD hier nicht verfügbar)
- [x] Feature-README finalisiert

## Entscheidungen/Notizen
- `TYPE_WOOD_SCREW = 'WoodScrew'` (kein Leerzeichen, passend zu 'Tab'/'Screw'/'Continuous').
- Rundes Loch (`screw_way_on_plane`) beim `part_interactor`, gleiche Position wie beim
  bestehenden "Screw"-Typ.
- `WoodScrewWidget` = `BaseTabWidget`-Felder + `half_tab_ratio` + `screw_diameter` (kein
  `screw_length`, keine Mutter-/Washer-Felder).
- Keine Ausfräsung (`screw_way_on_face`) für Schraube/Mutter/Washer bei diesem Typ.
