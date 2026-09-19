# Memory: tab-length-pockets

## Status
- Plan freigegeben: [tab-length-pockets.md](./tab-length-pockets.md)
- Branch `feature/tab-length-pockets` angelegt.

## Entscheidungen
- `through_tabs` (Default `True`) ist der eindeutige Durchgangsmodus.
- `tab_length` ist bei verdeckten Taschen eine absolute Laenge in mm.
- `tab_length_tolerance` ist die zusaetzliche Taschentiefe und hat den Default `0.5 mm`.
- Werte groesser als die Gegenmaterialdicke werden akzeptiert.
- Zapfen und Gegen-Tasche werden gemeinsam angepasst.
- Gilt fuer alle Tab-Widgets, einschliesslich Tab, Screw, WoodScrew und Continuous.

## Todo
- [x] Properties in `TabProperties`
- [x] Zapfen-/Taschengeometrie anpassen
- [x] UI fuer alle Tab-Widgets
- [x] Laengentoleranz in Geometrie und UI
- [x] Dokumentation aktualisieren
- [x] Syntax-Checks ausfuehren
- [ ] FreeCAD-Manuelltest (hier nicht verfuegbar)
- [x] README finalisieren
