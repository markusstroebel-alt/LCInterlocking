# Plan: Neuer Verbindungstyp "ImpactNut" (Einschlagmutter)

## Ziel/Beschreibung
Neben dem bestehenden Verbindungstyp `Screw` soll ein eigener Verbindungstyp fuer eine
Einschlagmutter entstehen. Die Verbindung erzeugt weiterhin Zapfen und Schrauben-/Taschengeometrie
wie `Screw`, verwendet aber eigene Masse und eine eigene Schraubenlaengenberechnung:

- Die Einschlagmutter sitzt in der Platte und hat einen eigenen, frei definierbaren
  **Aussendurchmesser**.
- Das **Bohrloch fuer die Einschlagmutter** soll separat definiert werden koennen.
- Die **Schraubenlaenge** wird nicht wie beim bisherigen `Screw` aus der gesamten Material-/Taschen-
  geometrie abgeleitet, sondern bezieht sich ab der **Oberkante des Washers bis zum bisherigen
  Schraubenkopf**.
- Die bestehende Screw-Variante bleibt unveraendert.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`: neuen Typ `TYPE_IMPACT_NUT = 'ImpactNut'` ergaenzen.
2. `panel/treepanel.py`: `ImpactNut` als separaten Auswahlpunkt neben `Screw` und `WoodScrew`
   anbieten.
3. `panel/tab.py`: eigenen `ImpactNutWidget` anlegen. Vorgesehene Felder:
   - gemeinsame Tab-Felder,
   - `half_tab_ratio`,
   - `screw_diameter`,
   - `screw_length` (Referenz: Oberkante Washer bis Schraubenkopf),
   - `nut_slot_overhang`,
   - `thread_clearance`,
   - `nut_outer_diameter` (Aussendurchmesser der Einschlagmutter),
   - `nut_hole_diameter` (separates Bohrloch fuer die Einschlagmutter),
   - optional `use_washer`, `washer_diameter`, `washer_thickness` wie beim Screw-Typ.
4. `lasercut/join.py`: eigene Geometriefunktionen fuer ImpactNut:
   - gemeinsame Zapfen-/Lochlogik wiederverwenden,
   - `screw_way_on_plane` fuer das Gegenstueck wiederverwenden oder eine Variante mit der neuen
     Referenzlaenge schaffen,
   - auf der Mutterseite eine runde Einschlagmutter-Tasche bzw. ein Bohrloch mit
     `nut_outer_diameter`/`nut_hole_diameter` erzeugen,
   - die Schrauben-/Gewindefreiraum-Geometrie ab Washer-Oberkante positionieren,
   - keine Nutzung der normalen `Screw`-Mutterntaschenformeln.
5. `lasercut/preferences.py` und `panel/preferencespage.py`: Defaults fuer die neuen
   ImpactNut-Werte in den allgemeinen FreeCAD-Einstellungen bereitstellen.
6. Presets und Dokumentation um den neuen Typ und seine Masse erweitern.

## Offene Fragen (bitte beantworten)
1. **Name**: Passt `ImpactNut` als interner/angezeigter Typname, oder soll der Eintrag
   `Einschlagmutter` heissen?
2. **Geometrie der Einschlagmutter**: Soll auf der Mutterseite ein runder Durchgang fuer den
   kompletten Aussendurchmesser erzeugt werden, oder eine Tasche mit `nut_outer_diameter`, in der
   nur das eigentliche Schraubenloch (`nut_hole_diameter`) durchgeht?
3. **Bedeutung der zwei Durchmesser**: Ist `nut_outer_diameter` der Aussendurchmesser des
   Metallkoerpers und `nut_hole_diameter` der Durchmesser der Bohrung fuer die Schraube?
4. **Washer**: Bleibt die Washer-Tasche optional und wird wie beim normalen `Screw` unter dem
   Schraubenkopf positioniert?
5. **Laengenreferenz**: Ist `screw_length` die Strecke von der Oberkante des Washers bis zur
   Unterseite des Schraubenkopfes (also ohne Washer-Dicke und ohne Einschlagmutter-Tiefe), oder
   bis zur Schraubenspitze?
6. **Einschlagmutter-Tiefe**: Brauchen wir dafuer ebenfalls ein separates Mass (z.B.
   `nut_height`/`nut_depth`), oder reicht der Aussendurchmesser plus Bohrlochdurchmesser?

## Naechster Schritt
Nach Beantwortung der offenen Fragen wird der Plan konkretisiert und zur expliziten Freigabe
vorgelegt. Erst danach wird ein eigener Feature-Branch angelegt und implementiert.
