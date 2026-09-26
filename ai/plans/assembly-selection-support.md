# Plan: Assembly-Auswahl fuer Interlocking

## Ziel
LCInterlocking soll Komponenten eines FreeCAD-Assemblys als getrennte Teile erkennen. Wird eine
Komponente oder deren Flaeche ueber einen Assembly-Subelement-Pfad wie `Wall.Pad.Face1`
ausgewaehlt, muss sie als `Wall` registriert und die Flaeche dieser Komponente zugeordnet werden.

## Problem
FreeCAD liefert fuer beide aktuellen Auswahlen `Base.` und `Wall.` das Objekt `Assembly`. Die
eigentliche Komponente steht nur im Sub-Element-Pfad. Der bisherige Auswahlcode speichert daher
zweimal `Assembly` und kann eine Flaeche wie `Wall.Pad.Face1` keinem getrennt konfigurierten Teil
zuordnen. Daraus folgt die Meldung `Part of face Face1 is not configured`.

## Vorgehen
1. `panel/selection.py`: eine Aufloesung fuer Assembly-Subelement-Pfade ergaenzen. Sie bestimmt
   fuer eine Auswahl den ersten Pfadbestandteil (z.B. `Wall`) und loest ihn gegen das Dokument zu
   einer Komponenteninstanz auf.
2. Die Teil-Auswahl (`get_freecad_objects_list`) auf die aufgeloeste Komponenteninstanz umstellen;
   normale Part-/PartDesign-Auswahlen bleiben unveraendert.
3. Die Flächen-Auswahl (`get_freecad_faces_objects_list`) auf dieselbe Komponenteninstanz
   umstellen und den verbleibenden Face-Namen konsistent an LCInterlocking weitergeben.
4. `panel/treepanel.py`: Fehlermeldungen um den Objekt- und Sub-Element-Pfad erweitern, falls eine
   Assembly-Komponente nicht aufgeloest werden kann.
5. Das bereits behobene `None`-Index-Handling beibehalten.
6. Syntax- und Whitespace-Pruefung ausfuehren. Anschliessend in FreeCAD pruefen: `Base.` und
   `Wall.` als Teile hinzufuegen, je eine Flaeche waehlen und eine Tab-Verbindung erzeugen.

## Betroffene Dateien
- `panel/selection.py`
- `panel/treepanel.py`
- `ai/plans/assembly-selection-support.memory.md`
- `ai/plans/assembly-selection-support.README.md`

## Annahmen und offene Fragen
- Der erste Bestandteil eines Assembly-Subelement-Pfads ist der Name der Assembly-Komponente.
- Komponenteninstanzen sind ueber `Document.getObject(component_name)` erreichbar.
- Verschachtelte Assemblys werden zunaechst nur unterstuetzt, wenn der erste Pfadbestandteil die
  direkt selektierbare Komponenteninstanz bezeichnet.
- Eine echte Laufzeitvalidierung ist nur in FreeCAD moeglich; die lokale Shell hat kein
  `FreeCAD`-Python-Modul.