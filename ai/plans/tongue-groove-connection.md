# Plan: Durchgehende Feder-und-Nut-Verbindung

## Ziel
Ein neuer Verbindungstyp `TongueGroove` soll die gesamte Breite einer ausgewaehlten
Face als durchgehende Feder verlaengern und im Gegenpart eine passende Nut erzeugen.
Er eignet sich insbesondere fuer Schubladenboeden: Eine Bodenplatte greift zum Beispiel
`10 mm` tief in eine Nut der Seitenwand ein, waehrend die Feder nur die halbe
Materialdicke hoch ist.

Die ausgewaehlte Master-Face gehoert immer zum Teil mit der Feder. Die Nut wird im
tatsaechlich geschnittenen Gegenpart erzeugt. Damit ist eindeutig, welches Teil
verlaengert wird.

## Bedienmodell
- **Groove depth**: Laenge der Feder ab der ausgewaehlten Face und Nuttiefe im
  Gegenpart, zum Beispiel `10 mm`.
- **Height mode**: `Full material thickness` oder `Custom height`.
  - Bei voller Hoehe entspricht die Feder der Materialdicke des ausgewählten Teils.
  - Bei eigener Hoehe wird **Tongue height** in Millimetern eingegeben, etwa die halbe
    Materialdicke.
- **Height alignment**: `Center`, `Side A` oder `Side B`.
  - Die Ausrichtung legt fest, wo die eigene Federhoehe ueber die Materialdicke der
    ausgewählten Face liegt.
  - `Side A` und `Side B` entsprechen deterministisch der positiven bzw. negativen
    lokalen Dickenachse der Face. Im Preview muss die Feder hervorgehoben erscheinen,
    damit die gewaehlte Seite ohne Koordinatenwissen sichtbar ist.
  - Ein Tooltip benennt `Side A` als die Seite in positiver lokaler Dickenrichtung und
    `Side B` als die Gegenrichtung.
- **Groove bottom clearance**: zusaetzliche Tiefe hinter der Feder, standardmaessig
  ueber die vorhandene `Tab length tolerance` vorbelegt. Dadurch laesst sich die Nut
  bei Bedarf etwas tiefer als die Feder schneiden.
- **Groove width clearance**: nutzt die vorhandene Slot-width-Tolerance, damit die
  Nut in der Hoehe passend zur Feder etwas Spiel erhalten kann.

Die Verbindung beansprucht die volle Breite der Face. Parameter fuer einzelne Tabs
(`Number of tabs`, `Width of tabs`, `Shift`, `Interval ratio`) werden fuer diesen Typ
nicht angezeigt und nicht verwendet.

## Geometrie
1. Die lokale Face-Achse der bestehenden Tab-Geometrie wird weiterverwendet:
   - die Feder verlaeuft entlang der Normalenrichtung der Master-Face,
   - ihre Breite entspricht der Face-Breite,
   - ihre Hoehe liegt ueber die lokale Materialdickenachse entsprechend `Height mode`
     und `Height alignment`.
2. Es wird ein einzelner Quader als Feder erzeugt, nicht eine Serie einzelner Tabs.
3. Der erste geometrisch schneidende Gegenpart erhaelt eine dazu passende Nut:
   - gleiche Breite,
   - Hoehe plus Slot-width-Tolerance,
   - Tiefe `Groove depth + Groove bottom clearance`.
4. Die bestehende Schnittpruefung entscheidet wie bei Tabs, welcher konfigurierte
   Gegenpart die Nut erhaelt. Der Preview und die finale Berechnung verwenden exakt
   denselben Geometriepfad.
5. Nicht ueberlappende oder ungueltige Werte werden mit klaren Fehlern abgefangen:
   positive Tiefe, positive Federhoehe, Federhoehe nicht groesser als Materialdicke.

## Umsetzungsschritte
1. `lasercut/tabproperties.py`: `TYPE_TONGUE_GROOVE` und persistierbare Eigenschaften
   fuer Tiefe, Hoehenmodus, eigene Hoehe und Seitenlage hinzufuegen. Bestehende Dokumente
   muessen beim Laden kompatibel bleiben.
2. `panel/tab.py`: eigenes `TongueGrooveWidget` mit den genannten, relevanten Feldern
   erstellen und im Typwechsler registrieren. Bei Typwechsel sollen gemeinsame Werte
   nicht verloren gehen.
3. `lasercut/join.py`: eine isolierte Geometriefunktion fuer Feder und Nut erstellen;
   sie verwendet die bestehende Face-Transformation und Intersectionslogik, aber nicht
   die Mehrfach-Tab-Positionierung.
4. `lasercut/preferences.py` und `panel/preferencespage.py`: Defaults fuer
   Nuttiefe, Hoehenmodus, eigene Federhoehe, Seitenlage und Bodenfreiraum anbieten,
   soweit sie nicht unmittelbar aus Materialdicke oder vorhandenen Toleranzen folgen.
5. `lasercut/presets.py`: neue TongueGroove-Parameter in Verbindungspresets speichern
   und laden.
6. `panel/treepanel.py`: Preview-Verhalten pruefen und bei Bedarf eine knappe
   Statusmeldung ausgeben, die Master-Face, Gegenpart und Seitenlage nennt.
7. Geometrie mit isolierten Fake-Objekten pruefen sowie in FreeCAD manuell testen:
   - volle Materialhoehe,
   - halbe Materialhoehe zentriert,
   - halbe Materialhoehe an Side A und Side B,
   - `10 mm` Nut mit Bodenfreiraum,
   - Assembly-Link als Master und Gegenpart,
   - Typwechsel von Tab nach TongueGroove.
8. README und Interlocking-Dokumentation ergaenzen.

## Betroffene Dateien
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `lasercut/preferences.py`
- `lasercut/presets.py`
- `panel/tab.py`
- `panel/preferencespage.py`
- `panel/treepanel.py` (nur Diagnose/Preview falls erforderlich)
- `README.md`
- `docs/interlocking.md`
- `ai/plans/tongue-groove-connection.memory.md`
- `ai/plans/tongue-groove-connection.README.md`

## Annahmen und offene Fragen
- Die Feder soll sich immer von der ausgewählten Master-Face weg in deren lokale
  Normalenrichtung erstrecken. Dies entspricht dem bestehenden Tab-Prinzip.
- `Side A` und `Side B` sind im UI absichtlich nicht mit Weltkoordinaten wie oben oder
  unten benannt, weil diese je nach Bauteilorientierung nicht stabil waeren. Das Preview
  dient zur unmittelbaren Kontrolle der Lage.
- Die volle Face-Breite ist fuer den Schubladenboden passend. Unterbrochene oder
  mehrfach getrennte Nuten sind nicht Teil dieses ersten Schritts.
- Es wird zunaechst keine automatische Aktualisierung nachgelagerter MultiJoins
  eingefuehrt; deren manuelle Neuberechnung bleibt unveraendert.