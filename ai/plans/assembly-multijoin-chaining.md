# Plan: Assembly-MultiJoin-Verkettung

## Ziel
Nach einem MultiJoin mit Assembly-Komponenten sollen die Ursprungslinks im Assembly erhalten
bleiben und die erzeugten Teile fuer weitere Interlocking-Verbindungen mit anderen
Assembly-Komponenten verwendbar sein. Insbesondere darf `Base` nicht mehr aus dem
Assembly-Container in `MultiJoin_origin_parts` verschoben werden.

## Ursache
`MultipleJoinGroup.execute()` fuegt jedes Ursprungsobjekt mit
`MultiJoin_origin_parts.addObject(freecad_obj)` in eine Dokumentgruppe ein. Bei einem
`App::Link` aus einem Assembly verschiebt FreeCAD das Linkobjekt dadurch aus dem Assembly.
Das erzeugte `Base_tab` wird zudem als freistehendes `Part::Feature` angelegt.

## Vorgehen
1. `panel/multiplejoins.py`: Assembly-Links erkennen und nicht mehr in
   `MultiJoin_origin_parts` verschieben. Der Link bleibt Mitglied seines bisherigen
   Assembly-Containers und wird lediglich im MultiJoin referenziert.
2. Die Ursprungsgruppenlogik so anpassen, dass nur nicht-Assembly-Objekte als Kinder der
   `MultiJoin_origin_parts`-Gruppe organisiert werden; die Edit-/Sichtbarkeitslogik muss beide
   Kategorien weiterhin korrekt behandeln.
3. Fuer die erzeugten Parts die bestehende globale Platzierung beibehalten, aber eine verlässliche
   Auswahl mit Assembly-Komponenten fuer weitere MultiJoins sicherstellen. Falls die Assembly API
   es zulaesst, wird ein erzeugtes Teil als Assembly-kompatibler Link oder Teil in denselben
   Assembly-Kontext eingefuegt; andernfalls bleibt es freistehend und wird explizit fuer die
   Kombination mit Assembly-Links unterstuetzt.
4. `panel/selection.py`: die Komponentenauflösung fuer bereits erzeugte `Part::Feature`-Teile und
   fuer Assembly-Links gemeinsam testen, damit ein zweiter MultiJoin `Base_tab` und `Wall001`
   aufnehmen kann.
5. Dokumentation ergaenzen: MultiJoin-Ausgabe kann als Eingabe fuer eine weitere Verbindung
   dienen; Assembly-Ursprungslinks werden nicht aus dem Assembly entfernt.
6. Syntax- und Whitespace-Pruefung ausfuehren sowie in FreeCAD pruefen:
   - `Base` und `Wall` verbinden,
   - kontrollieren, dass `Base` im Assembly bleibt,
   - `Base_tab` mit `Wall001` erneut verbinden,
   - Preview und finalen MultiJoin pruefen.

## Betroffene Dateien
- `panel/multiplejoins.py`
- `panel/selection.py` (nur falls fuer Misch-Auswahlen erforderlich)
- `docs/interlocking.md`
- `README.md`
- `ai/plans/assembly-multijoin-chaining.memory.md`
- `ai/plans/assembly-multijoin-chaining.README.md`

## Annahmen und offene Fragen
- Assembly-Komponenten sind `App::Link`-Objekte und koennen ueber `LinkedObject` erkannt werden.
- Ein Assembly-Link darf nicht in eine andere `App::DocumentObjectGroup` verschoben werden.
- Ob die erzeugten `Part::Feature`-Objekte als direkte Assembly-Mitglieder eingefuegt werden
  duerfen, muss mit der vorhandenen Assembly-API in FreeCAD getestet werden.
- Bis zur manuellen FreeCAD-Pruefung wird der kleinste sichere Schritt bevorzugt: Ursprungslinks
  im Assembly behalten und eine weitere Verbindung mit dem freistehenden Ergebnis ermoeglichen.