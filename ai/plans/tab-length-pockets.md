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
- Neue Properties `through_tabs` (bool), `tab_length` (mm) und `tab_length_tolerance` (mm) pro
   Tab/Face, in allen Tab-Widgets.
- `through_tabs = True` bedeutet "Durchgang" und bleibt der Default fuer bestehende und neue
   Verbindungen. In diesem Modus wird die jeweilige Gegenmaterialdicke verwendet.
- `through_tabs = False` aktiviert verdeckte Taschen; `tab_length` ist dann eine absolute
   Zapfenlaenge entlang der lokalen X-Achse. `tab_length` muss in diesem Modus groesser als null
   sein.
- Die Geometrie wird nicht auf die Gegenmaterialdicke begrenzt: Werte groesser als die
   Materialdicke werden akzeptiert.
- `tab_join_create_tab_on_face` verwendet die gewaehlte Laenge fuer den Zapfen.
- `helper.tab_join_create_hole_on_plane` erzeugt automatisch eine Tasche mit der Tiefe
   `tab_length + tab_length_tolerance`; dadurch ist die Tasche um die definierte Toleranz tiefer
   als der Zapfen. Bei `through_tabs = True` bleibt es ein Durchgangsloch und die Toleranz wird
   ignoriert.
- Bei `through_tabs = True` bleibt das bisherige Durchgangsverhalten unveraendert.

## Betroffene Dateien/Module (vorlaeufig)
- `lasercut/tabproperties.py` — Properties/Defaults fuer `tab_length` und
   `tab_length_tolerance`.
- `lasercut/join.py` — Tab-Geometrie verwendet `tab_length`.
- `lasercut/helper.py` — Gegen-Tasche verwendet `tab_length` und passende Positionierung.
- `panel/tab.py` — Checkbox `through_tabs` sowie Eingabefelder fuer Zapfenlaenge und
   Laengentoleranz in `BaseTabWidget`, damit sie bei allen Tab-Typen verfuegbar sind; beide
   Laengenfelder werden nur bei deaktiviertem Durchgangsmodus angezeigt.
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
6. **Taschentiefe**: Im Taschenmodus wird die Tasche um `tab_length_tolerance` tiefer als der
   Zapfen erzeugt. Im Durchgangsmodus hat die Toleranz keine Wirkung.

## Naechster Schritt
Vor der Umsetzung ist noch der Defaultwert fuer `tab_length_tolerance` zu bestaetigen. Danach
wird der bestehende Feature-Branch verwendet und die Erweiterung feingranular implementiert.
