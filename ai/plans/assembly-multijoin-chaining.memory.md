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
- Manueller Test: Die Assembly-Links bleiben im Assembly, aber `fromParts` als
  `App::PropertyLinkList` erzeugt eine unzulaessige Referenz von `MultiJoin` auf die Links im
  Assembly. Die Auswertung von `Wall001.Pad.Face3` waehlt zudem bisher die erste Instanz `Wall`,
  da beide Links auf dasselbe externe Body zeigen.
- Nachbesserung: `fromParts` speichert nur noch die lokale Ursprungsgruppe; die Sichtbarkeit der
  Quellen wird aus der serialisierten Teileliste bestimmt. Bei mehreren Links auf ein Quellteil
  bevorzugt die Gesichtsauswahl die im aktuellen MultiJoin konfigurierte Instanz, etwa `Wall001`.
- Syntax, Whitespace, Editor-Diagnosen und die simulierte Mehrfachinstanz-Auswahl sind erfolgreich.
- Offener Punkt: In FreeCAD mit frisch erzeugten MultiJoins pruefen, dass die Scope-Warnung nicht
  mehr erscheint und `Base_tab` mit `Wall001` verbunden werden kann.