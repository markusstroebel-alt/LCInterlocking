# Plan: Neuer Verbindungstyp "ScrewInNut" (Eindrehmutter)

## Ziel/Beschreibung
Neben dem bestehenden Verbindungstyp `Screw` soll ein eigener Verbindungstyp fuer eine
Eindrehmutter entstehen. Die Verbindung erzeugt weiterhin Zapfen und Schrauben-/Taschengeometrie
wie `Screw`, verwendet aber eigene Masse und eine eigene Schraubenlaengenberechnung:

- Die Eindrehmutter wird von der Innenseite in die Aussenplatte geschraubt und hat einen frei
   definierbaren **Aussendurchmesser**. Ein separates Mutter-Bohrloch ist nicht erforderlich;
   der Schraubendurchmesser bestimmt den inneren Durchgang.
- Die **Eindrehtiefe** wird separat definiert.
- Die **Schraubenlaenge** wird aus Washer, Schraubenkanal, Eindrehtiefe und Gewinde-Freiraum
   berechnet:
   `screw_length = washer_thickness + screw_channel_length + nut_depth + thread_clearance`.
- Die bestehende Screw-Variante bleibt unveraendert.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`: neuen Typ `TYPE_SCREW_IN_NUT = 'ScrewInNut'` ergaenzen.
2. `panel/treepanel.py`: `ScrewInNut` als separaten Auswahlpunkt neben `Screw` und `WoodScrew`
   anbieten.
3. `panel/tab.py`: eigenen `ScrewInNutWidget` anlegen. Vorgesehene Felder:
   - gemeinsame Tab-Felder,
   - `half_tab_ratio`,
   - `screw_diameter`,
   - `screw_channel_length` bzw. die dafuer erforderliche Platten-/Kanalgeometrie,
   - `nut_depth` (Eindrehtiefe),
   - `thread_clearance`,
   - `nut_outer_diameter` (Aussendurchmesser der Eindrehmutter),
   - optional `use_washer`, `washer_diameter`, `washer_thickness` wie beim Screw-Typ.
4. `lasercut/join.py`: eigene Geometriefunktionen fuer ScrewInNut:
   - gemeinsame Zapfen-/Lochlogik wiederverwenden,
   - `screw_way_on_plane` fuer das Gegenstueck wiederverwenden oder eine Variante mit der neuen
     Referenzlaenge schaffen,
    - auf der Mutterseite eine runde Tasche fuer die Eindrehmutter mit
       `nut_outer_diameter` und `nut_depth` erzeugen,
    - den inneren Durchgang aus `screw_diameter` ableiten,
    - die Schraubenkanal-/Gewindefreiraum-Geometrie ab Washer-Oberkante positionieren,
    - keine Nutzung der normalen `Screw`-Mutterntaschenformeln.
5. `lasercut/preferences.py` und `panel/preferencespage.py`: Defaults fuer die neuen
   ScrewInNut-Werte (`nut_outer_diameter`, `nut_depth`, `thread_clearance`) in den allgemeinen
   FreeCAD-Einstellungen bereitstellen.
6. Presets und Dokumentation um den neuen Typ und seine Masse erweitern.

## Offene Fragen (bitte beantworten)
## Entschiedene Punkte (vom Nutzer beantwortet)
1. **Typname**: `ScrewInNut` (Eindrehmutter).
2. **Muttergeometrie**: Nur der Aussendurchmesser wird angegeben; ein separates Mutter-Bohrloch
   ist nicht erforderlich.
3. **Schraubendurchgang**: Der innere Durchgang wird aus `screw_diameter` abgeleitet.
4. **Washer**: Die Washer-Tasche bleibt optional und wird wie beim normalen `Screw` verwendet.
5. **Eindrehtiefe und Schraubenlaenge**: Die Eindrehtiefe wird separat definiert. Die
   Schraubenlaenge ergibt sich aus `washer_thickness + screw_channel_length + nut_depth +
   thread_clearance`.
6. **Gewinde-Freiraum**: `thread_clearance` bleibt ein zusaetzlicher Freiraum hinter der
   Eindrehmutter.

## Naechster Schritt
Der konkretisierte Plan wird zur expliziten Freigabe vorgelegt. Erst danach wird ein eigener
Feature-Branch angelegt und implementiert.
