# Plan: Neuer Verbindungstyp "Holzschraube" (Wood Screw)

## Ziel/Beschreibung
Der bestehende Verbindungstyp "Screw" (`TabProperties.TYPE_T_SLOT`) erzeugt Zapfen (Tabs) *und*
eine Ausfräsung/Slot für Schraubenschaft + Mutter + Unterlegscheibe (`screw_way_on_face` in
`lasercut/join.py`) sowie ein rundes Loch für den Schraubenschaft im Gegenstück
(`screw_way_on_plane`). Für Holzschrauben (die direkt ins Holz greifen, ohne Mutter) wird nur
Folgendes benötigt:
- die Zapfen (wie bei "Screw"/"Tab"),
- das runde Loch für den Schraubenschaft im Gegenstück (`screw_way_on_plane`).

Die Ausfräsung für Schraubenschaft + Mutter + Unterlegscheibe (`screw_way_on_face`) entfällt
komplett. Dafür soll ein neuer, eigenständiger Auswahlpunkt entstehen (wie "Tab", "Screw",
"Continuous"), z.B. **"Wood screw"**.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`: neue Konstante `TYPE_WOOD_SCREW = 'Wood screw'`.
2. `lasercut/join.py`:
   - Gemeinsame Zapfen-/Lochlogik aus `make_tslot_tab_join` in eine Hilfsfunktion auslagern (Tabs
     erzeugen, `check_intersect`, `tab_join_create_hole_on_plane`), um Duplikation zu vermeiden.
   - Neue Funktion `make_wood_screw_tab_join(tab, tab_part, other_parts)`: nutzt die gemeinsame
     Zapfenlogik, fügt danach nur `screw_way_on_plane` (rundes Loch) beim `part_interactor` hinzu —
     **kein** `screw_way_on_face`.
   - Dispatch-Stelle (Ende der Datei) um
     `elif tab.tab_type == TabProperties.TYPE_WOOD_SCREW: make_wood_screw_tab_join(...)` erweitern.
3. `panel/tab.py`: neue Widget-Klasse `WoodScrewWidget(BaseTabWidget)` mit den Feldern
   `half_tab_ratio` und `screw_diameter` (kein `screw_length`, `nut_flat_flat`, `nut_height`,
   `use_washer`, `washer_diameter`, `washer_thickness` — die werden nicht gebraucht). Verdrahtung in
   `TabsList.createWidgetFromTabProperties`.
4. `panel/treepanel.py`: `TabProperties.TYPE_WOOD_SCREW` zur Dropdown-Liste der Verbindungstypen
   hinzufügen.
5. `docs/interlocking.md`: neuen Verbindungstyp dokumentieren.

## Betroffene Dateien/Module
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `panel/tab.py`
- `panel/treepanel.py`
- `docs/interlocking.md`

## Offene Fragen (bitte kurz bestätigen)
1. **Name in der Dropdown-Liste**: Passt "Wood screw" als Anzeigename, oder bevorzugst du eine
   andere Bezeichnung (z.B. "Holzschraube", "WoodScrew" ohne Leerzeichen)?
2. **Position des Lochs**: Das runde Loch (`screw_way_on_plane`) kommt wie bisher beim
   `part_interactor` (Gegenstück) an derselben Position wie beim bestehenden "Screw"-Typ — richtig
   so?
3. **half_tab_ratio/screw_diameter**: Reichen diese zwei Felder, oder werden weitere bestehende
   Screw-Felder (z.B. `screw_length_tol`, `dog_bone`) ebenfalls benötigt?

## Nächster Schritt
Nach Bestätigung Feature-Branch `feature/wood-screw-connection` anlegen und feingranular umsetzen.
