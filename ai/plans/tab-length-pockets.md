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
- Neue optionale Property `tab_length` (mm) pro Tab/Face.
- Rueckwaertskompatibler Default: volle Materialdicke (`0`/leer als "durchgehend" oder ein
  automatisch gesetzter Wert, noch zu entscheiden).
- `tab_join_create_tab_on_face` verwendet die gewaehlte Laenge entlang der lokalen X-Achse,
  begrenzt auf die Gegenmaterialdicke.
- `helper.tab_join_create_hole_on_plane` erzeugt passend dazu eine Tasche mit derselben Tiefe,
  statt immer die komplette Materialdicke zu schneiden.
- Bei voller Laenge bleibt das bisherige Durchgangsverhalten unveraendert.

## Betroffene Dateien/Module (vorlaeufig)
- `lasercut/tabproperties.py` — Property/Default fuer `tab_length`.
- `lasercut/join.py` — Tab-Geometrie verwendet `tab_length`.
- `lasercut/helper.py` — Gegen-Tasche verwendet `tab_length` und passende Positionierung.
- `panel/tab.py` — Eingabefeld fuer Zapfenlaenge in `BaseTabWidget` oder den relevanten Widgets.
- `docs/interlocking.md` — Beschreibung von Durchgangszapfen vs. verdeckten Taschen.

## Offene Fragen (bitte beantworten)
1. **Bedeutung der Laenge**: Soll `tab_length` eine absolute Laenge in mm sein, oder ein relativer
   Anteil der Gegenmaterialdicke (z.B. 50%)?
2. **Standardwert/Durchgang**: Soll der Default die volle Materialdicke sein, oder soll `0`/leer
   explizit "Durchgang" bedeuten und ein positiver Wert eine Tasche aktivieren?
3. **Einseitig oder beidseitig**: Soll die Einstellung nur fuer die Zapfen gelten (Zapfen ragen
   kuerzer in das Gegenmaterial), waehrend die bestehende Gegen-Tasche automatisch passend tief
   wird? Oder sollen auch andere bestehende Durchgangsloecher/-geometrien begrenzt werden?
4. **Laenge bei Materialdicke**: Wenn `tab_length` groesser als die Gegenmaterialdicke ist, soll
   auf die Materialdicke begrenzt werden oder ein Fehler angezeigt werden?
5. **Geltungsbereich**: Soll `tab_length` in allen Tab-Widgets (`Tab`, `Screw`, `WoodScrew`, ggf.
   `Continuous`) erscheinen, oder nur bei `Tab`/`Screw`/`WoodScrew`?

## Naechster Schritt
Nach Beantwortung wird der Plan konkretisiert und zur Freigabe vorgelegt. Erst danach wird ein
Feature-Branch angelegt und implementiert.
