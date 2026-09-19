# Memory: tab-length-pockets

## Status
- Plan freigegeben: [tab-length-pockets.md](./tab-length-pockets.md)
- Branch `feature/tab-length-pockets` angelegt.

## Entscheidungen
- `through_tabs` (Default `True`) ist der eindeutige Durchgangsmodus.
- `tab_length` ist bei verdeckten Taschen eine absolute Laenge in mm.
- Werte groesser als die Gegenmaterialdicke werden akzeptiert.
- Zapfen und Gegen-Tasche werden gemeinsam angepasst.
- Gilt fuer alle Tab-Widgets, einschliesslich Tab, Screw, WoodScrew und Continuous.

## Todo
- [x] Properties in `TabProperties`
- [x] Zapfen-/Taschengeometrie anpassen
- [x] UI fuer alle Tab-Widgets
- [x] Dokumentation aktualisieren
- [x] Syntax-Checks ausfuehren
- [ ] FreeCAD-Manuelltest (hier nicht verfuegbar)
- [x] README finalisieren
