# Memory: connection-presets

## Status
- Plan finalisiert: [connection-presets.md](./connection-presets.md)
- Branch `feature/connection-presets` angelegt (basiert auf `feature/nut-slot-shape`, welches
  wiederum auf `develop` basiert).

## Todo
- [x] `lasercut/presets.py` (neu): Laden/Speichern/Verwalten der Presets als globale JSON-Datei
- [x] `panel/toolwidget.py` (`ParamWidget`): generische Preset-UI (Dropdown, Save as, Delete)
- [x] `docs/interlocking.md`: Kurzbeschreibung ergänzt (inkl. Korrektur veralteter Washer-Doku)
- [ ] Manuell in FreeCAD testen (FreeCAD hier nicht verfügbar für automatisierte Tests)
- [x] Feature-README finalisiert

## Entscheidungen/Notizen
- Datenformat: `{"<tab_type>": [{"name": "...", "values": {"<property>": <value>, ...}}, ...]}`
- Presets nach `tab_type` gruppiert/gefiltert (z.B. `TabProperties.TYPE_T_SLOT`), damit nur
  passende Presets pro Widget-Typ angezeigt werden.
- Preset-Anwendung überschreibt nur Widgets, deren Name in `values` vorkommt UND im aktuellen
  `widget_list` existiert (andere Typen mit anderen Feldern werden automatisch ignoriert).
- Speicherort: `FreeCAD.getUserAppDataDir() + "LCInterlocking_presets.json"`.
