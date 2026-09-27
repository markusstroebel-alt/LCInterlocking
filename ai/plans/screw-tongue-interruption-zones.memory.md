# Fortschritt: TongueGroove-Unterbrechungen fuer Schraubverbindungen

- Nutzerwunsch: Feder und Nut an jeder einzelnen `Tab - Schraube - Tab`-Gruppe
  unterbrechen, einschliesslich `ScrewInNut`.
- Ursache bestaetigt: Der aktuelle spaete `toRemove`-Schnitt entfernt auch
  Screw-Tabs und betrifft die Groove-Geometrie nicht gezielt.
- Vorgeschlagene Loesung: Unterbrechungszonen vor dem Hinzufuegen von Feder
  und Groove anwenden; Screw-Tabs und -Ausschnitte getrennt beibehalten.
- Nutzer hat den Plan freigegeben; Branch
  `feature/screw-tongue-interruption-zones` wurde angelegt.
- Erledigt: `JoinContext` registriert eine Unterbrechungszone pro erfolgreicher
  `Tab - Schraube - Tab`-Position. Die Zone ersetzt nur die gespeicherten
  Tongue- und Groove-Teilvolumina, nicht die gesamten Part-Geometrien.
- Erledigt: `ScrewInNut` verwendet denselben Registrierungspfad wie `Screw`.
- Geprueft: Zwei getrennte Zonen auf derselben Face werden nacheinander auf
  Tongue und Groove angewendet; abweichende Face und abweichender Gegenpart
  bleiben unveraendert. Der alte nachtraegliche Freiraum-API-Pfad ist entfernt.
- Geprueft: Der Dispatcher reicht den Kontext an `Screw` und `ScrewInNut`
  weiter. AST-Parse und `git diff --check` bestanden. Die einzigen
  Editor-Hinweise sind die bekannte fehlende `FreeCAD`-/`Part`-Umgebung.
- Commits: `c0cebc1` dokumentiert den Plan, `9432ee9` implementiert die
  positionsgenauen Unterbrechungszonen.
- Offen: Manueller FreeCAD-Test mit mehreren `Screw`- und `ScrewInNut`-
  Positionen auf derselben Face zum selben Gegenpart.