# Memory: nut-slot-shape

## Status
- Plan mehrfach überarbeitet (erste Annahme "Teiltiefen-Fräsen" war falsch, korrigiert auf reinen
  Durchgangsschnitt). Finaler Plan mit Nutzer-Antworten abgestimmt und freigegeben.
- Implementierung abgeschlossen auf Branch `feature/nut-slot-shape`, feingranular committed:
  1. Workflow-Instructions (.github/copilot-instructions.md) — auf develop.
  2. Plan/Memory/README-Grundgerüst.
  3. Plan finalisiert mit Nutzer-Entscheidungen.
  4. `helper.get_washer_spec` (ISO 7089 Vorschlagswerte).
  5. `TabProperties`: `nut_flat_flat`, `nut_height`, `use_washer`, `washer_diameter`,
     `washer_thickness` + "letzte Werte"-Cache (`_last_nut_washer_values`).
  6. `join.screw_way_on_face`: nutzt jetzt `tab.nut_flat_flat`/`tab.nut_height`, optionale
     Washer-Tasche (Zylinder) direkt zwischen Schrauben- und Mutter-Tasche.
  7. `panel/tab.py` `TSlotWidget`: neue UI-Felder; `panel/toolwidget.py`: Checkbox löst jetzt auch
     `listchangeIndex` aus (nötig, damit Washer-Felder beim Toggle sofort ein-/ausgeblendet werden).
  8. `docs/interlocking.md` aktualisiert.

## Todo
- [x] `lasercut/tabproperties.py`
- [x] `lasercut/helper.py`
- [x] `lasercut/join.py`
- [x] `panel/tab.py` + `panel/toolwidget.py`
- [x] `docs/interlocking.md`
- [ ] Manuell in FreeCAD testen (test/simple_box.FCStd o.ä.) — **noch nicht gemacht, FreeCAD in
  dieser Umgebung nicht verfügbar**. Bitte vor Merge in FreeCAD selbst verifizieren.
- [x] Feature-README finalisiert

## Entscheidungen/Notizen
- Kein `nut_type`-Enum (Hex/Square) nötig: `nut_flat_flat`/`nut_height` sind einfach frei
  editierbare Felder, die bisherige Box-Geometrie ist für jede Mutterform generisch genug.
- Washer-Tasche wird genau wie die Mutter-Tasche gehandhabt (eigene Box mit `washer_diameter` als
  Breite/Schlüsselweite und `washer_thickness` als Länge/Dicke), direkt anschließend hinter
  (unterhalb) der Mutter-Tasche positioniert — zwei Korrekturrunden nach Nutzer-Feedback:
  1. Erst eigenes Segment VOR der Mutter (zwischen Schrauben- und Mutter-Tasche) — verworfen.
  2. Dann Kreisausschnitt deckungsgleich MIT der Mutter-Tasche — verworfen.
  3. Jetzt: Box-Tasche wie die Mutter, aber HINTER/unterhalb der Mutter-Tasche — aktueller Stand.
- Rückwärtskompatibilität: bestehende Projekte ohne die neuen Properties bekommen beim Laden
  automatisch die aus `get_screw_nut_spec`/`get_washer_spec` abgeleiteten Default-Werte
  (`hasattr`-Check wie bei allen anderen Properties in `TabProperties`).
