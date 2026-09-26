# Fortschritt: Assembly-Auswahl fuer Interlocking

- Plan freigegeben und umgesetzt.
- Reproduzierbarer Fall: `selection.Object` ist `Assembly`, die Komponenten stehen nur in
  Sub-Element-Pfaden wie `Base.` und `Wall.Pad.Face1`.
- Die Auswahl muss auf die jeweilige Komponenteninstanz aufgeloest werden, nicht auf den
  Assembly-Container.
- `panel/selection.py` loest den ersten Pfadbestandteil gegen das Dokument auf und speichert fuer
  Flaechen nur noch den lokalen Namen wie `Face1`.
- Ein isolierter Test mit `Base.`, `Wall.` und `Wall.Pad.Face1` ist erfolgreich; Python-Syntax und
  `git diff --check` sind ebenfalls erfolgreich.
- Offener Punkt: Manuelle Pruefung im FreeCAD-Assembly, da keine FreeCAD-Kommandozeile vorhanden
  ist.