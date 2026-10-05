# Plan: Sichtbare Bauteile als einzelne DXF exportieren

## Ziel
Ein neuer LCInterlocking-Exportcommand schreibt alle aktuell sichtbaren,
exportierbaren Bauteile des aktiven Dokuments als einzelne DXF-Dateien in einen
vom Benutzer gewaehlten Ordner. Jede Datei enthaelt die fuer die Fertigung
geeigneten 2D-Fräsansichten eines Bauteils, einschliesslich Beschriftungen fuer
Bearbeitungsseite und Taschentiefe. Alle Ansichten eines Bauteils liegen
nebeneinander in derselben DXF-Datei.

## Ausgangslage
Der vorhandene Command `export_command` verarbeitet ausschliesslich die
manuelle Auswahl. Er erzeugt ein separates FreeCAD-Dokument, richtet jedes
Shape nach seiner groessten Flaeche aus und erstellt `Draft.makeShape2DView`-
Objekte. Er schreibt keine DXF-Dateien und betrachtet keine Sichtbarkeit.

FreeCAD 1.1 stellt die Draft-Schnittstelle `importDXF` bereit. Damit kann die
vorhandene 2D-Projektion pro Bauteil als echte DXF-Datei gespeichert werden,
ohne eine weitere Python-Abhaengigkeit einzufuehren.

## Geplantes Verhalten
1. Ein neuer Toolbar- und Menuecommand, zum Beispiel **Export visible DXF**,
   ist aktiv, wenn ein Dokument geoeffnet ist.
2. Nach dem Start waehlt der Benutzer einen Zielordner. Ein Abbruch erzeugt
   weder Dokumente noch Dateien.
3. Der Command sammelt die im FreeCAD-Modellbaum sichtbaren geometrischen
   Blattobjekte. Massgeblich ist der View-Status, der im Baum mit der
   Leertaste ein- oder ausgeschaltet wird; die aktuelle 3D-Auswahl spielt
   keine Rolle. Gruppen, Urspruenge, Helper und im Baum ausgeblendete
   Quellobjekte werden nicht selbst exportiert. Sichtbare, erzeugte Ergebnisse
   wie HoleTemplate- oder MultiJoin-`Part::Feature`-Objekte werden hingegen
   bevorzugt exportiert.
4. Die Analyse bestimmt Frässeiten aus Paaren paralleler Außenflächen. Das
   dominante Flächenpaar definiert zuerst Ober- und Unterseite; zusätzliche
   orthogonale Flächenpaare werden berücksichtigt, wenn auf ihnen Taschen
   liegen.
5. Eine Seite erhaelt eine Fräsansicht, wenn sie Taschen besitzt: Das sind
   innenliegende, zur Außenfläche parallele Bodenflächen mit einem Abstand
   kleiner als die Materialstärke. Jede Fräsansicht enthält immer die
   vollständige Außenkontur, Durchbrüche und die Taschen dieser Seite; sie ist
   damit direkt als einzelne Spannlage in Estlcam verwendbar.
6. Taschen auf Ober- und Unterseite ergeben zwei Ansichten. Liegen Taschen an
   weiteren Seiten, ergänzt der Export die nötigen dritte und vierte Ansicht.
   Bauteile ohne Taschen erhalten eine Standardansicht mit Außenkontur und
   Durchbrüchen.
7. Jede Ansicht wird mit dem Bauteilnamen, einer eindeutigen Seitenkennung wie
   `OBEN`, `UNTEN`, `SEITE RECHTS` oder `SEITE LINKS`, der
   Materialstaerke und den gefundenen Taschentiefen als Draft-Text in der DXF
   beschriftet. Die Taschentiefen werden relativ zur jeweiligen Frässeite
   angegeben, zum Beispiel `TASCHE 8.00 mm`.
8. Alle Ansichten eines Bauteils werden mit festem Abstand nebeneinander in
   einer `.dxf`-Datei angeordnet. Der Dateiname wird aus `Label`/`Name`
   gebildet, fuer Dateien bereinigt und bei Duplikaten stabil nummeriert.
9. Die Geometrie jeder Ansicht wird in DXF-Layer aufgeteilt: `KONTUR` fuer die
   Außenkontur, `DURCHBRUCH` fuer durchgehende Innenkonturen und `TEXT` fuer
   Beschriftungen. Taschengeometrie wird je gefundener Tiefe auf einen eigenen
   Layer wie `TASCHE_8_00MM` gelegt. Das erlaubt in Estlcam die direkte
   Zuordnung einer Fräsoperation pro Taschentiefe.
10. Der Command meldet nach Abschluss die Anzahl geschriebener DXF-Dateien und
   jene sichtbaren Objekte, die keine exportierbare Shape hatten.
11. Der bestehende manuelle Exportcommand bleibt unveraendert erhalten.

## Vorgehen
1. In `ExportPanel.py` eine klar getrennte Sichtbarkeits- und
   Exportkandidaten-Ermittlung implementieren. Sie wertet den im Modellbaum
   gesetzten `ViewObject.Visibility`-Status aus, verwendet reale sichtbare
   Blattobjekte und verhindert Doppel-Exporte von Quellen, die durch sichtbare
   generierte Ergebnisse ersetzt wurden.
