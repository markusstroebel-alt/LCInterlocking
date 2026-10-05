# Fortschritt: Identische sichtbare Bauteile gruppieren

## Entscheidung

- Gleichheit wird nur fuer exportierbare Volumenkoerper ermittelt und ignoriert
  deren Placement im Modell.
- Unsichere Vergleiche bleiben getrennte Gruppen, damit keine verschiedenen
  Fertigungsteile zusammengefasst werden.
- Eine Gruppen-DXF verwendet die erste sichtbare Instanz als Namen und traegt
  `MENGE <Anzahl>` im `TEXT`-Layer.

## Stand

- Plan freigegeben.
- Feature-Branch `feature/visible-dxf-identical-grouping` erstellt.
- Export gruppiert sichtbare Koerper mit gleicher normalisierter Geometrie und
  uebergibt die Gruppengroesse an die DXF-Beschriftung. Kompakte Shape-
  Kenndaten filtern Kandidaten; `common()` bestaetigt anschliessend das
  gemeinsame Volumen ohne speicherintensive Tessellierung.
- Der echte FreeCAD-Test bestaetigt: drei gleich geformte, verschieden
  platzierte oder gedrehte Koerper ergeben eine DXF mit `MENGE 3`; ein
  abweichender Koerper bleibt getrennt.