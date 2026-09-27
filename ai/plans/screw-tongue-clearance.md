# Plan: Schraubenfreiraum in TongueGroove

## Ziel
Eine TongueGroove-Feder darf keine Freiraeume einer Screw-Verbindung verdecken,
wenn beide Verbindungen auf derselben CAD-Flaeche zum selben Gegenpart erstellt
werden. Schraubenkanal, Schraubenbohrung und zugehoerige Slots bleiben fuer die
Montage offen.

## Ursache
Die TongueGroove-Feder wird dem Quellpart als `toAdd` hinzugefuegt. Screw erzeugt
einige Freiraeume dagegen im Gegenpart als `toRemove`. Die abschliessende
Boolesche Verarbeitung schneidet nur aus dem jeweiligen Materialelement. Ein
Freiraum im Gegenpart wird deshalb nicht automatisch auch aus der Feder des
Quellparts entfernt.

## Vorgehen
1. In `lasercut/join.py` einen Berechnungskontext fuer Schraubenfreiraeume
   einfuehren. Er ordnet die transformierten Screw-Freiraeume dem Quellobjekt,
   der Face und dem Gegenpart zu.
2. `make_tslot_tab_join()` registriert die Freiraeume, die im Gegenpart liegen:
   die beiden Slot-Ausschnitte und die Schraubenbohrung.
3. `make_tongue_groove_join()` liest passende Freiraeume aus diesem Kontext und
   fuegt sie als `toRemove` zum Quellpart der Feder hinzu. Dadurch wird nur die
   tatsaechliche Ueberlappung aus der Feder entfernt.
4. Die Zuordnung bleibt auf dieselbe Quell-Face und denselben Gegenpart
   beschraenkt. Andere TongueGroove- oder Screw-Verbindungen werden nicht
   beeinflusst.
5. Isolierte Tests pruefen die Zuordnung und dass nur die passende Feder den
   Freiraum erhaelt. Danach werden Syntax, Whitespace und Editor-Diagnosen
   geprueft.
6. Manueller FreeCAD-Test: TongueGroove und Screw auf einer Face erzeugen,
   Preview und MultiJoin pruefen sowie sicherstellen, dass der Schraubenslot
   unten offen bleibt.

## Betroffene Dateien
- `lasercut/join.py`
- `ai/plans/screw-tongue-clearance.memory.md`
- `ai/plans/screw-tongue-clearance.README.md`

## Annahmen
- Schraubenfreiraum hat Vorrang vor einer sich ueberlappenden Feder.
- Die Feder wird im Bereich der Schraubverbindung unterbrochen; das ist
  erforderlich, um Montagezugang und Freiraum zu erhalten.
- Die Regel gilt zunaechst fuer den Verbindungstyp `Screw`, nicht fuer andere
  Verbindungstypen.