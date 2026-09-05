# Feature: Auswählbare Mutter-Slot-Form (Vierkantmutter / Unterlegscheibe)

## Zweck
Beim Schraub-Verbindungstyp (T-Slot/"Screw") kann jetzt pro Verbindung gewählt werden, ob die Tasche
auf der Material-Fläche für eine Vierkant-/Sechskantmutter (rechteckig, wie bisher) oder für eine
Unterlegscheibe (rund) ausgelegt wird.

## Nutzung
In den Eigenschaften einer Screw-Verbindung (Panel "Slots" bzw. Tab-Eigenschaften) steht ein neues
Feld **"Nut slot type"** zur Verfügung:
- **Square nut** (Standard): wie bisher, rechteckige Tasche passend zur Mutterschlüsselweite.
- **Washer**: runde Tasche passend zum Außendurchmesser einer Unterlegscheibe, ersetzt die
  Mutter-Tasche komplett.

## Relevante Dateien
- `lasercut/tabproperties.py` — neues Property `nut_slot_type`
- `lasercut/helper.py` — Standardmaße für Unterlegscheiben je Schraubendurchmesser
- `lasercut/join.py` — Erzeugung der runden bzw. rechteckigen Tasche
- `panel/tab.py` — UI-Auswahlfeld im `TSlotWidget`
- `docs/interlocking.md` — Dokumentation
