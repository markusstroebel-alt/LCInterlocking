# Plan: Auswählbare Form des Mutter-Slots (Vierkantmutter / Unterlegscheibe)

## Ziel/Beschreibung
Aktuell erzeugt der T-Slot/Screw-Verbindungstyp (`lasercut/join.py:screw_way_on_face`) immer eine
rechteckige Tasche für die Mutter (Breite = `nut_flat_flat`, Länge = `nut_height`), passend für eine
Vierkant-/Sechskantmutter mit Verdrehsicherung. Der Nutzer möchte stattdessen wahlweise auch eine
runde Tasche für eine Unterlegscheibe (Washer) erzeugen können, z.B. wenn keine Mutter, sondern nur
eine Unterlegscheibe unter dem Schraubenkopf/der Mutter sitzt.

## Geplantes Vorgehen
1. `TabProperties` (lasercut/tabproperties.py) um ein neues Property `nut_slot_type` erweitern
   (z.B. Werte `"square_nut"` / `"washer"`), Default = `"square_nut"` (Rückwärtskompatibilität).
2. Bei `nut_slot_type == "washer"` zusätzliche Dimensionen benötigt: Außendurchmesser der
   Unterlegscheibe (`washer_diameter`) und ggf. `washer_thickness` (falls abweichend von
   `nut_height`). Neue Properties dafür ergänzen.
3. `panel/tab.py` (`TSlotWidget`): Dropdown/Auswahl für `nut_slot_type` ergänzen sowie die neuen
   Washer-Felder nur anzeigen, wenn `washer` ausgewählt ist (falls das UI-Framework das unterstützt,
   sonst immer anzeigen).
4. `lasercut/join.py` (`screw_way_on_face`): Erzeugung der Mutter-Tasche abhängig von
   `nut_slot_type` verzweigen:
   - `square_nut`: bestehende Box-Logik (unverändert).
   - `washer`: zylindrische Tasche mit Radius aus `washer_diameter`, Tiefe wie bisher
     `corrected_height`, optional mit Dog-Bone-Logik (falls sinnvoll für runde Form) oder ohne.
5. `lasercut/helper.py` (`get_screw_nut_spec`): ggf. Standard-Washer-Maße pro Schraubendurchmesser
   ergänzen (ähnlich der bestehenden Nut-Tabelle), damit sinnvolle Defaults vorgeschlagen werden.
6. Dokumentation `docs/interlocking.md` um die neue Option ergänzen.

## Betroffene Dateien/Module
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `lasercut/helper.py`
- `panel/tab.py`
- `docs/interlocking.md`

## Offene Fragen/Annahmen (Nutzer nicht erreichbar, autonom entschieden)
1. **Ersetzt vs. zusätzlich**: Die Unterlegscheiben-Tasche *ersetzt* die Mutter-Tasche komplett
   (Auswahl ist eine Alternative: entweder Vierkantmutter ODER Unterlegscheibe), keine Kombination.
2. **Standardmaße**: Es wird eine Default-Tabelle für Unterlegscheiben-Außendurchmesser/-Dicke je
   Schraubendurchmesser angelegt (analog zur bestehenden `get_screw_nut_spec`-Tabelle in
   `lasercut/helper.py`), die der Nutzer bei Bedarf überschreiben kann.
3. **Keine Verdrehsicherung**: Die Unterlegscheiben-Tasche ist ein einfacher runder Ausschnitt ohne
   Anti-Rotation (Dog-Bone-Option bleibt für diese Form deaktiviert/ignoriert, da bei runden Formen
   nicht sinnvoll).
4. **Geltungsbereich**: Die Auswahl `nut_slot_type` ist ein Property pro Schraubverbindung
   (Tab/Face), analog zu den bestehenden Properties wie `screw_diameter`, nicht global fürs Projekt.

