# Plan: Klare Schrauben- und Mutterntaschen-Masse

## Ziel/Beschreibung
Die aktuelle Property `screw_length_tol` ist missverstaendlich und wird in der Geometrie gleichzeitig
zur Laenge/Position des Schraubenkanals und zum Ueberstand der Mutterntasche verwendet. Fuer den
Screw-Verbindungstyp sollen vier getrennte Angaben sichtbar und eindeutig sein:

1. **Schraubenlaenge (`screw_length`)** — reale Laenge der verwendeten Schraube.
2. **Mutternhoehe (`nut_height`)** — axiale Laenge/Hoehe der Mutterntasche.
3. **Ueberstand ueber Mutter (`nut_slot_overhang`)** — wie weit die Mutterntasche hinter der Mutter
   ueber den Schraubenkanal hinausreicht.
4. **Gewinde-Freiraum (`thread_clearance`)** — zusaetzlicher axialer Platz hinter der Mutter fuer
   das ueberstehende Gewinde. Dieser Wert ist ein geometrischer Freiraum und keine Aenderung der
   realen Schraubenlaenge.

Die vorhandene Washer-Geometrie bleibt davon getrennt: Falls aktiv, wird sie weiterhin als eigene
Tasche hinter der Mutterntasche angefuegt. Alle diese Werte sollen als Defaults in den allgemeinen
FreeCAD-Einstellungen konfigurierbar sein; einzelne Verbindungen bleiben danach frei editierbar.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`:
   - Neue Properties `nut_slot_overhang` und `thread_clearance` aufnehmen.
   - `screw_length_tol` aus der UI entfernen, aber beim Laden alter Dokumente weiterhin akzeptieren.
   - Alte `screw_length_tol`-Werte einmalig als `nut_slot_overhang` uebernehmen, damit bestehende
     Dokumente ihr bisheriges Verhalten behalten.
   - Neue Defaults: `nut_slot_overhang = 0.5 mm`, `thread_clearance = 3.0 mm`.
    - Die Defaults fuer `screw_diameter`, `screw_length`, `nut_slot_overhang`, `thread_clearance`,
       `nut_flat_flat`, `nut_height`, `use_washer`, `washer_diameter` und `washer_thickness` aus
       den FreeCAD-Einstellungen uebernehmen, sofern ein Default dort gesetzt ist.
2. `lasercut/preferences.py`:
   - Eine FreeCAD-ParamGet-Gruppe fuer alle Screw-Defaults bereitstellen.
    - Die bisherigen tabellen-/codebasierten Werte nur als Fallback verwenden, wenn kein
       Einstellungswert existiert. `screw_length_tol` bleibt dabei nur als Legacy-Eingabe fuer
       alte Dokumente erhalten und wird nicht als neuer Einstellungswert gefuehrt.
3. `panel/tab.py` (`TSlotWidget`):
   - `Screw length tol.` durch drei klar beschriftete Felder ersetzen:
     `Screw length`, `Nut height`, `Nut slot overhang`, `Thread clearance`.
   - `nut_height` ist bereits vorhanden und bleibt editierbar.
4. `lasercut/join.py` (`screw_way_on_face`):
   - Schraubenkanal aus realer Schraubenlaenge und Materialdicke berechnen.
   - Mutterntasche an der Mutterposition mit `nut_slot_overhang` hinter dem Schraubenkanal
     positionieren/erweitern.
   - `thread_clearance` als zusaetzlichen Freiraum hinter der Mutterntasche beruecksichtigen.
   - Die Werte muessen getrennt bleiben: Ueberstand/Geometrie-Freiraum duerfen nicht die reale
     `screw_length` veraendern.
5. Washer-Logik pruefen und an die neue Mutterntaschenposition anbinden, ohne die Bedeutung von
   `washer_diameter`/`washer_thickness` zu veraendern.
6. Native FreeCAD-Preferences-Seite erweitern, damit alle Screw-Defaults dort bearbeitet werden
   koennen. Die Werte werden beim Erzeugen neuer Screw-Verbindungen vorgeschlagen; bestehende
   Verbindungen werden nicht automatisch veraendert.
7. Preset- und README-/Memory-Daten aktualisieren, damit neue Felder gespeichert werden.
8. `docs/interlocking.md` um die vier Masse und ihre Bedeutung sowie den zentralen Einstellungsort
   ergaenzen.

## Offene fachliche Klaerung
Die Begriffe "Ueberstand ueber Mutter" und "Gewinde-Freiraum" koennen geometrisch auf dieselbe
Richtung zeigen. Fuer eine eindeutige Implementierung wird angenommen:

- `nut_slot_overhang` bestimmt den Abstand/axialen Ueberstand der Mutterntasche relativ zum
  Schraubenkanal.
- `thread_clearance` verlaengert den Freiraum hinter der Mutterntasche zusaetzlich.
- Die vier Werte gelten pro Screw-Verbindung; `nut_flat_flat` und Washer-Werte bleiben bestehen.

## Naechster Schritt
Bestaetigt: `thread_clearance` wird zusaetzlich hinter der Mutterntasche erzeugt. Es veraendert
weder `screw_length` noch `nut_slot_overhang`. Alle Screw-Defaults werden zentral in den FreeCAD-
Einstellungen festgelegt; die Werte pro Verbindung bleiben ueberschreibbar. Die vorgeschlagenen
Defaults sind `nut_slot_overhang = 0.5 mm` und `thread_clearance = 3.0 mm`.

Vor der Umsetzung muss der konkretisierte Plan noch explizit freigegeben werden.
