# Assembly-Auswahl fuer Interlocking

## Zweck
Ermoeglicht, Komponenten eines FreeCAD-Assemblys im Interlocking-Dialog als getrennte Teile zu
verwenden.

## Verwendung
Komponenten im Assembly auswaehlen und mit **Add parts** hinzufuegen. Danach die Flaechen derselben
Komponenten auswaehlen und mit **Add faces** oder **Add same faces** verbinden.

Auch wenn FreeCAD beim Klick auf eine Flaeche das innere PartDesign-Feature eines externen
`App::Link` auswaehlt, ordnet LCInterlocking die Flaeche wieder der Assembly-Komponente zu.

## Relevante Dateien
- `panel/selection.py`
- `panel/treepanel.py`