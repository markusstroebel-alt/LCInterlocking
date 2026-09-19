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
Tasche hinter der Mutterntasche angefuegt.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`:
   - Neue Properties `nut_slot_overhang` und `thread_clearance` aufnehmen.
   - `screw_length_tol` aus der UI entfernen, aber beim Laden alter Dokumente weiterhin akzeptieren.
   - Alte `screw_length_tol`-Werte einmalig als `nut_slot_overhang` uebernehmen, damit bestehende
     Dokumente ihr bisheriges Verhalten behalten.
   - Neue Defaults: `nut_slot_overhang = 0.5 mm`, `thread_clearance = 3.0 mm`.
2. `panel/tab.py` (`TSlotWidget`):
   - `Screw length tol.` durch drei klar beschriftete Felder ersetzen:
     `Screw length`, `Nut height`, `Nut slot overhang`, `Thread clearance`.
   - `nut_height` ist bereits vorhanden und bleibt editierbar.
3. `lasercut/join.py` (`screw_way_on_face`):
   - Schraubenkanal aus realer Schraubenlaenge und Materialdicke berechnen.
   - Mutterntasche an der Mutterposition mit `nut_slot_overhang` hinter dem Schraubenkanal
     positionieren/erweitern.
   - `thread_clearance` als zusaetzlichen Freiraum hinter der Mutterntasche beruecksichtigen.
   - Die Werte muessen getrennt bleiben: Ueberstand/Geometrie-Freiraum duerfen nicht die reale
     `screw_length` veraendern.
4. Washer-Logik pruefen und an die neue Mutterntaschenposition anbinden, ohne die Bedeutung von
   `washer_diameter`/`washer_thickness` zu veraendern.
5. Preset- und README-/Memory-Daten aktualisieren, damit neue Felder gespeichert werden.
6. `docs/interlocking.md` um die vier Masse und ihre Bedeutung ergaenzen.

## Offene fachliche Klaerung
Die Begriffe "Ueberstand ueber Mutter" und "Gewinde-Freiraum" koennen geometrisch auf dieselbe
Richtung zeigen. Fuer eine eindeutige Implementierung wird angenommen:

- `nut_slot_overhang` bestimmt den Abstand/axialen Ueberstand der Mutterntasche relativ zum
  Schraubenkanal.
- `thread_clearance` verlaengert den Freiraum hinter der Mutterntasche zusaetzlich.
- Die vier Werte gelten pro Screw-Verbindung; `nut_flat_flat` und Washer-Werte bleiben bestehen.

## Naechster Schritt
Bestaetigt: `thread_clearance` wird zusaetzlich hinter der Mutterntasche erzeugt. Es veraendert
weder `screw_length` noch `nut_slot_overhang`. Die vorgeschlagenen Defaults sind
`nut_slot_overhang = 0.5 mm` und `thread_clearance = 3.0 mm`.

Vor der Umsetzung muss der konkretisierte Plan noch explizit freigegeben werden.
