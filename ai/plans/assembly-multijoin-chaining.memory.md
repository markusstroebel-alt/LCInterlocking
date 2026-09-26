# Fortschritt: Assembly-MultiJoin-Verkettung

- Plan freigegeben und Umsetzung begonnen.
- Ursache bestaetigt: `MultiJoin_origin_parts.addObject(Base)` verschiebt den Assembly-Link `Base`
  aus dem Assembly-Container.
- Das erzeugte `Base_tab` ist ein freistehendes `Part::Feature`; das Folge-Szenario ist eine
  Verbindung mit der Assembly-Komponente `Wall001`.
- `MultipleJoinGroup.execute()` behaelt Objekte mit `LinkedObject` im bisherigen Container und
  verschiebt nur Nicht-Link-Objekte in `MultiJoin_origin_parts`.
- Debugmeldungen mit dem Praefix `[LCInterlocking]` dokumentieren Pfadauflösung, die Zuordnung
  eines externen Features zu seinem Assembly-Link sowie die Behandlung von Quellen und Ergebnissen.
- Simulierte Auswahl eines externen `Pad` wird korrekt zu `Wall` aufgeloest. Python-Syntax,
  Editor-Diagnosen und `git diff --check` sind erfolgreich.
- Offener Punkt: In FreeCAD pruefen, dass `Base` nach dem ersten MultiJoin im Assembly bleibt und
  `Base_tab` mit `Wall001` in einem zweiten MultiJoin verbunden werden kann.