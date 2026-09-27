# Plan: TongueGroove-Unterbrechungen fuer Schraubverbindungen

## Ziel
Bei einer gemeinsamen `TongueGroove`- und `Screw`- oder `ScrewInNut`-Verbindung
auf derselben Face soll die Feder und die Nut fuer jede einzelne
`Tab - Schraube - Tab`-Position unterbrochen werden. Die beiden Screw-Tabs,
ihre Slots und die Schraubenbohrung bleiben dabei unveraendert bestehen.

## Ursache
Der aktuelle Schraubenfreiraum wird erst als `toRemove` des fertigen Quellparts
registriert. Dadurch schneidet er nicht nur die TongueGroove-Feder, sondern auch
die separat erzeugten Screw-Tabs. Ausserdem wird die Groove-Entfernung im
Gegenpart nicht gezielt unterbrochen.

## Vorgehen
1. `JoinContext` von einzelnen Freiraeum-Volumen auf explizite
   Unterbrechungszonen erweitern. Eine Zone wird pro erzeugter
   `Tab - Schraube - Tab`-Position registriert und ist auf Quellobjekt, Face
   und Gegenpart begrenzt.
2. Die Zone deckt in Face-Richtung den gesamten Bereich von der Aussenkante des
   linken bis zur Aussenkante des rechten Screw-Tabs ab. Die vorhandenen
   Screw-Tabs bleiben eigene `toAdd`-Geometrien; Slots und Bohrung bleiben
   eigene `toRemove`-Geometrien.
3. `make_tongue_groove_join()` sammelt alle passenden Zonen, bevor es seine
   Geometrie hinzufuegt:
   - Die Feder wird mit diesen Zonen verschnitten, bevor sie als `toAdd`
     gespeichert wird.
   - Das Groove-Ausschnittvolumen wird mit denselben Zonen verschnitten, bevor
     es als `toRemove` im Gegenpart gespeichert wird.
4. `Screw` und `ScrewInNut` registrieren ihre Zonen jeweils fuer jede
   erzeugte Position. Mehrere Schraubverbindungen auf derselben Face erzeugen
   mehrere unabhaengige Unterbrechungen.
5. Die bisherige nachtraegliche Regel `Screw-Freiraum als toRemove der Feder`
   wird entfernt, damit Screw-Tabs nicht mehr ausgeschnitten werden.
6. Isolierte Tests pruefen die Zuordnung pro Face/Gegenpart, mehrere getrennte
   Zonen sowie die Registrierung fuer beide Schraubtypen. Anschliessend folgen
   Syntax-, Whitespace- und Editor-Pruefungen.
7. Manueller FreeCAD-Test: TongueGroove mit mehreren `Screw`- und
   `ScrewInNut`-Positionen auf derselben Face erzeugen. Kontrollieren, dass
   jede `Tab - Schraube - Tab`-Gruppe eine eigene Luecke in Feder und Nut hat,
   waehrend ihre Tabs, Slots und Bohrung erhalten bleiben.

## Betroffene Dateien
- `lasercut/join.py`
- `README.md`
- `docs/interlocking.md`
- `ai/plans/screw-tongue-interruption-zones.memory.md`
- `ai/plans/screw-tongue-interruption-zones.README.md`

## Annahmen
- Die Unterbrechungsbreite wird durch die beiden Screw-Tabs bestimmt, nicht
  durch eine pauschale globale Breite.
- Eine Verbindung mit mehreren Schraubpositionen erhaelt eine Unterbrechung
  pro Position.
- Die Regel gilt nur fuer identische Kombinationen aus Quellobjekt, Face und
  Gegenpart.