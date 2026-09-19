# Plan: Einstellbare Zapfenlaenge und verdeckte Zapfen-Taschen

## Ziel/Beschreibung
Aktuell reicht ein erzeugter Zapfen (`tab_join_create_tab_on_face` in `lasercut/join.py`) immer ueber
die komplette Dicke des Gegenmaterials (`corrected_length = material_plane.thickness`). Der Nutzer
moechte die Zapfenlaenge optional kuerzer einstellen koennen, damit die Zapfen nicht durch die
Gegenplatte ragen, sondern in gefraesten Taschen enden.

Die Einstellung soll generell fuer die Verbindungsarten gelten, die Zapfen erzeugen, insbesondere
`Tab`, `Screw` und `WoodScrew`. Der Gegenpart muss dann eine Tasche mit der entsprechenden Tiefe
statt eines Durchgangslochs erhalten.

## Technische Leitidee
- Neue Properties `through_tabs` (bool) und `tab_length` (mm) pro Tab/Face, in allen Tab-Widgets.
- `through_tabs = True` bedeutet "Durchgang" und bleibt der Default fuer bestehende und neue
   Verbindungen. In diesem Modus wird die jeweilige Gegenmaterialdicke verwendet.
- `through_tabs = False` aktiviert verdeckte Taschen; `tab_length` ist dann eine absolute
   Zapfenlaenge entlang der lokalen X-Achse. `tab_length` muss in diesem Modus groesser als null
   sein.
- Die Geometrie wird nicht auf die Gegenmaterialdicke begrenzt: Werte groesser als die
   Materialdicke werden akzeptiert.
- `tab_join_create_tab_on_face` verwendet die gewaehlte Laenge fuer den Zapfen.
- `helper.tab_join_create_hole_on_plane` erzeugt automatisch eine Tasche mit derselben Tiefe; bei
   `through_tabs = True` bleibt es ein Durchgangsloch.
- Bei `through_tabs = True` bleibt das bisherige Durchgangsverhalten unveraendert.

## Betroffene Dateien/Module (vorlaeufig)
- `lasercut/tabproperties.py` — Property/Default fuer `tab_length`.
- `lasercut/join.py` — Tab-Geometrie verwendet `tab_length`.
- `lasercut/helper.py` — Gegen-Tasche verwendet `tab_length` und passende Positionierung.
- `panel/tab.py` — Checkbox `through_tabs` und Eingabefeld fuer Zapfenlaenge in `BaseTabWidget`,
   damit beides bei allen Tab-Typen verfuegbar ist; `tab_length` wird nur bei deaktiviertem
   Durchgangsmodus bearbeitbar/angezeigt.
- `docs/interlocking.md` — Beschreibung von Durchgangszapfen vs. verdeckten Taschen.

## Entschiedene Punkte (vom Nutzer beantwortet)
1. **Bedeutung der Laenge**: `tab_length` ist eine absolute Laenge in Millimetern, wenn der
   Durchgangsmodus deaktiviert ist.
2. **Standardwert/Durchgang**: `through_tabs = True` bedeutet Durchgang und ist der Default;
   `0` wird nicht mehr als Modus-Sentinel verwendet.
3. **Einseitig oder beidseitig**: Die Zapfenlaenge und die automatisch erzeugte Gegen-Tasche
   werden gemeinsam angepasst; andere Durchgangsloecher bleiben unveraendert.
4. **Laenge bei Materialdicke**: Werte groesser als die Gegenmaterialdicke werden akzeptiert und
   nicht auf die Dicke begrenzt.
5. **Geltungsbereich**: Das Feld erscheint in allen Tab-Widgets, einschliesslich `Tab`, `Screw`,
   `WoodScrew` und `Continuous`.

## Naechster Schritt
Der konkretisierte Plan muss vor der Umsetzung noch explizit freigegeben werden. Danach wird ein
Feature-Branch angelegt und feingranular implementiert.
