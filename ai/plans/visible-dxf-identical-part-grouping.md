# Plan: Identische sichtbare Bauteile als Mengen-DXF exportieren

## Ziel

Der sichtbare DXF-Export soll geometrisch identische Bauteile nur einmal als
DXF schreiben. Die Beschriftung dieser DXF gibt die Anzahl der sichtbaren
Instanzen an, damit die Datei direkt als Fertigungsmenge genutzt werden kann.

## Ausgangslage

`export_visible_parts()` in `ExportPanel.py` exportiert zurzeit jedes sichtbare
Volumenobjekt einzeln. Gleiche Labels werden lediglich durch Dateinamen wie
`bauteil_2.dxf` unterschieden. Zwei gleich geformte, verschieden platzierte
Objekte erzeugen daher doppelte DXF-Dateien.

## Geplantes Verhalten

1. Der Export sammelt weiterhin nur sichtbare Volumenkörper.
2. Er gruppiert geometrisch identische Körper unabhängig von ihrer Placement im
   Modell. Unterschiede in Kontur, Durchbrüchen oder Taschen ergeben getrennte
   Gruppen.
3. Pro Gruppe wird genau eine DXF erzeugt. Ihr Dateiname basiert auf dem ersten
   sichtbaren Objekt der Gruppe.
4. Die Ansichtsbeschriftung enthält zusätzlich `MENGE <Anzahl>`, zum Beispiel
   `MENGE 4`.
5. Im Abschlussdialog zählt jede geschriebene Gruppen-DXF als eine Datei und
   benennt die durch Gruppierung eingesparten Duplikate transparent.

## Vorgehen

1. In `ExportPanel.py` einen placementsunabhängigen Geometrievergleich für
   exportierbare Solids implementieren. Kompakte Kenndaten zu Volumen, Flaeche,
   Begrenzungsbox und Topologie dienen als Vorfilter; nur passende Kandidaten
   werden mit einem gemeinsamen Volumenvergleich bestaetigt. Bei nicht sicher
   vergleichbaren Shapes verbleiben Objekte in getrennten Gruppen.
2. `visible_export_objects()` unverändert als Sichtbarkeitsfilter verwenden
   und in `export_visible_parts()` die Objekte vor dem Export gruppieren.
3. `export_part_dxf()` und `_view_text()` um die Stückzahl der jeweiligen
   Gruppe ergänzen, ohne den bestehenden manuellen SVG-Export zu verändern.
4. Den FreeCAD-Regressionstest erweitern: zwei gleiche Körper an verschiedenen
   Positionen schreiben eine DXF mit `MENGE 2`; ein Körper mit abweichender
   Geometrie erzeugt eine zweite DXF.
5. `docs/export.md`, README und die Feature-Begleitdateien um das
   Mengenverhalten ergänzen.

## Betroffene Dateien

- `ExportPanel.py`
- `test/test_visible_dxf_freecad.py`
- `README.md`
- `docs/export.md`
- `ai/plans/visible-dxf-identical-part-grouping.memory.md`
- `ai/plans/visible-dxf-identical-part-grouping.README.md`

## Annahmen und offene Fragen

- Identisch bedeutet gleiche fertige Fräsgeometrie unabhängig von Position und
  Orientierung im Modell, nicht gleiche Labels oder gleiche Quellobjekte.
- Die erste sichtbare Instanz bestimmt Dateiname und Bauteilname der Gruppe.
- Eine Menge steht als `MENGE <Anzahl>` im `TEXT`-Layer; es entsteht kein
  separates Stücklistenformat.
- Unsichere oder ungültige Topologien werden bewusst nicht gruppiert, damit
  keine unterschiedlichen Teile versehentlich zu einer Fertigungsdatei
  zusammenfallen.

## Validierung

1. Den echten FreeCAD-DXF-Test mit zwei gleich geformten, verschieden
   platzierten Körpern sowie einem abweichenden Körper ausführen.
2. Prüfen, dass die resultierenden DXF-Dateien die erwartete Anzahl haben und
   die Gruppen-DXF `MENGE 2` im `TEXT`-Layer enthält.
3. `py_compile`, `git diff --check` und die bestehenden DXF-Regressionen
   ausführen.