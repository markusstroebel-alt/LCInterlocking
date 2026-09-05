# Plan: Fräs-/lasertaugliche Mutter-Tasche (Unterlegscheibe unter Mutter / Vierkantmutter)

## Ziel/Beschreibung
Teile werden per Laser oder 3-Achsen-CNC gefertigt — beides als **Durchgangsschnitt** (keine
Teiltiefen-Taschen, gemäß Nutzer-Vorgabe). Die aktuelle Mutter-Tasche in `screw_way_on_face`
(lasercut/join.py) ist eine einzelne rechteckige Durchgangs-Tasche (Breite = `nut_flat_flat`,
Länge = `nut_height`), direkt neben der Tasche für den Schraubenschaft (`screw_hole`), beide entlang
der Schraubenachse (X) aneinandergereiht und komplett durchs Material geschnitten.

Ziel ist, die 2D-Geometrie so zu erweitern, dass wahlweise:
1. zusätzlich eine runde Durchgangs-Tasche für eine Unterlegscheibe (definierbarer Durchmesser)
   zwischen Schrauben- und Mutter-Tasche eingefügt wird, oder
2. die Mutter-Tasche für eine Vierkantmutter statt der aktuellen Muttergeometrie ausgelegt wird
   (Schlüsselweite/Breite entsprechend anpassbar).

Da alles ein reiner Durchgangsschnitt bleibt, ist keine Teiltiefen-/Pocket-Logik nötig — die neue
Geometrie ist einfach eine weitere durchgängig geschnittene Fläche (Kreis bzw. angepasste Box), die
mit den bestehenden Formen (`Part.fuse`) vereinigt wird, analog zur bestehenden
`screw_hole.fuse(nut_hole)`-Logik.

## Geplantes Vorgehen
1. `lasercut/tabproperties.py`: neue Properties ergänzen (Rückwärtskompatibilität: nur gesetzt,
   wenn noch nicht vorhanden, wie bei den bestehenden Properties):
   - `nut_flat_flat` (float, frei editierbar) — Schlüsselweite der Mutter (ersetzt bisher die
     ausschließlich intern aus `get_screw_nut_spec` berechnete Breite).
   - `nut_height` (float, frei editierbar) — Höhe/Länge der Mutter-Tasche.
   - `use_washer` (bool, Default `False`) — Unterlegscheiben-Tasche zusätzlich einfügen.
   - `washer_diameter` (float, frei editierbar) — Außendurchmesser der Unterlegscheibe.
   - `washer_thickness` (float, frei editierbar) — Dicke/Länge der Unterlegscheiben-Tasche.
   - Als Vorschlagswert (Default beim Anlegen einer neuen Verbindung) gilt: falls bereits an
     anderer Stelle im laufenden Programm ein Wert gesetzt wurde, diesen zuletzt verwendeten Wert
     vorschlagen (klassenweiter "letzter Wert"-Cache); ansonsten Fallback auf die bestehende
     `get_screw_nut_spec`-Tabelle (Mutter) bzw. einfache Standard-Washer-Maße (ISO 7089) für die
     Unterlegscheibe.
2. `lasercut/helper.py`:
   - Neue Funktion `get_washer_spec(screw_diameter)` mit Standard-Außendurchmessern/-Dicken
     (ISO 7089) als Vorschlagswert für neue Verbindungen.
3. `lasercut/join.py` (`screw_way_on_face`):
   - Mutter-Tasche verwendet künftig `tab.nut_flat_flat`/`tab.nut_height` statt der Werte aus
     `screw_nut_spec` (Vierkant- oder Sechskantmutter ist dadurch einfach eine andere
     Schlüsselweite/Höhe, keine eigene Typ-Unterscheidung im Code nötig).
   - Wenn `tab.use_washer`: zusätzliche zylindrische Durchgangs-Tasche (Radius aus
     `washer_diameter`, Länge aus `washer_thickness`, Höhe = `corrected_height` wie die anderen
     Taschen) direkt angrenzend zwischen `screw_hole` und `nut_hole` einfügen und mit den
     bestehenden Formen fusen (`Part.fuse`). Mutter- und Unterlegscheiben-Tasche sind gleichzeitig
     kombinierbar (kein Ausschluss).
4. `panel/tab.py` (`TSlotWidget`): UI-Felder für `nut_flat_flat`, `nut_height`, `use_washer`
   (Checkbox), `washer_diameter` und `washer_thickness` (letztere zwei nur sichtbar wenn
   `use_washer` aktiv, via bestehendem `parent_name`/`parent_value`-Mechanismus in
   `panel/toolwidget.py`).
5. Dokumentation `docs/interlocking.md` um die neuen Optionen ergänzen.

## Betroffene Dateien/Module
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `lasercut/helper.py`
- `panel/tab.py`
- `docs/interlocking.md`

## Entschiedene Punkte (vom Nutzer beantwortet)
1. **Position der Unterlegscheibe**: immer direkt angrenzend zwischen Schrauben- und Mutter-Tasche.
2. **Maße**: freie Felder für Mutter-Schlüsselweite/-Höhe und Washer-Breite/-Dicke, mit
   vorbelegtem Vorschlagswert (aus Tabelle bzw. zuletzt genutzten Werten).
3. **Kombination**: Mutter- und Unterlegscheiben-Tasche sind gleichzeitig nutzbar (kein Ausschluss).
4. **Geltungsbereich**: Property pro einzelner Schraubverbindung (Tab/Face); bei neu angelegten
   Verbindungen werden die zuletzt verwendeten Werte als Vorschlag vorbelegt.

