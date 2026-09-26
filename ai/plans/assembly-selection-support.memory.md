# Fortschritt: Assembly-Auswahl fuer Interlocking

- Plan freigegeben und umgesetzt.
- Reproduzierbarer Fall: `selection.Object` ist `Assembly`, die Komponenten stehen nur in
  Sub-Element-Pfaden wie `Base.` und `Wall.Pad.Face1`.
- Die Auswahl muss auf die jeweilige Komponenteninstanz aufgeloest werden, nicht auf den
  Assembly-Container.
- Die Teileauswahl loest Assembly-Pfade wie `Base.` und `Wall.` gegen das Dokument auf.
- FreeCAD loest die Flächenauswahl bereits bis zur Komponenteninstanz auf: Bei einer Auswahl von
  `Wall.Pad.Face1` ist das Objekt `Wall` und der Restpfad `Pad.Face1`. Die Flächenauswahl behält
  deshalb das gelieferte Objekt bei und speichert nur den lokalen Namen `Face1`.
- Bei Auswahl des externen Quelldokuments kann FreeCAD stattdessen `Pad` liefern. Die aktive
  Assembly wird dann nach `App::Link`-Komponenten durchsucht, deren `LinkedObject`-Body das Pad
  enthaelt; die Auswahl wird wieder der Komponente `Wall` zugeordnet.
- Die getestete `Wall.FCStd` bestaetigt, dass ihr `Body` das Pad enthaelt. Isolierte Tests fuer
  beide Auswahlformen, Python-Syntax und `git diff --check` sind erfolgreich.
- Offener Punkt: Manuelle Pruefung im FreeCAD-Assembly, da keine FreeCAD-Kommandozeile vorhanden
  ist.