2. Eine Helper-Funktion fuer sichere DXF-Dateinamen und kollisionsfreie
   Zielpfade erstellen.
3. Eine Topologieanalyse implementieren: Gegenueberliegende Außenflächen
   bestimmen, ihre Normalen orientieren und parallele Innenflächen als
   Taschenböden klassifizieren. Die Tiefen werden als Abstand vom jeweiligen
   Außenflächen-Niveau berechnet und gleichartige Tiefen zusammengefasst.
4. Die vorhandene Projektion/Ausrichtung in eine wiederverwendbare
   Einzelansicht-Funktion ueberfuehren. Sie erzeugt für jede Frässeite immer
   Außenkontur und Durchbrüche sowie zusätzlich die Taschengeometrien aus der
   gewaehlten Richtung. Die erzeugten 2D-Objekte erhalten die DXF-Layer
   `KONTUR`, `DURCHBRUCH`, `TEXT` oder einen aus der Taschentiefe abgeleiteten
   `TASCHE_<TIEFE>MM`-Layer. Alle Ansichten eines Bauteils werden in einem
   temporaeren FreeCAD-Dokument neben- und kollisionsfrei platziert.
5. Beschriftungen als Draft-Text mit Bauteilname, Seite, Materialstaerke und
   Taschentiefe erzeugen. Den DXF-Export mit `importDXF.export()` auf alle
   Projektionen und Texte eines Bauteils anwenden. Fehler eines einzelnen
   Bauteils werden gesammelt; verbleibende Bauteile werden weiter exportiert.
6. Command in `InitGui.py` registrieren und einen passenden Icon-/Tooltip-Text
   nach lokalem Stil ergaenzen.
7. Einen fokussierten echten FreeCAD-Test hinzufuegen: ein Bauteil mit Taschen
   auf mehreren Seiten erzeugt eine DXF-Datei mit mehreren beschrifteten
   Ansichten; einseitige Taschen erzeugen nur die zugehoerige Ansicht; ein
   unsichtbares Shape wird ausgelassen; mehrfache Labels erzeugen eindeutige
   Namen.
8. README und `docs/export.md` um Workflow, Taschenansichten und
   Ergebnisdateien ergaenzen.

## Betroffene Dateien
- `ExportPanel.py`
- `InitGui.py`
- `test/test_holetemplate_freecad.py` oder ein neuer fokussierter FreeCAD-Test
- `README.md`
- `docs/export.md`
- `ai/plans/visible-dxf-export.memory.md` (nach Freigabe)
- `ai/plans/visible-dxf-export.README.md` (nach Freigabe)

## Annahmen und offene Fragen
- Die Funktion richtet sich vorrangig an flache Plattenbauteile, kann bei
   Taschen auf seitlichen Außenflächen aber weitere orthogonale Ansichten
   erzeugen. Formteile ohne eine eindeutig zuordenbare Taschenrichtung werden
   mit einer klaren Warnung uebersprungen.
- Pro sichtbarer Komponente entsteht genau eine DXF. Sie enthält je Spannlage
   eine vollständige, beschriftete Bearbeitungsansicht mit Kontur, Durchbrüchen
   und den Taschen dieser Seite. Die Ansichten liegen nebeneinander.
- Die DXF-Layer `KONTUR`, `DURCHBRUCH` und `TEXT` sowie ein eigener
   `TASCHE_<TIEFE>MM`-Layer je Taschentiefe sind für Estlcam gedacht. Die
   Zuordnung konkreter Frässtrategien und Werkzeuge bleibt in Estlcam beim
   Benutzer.
- Eine Tasche ist in der ersten Version eine zur Frässeite parallele,
   innenliegende Bodenflaeche. Schräge oder gekruemmte Taschenflaechen werden
   nicht automatisch klassifiziert und muessen vor dem Fräsen manuell geprueft
   werden.
- Der Zielordner wird bei jedem Aufruf im Dialog abgefragt; die letzte Auswahl
  wird in dieser ersten Version nicht persistent gespeichert.
- Sichtbarkeit folgt ausschließlich dem aktuellen Modellbaum-Status
   (`ViewObject.Visibility`), nicht der aktuellen Auswahl. Unsichtbare Quellen
   hinter sichtbaren HoleTemplate-/MultiJoin-Ergebnissen werden nicht erneut
   exportiert.

## Validierung
1. Echten FreeCAD-Test mit ein-, zwei- und mehrseitigen Taschen sowie
   sichtbaren und unsichtbaren `Part::Feature`-Objekten ausfuehren. Nichtleere
   DXF-Dateien mit getrennten, beschrifteten Ansichten und den erwarteten
   Estlcam-Layern pruefen.
2. Bestehende Export-/HoleTemplate-Regression und `py_compile` der geaenderten
   Module ausfuehren.
3. `git diff --check` ausfuehren.
4. Manuell im GUI einen Assembly-/HoleTemplate-Stand exportieren und pruefen,
   dass nur die sichtbaren Endergebnisse im Zielordner liegen.