# Memory: nut-slot-shape

## Status
- Plan erstellt: [nut-slot-shape.md](./nut-slot-shape.md)
- Nutzer war bei Rückfragen nicht erreichbar → offene Fragen im Plan autonom entschieden
  (Unterlegscheibe ersetzt Mutter komplett, Default-Maßtabelle, kein Anti-Rotation, Property pro Tab).
- Feature-Branch `feature/nut-slot-shape` angelegt.

## Todo
- [ ] `lasercut/tabproperties.py`: `nut_slot_type` Property ('square_nut' | 'washer') + Defaults
- [ ] `lasercut/helper.py`: Default-Washer-Maße Tabelle (analog `get_screw_nut_spec`)
- [ ] `lasercut/join.py`: `screw_way_on_face` verzweigen für runde Washer-Tasche
- [ ] `panel/tab.py`: `TSlotWidget` um Auswahlfeld für `nut_slot_type` erweitern
- [ ] `docs/interlocking.md`: neue Option dokumentieren
- [ ] Manuell in FreeCAD testen (test/simple_box.FCStd o.ä.)
- [ ] Feature-README finalisieren

## Entscheidungen/Notizen
- Property-Name: `nut_slot_type`, Werte als Strings `"square_nut"` (Default, Rückwärtskompatibilität)
  und `"washer"`.
- Washer-Tasche: Zylinder mit Radius `washer_diameter/2`, Tiefe = Face-Dicke, ohne Dog-Bone.
- Bestehende Box-Logik für `square_nut` bleibt unverändert (keine Regression für bestehende Projekte).
