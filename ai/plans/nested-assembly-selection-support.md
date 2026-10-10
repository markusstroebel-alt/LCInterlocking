# Plan: Sichere Auswahl in verschachtelten Assemblys

## Ziel
Alle auswahlbasierten LCInterlocking-Werkzeuge sollen Komponenten auch in
verschachtelten FreeCAD-Assemblys eindeutig und mit ihrer tatsaechlich
platzierten Instanz verarbeiten. Das betrifft MultiJoin/Interlocking,
Crosspiece, Living Hinge, Hole templates und Export.

## Ausgangslage
Die meisten Werkzeuge verwenden bereits `panel.selection`. Die aktuelle
Aufloesung erkennt direkte `App::Link`-Auswahlen und durchsucht `Group`-
Kinder, verfolgt aber nicht rekursiv `LinkedObject`-Ketten. Bei einer Auswahl
eines inneren Body oder Pad kann sie daher nicht sicher die konkrete Instanz
einer verschachtelten Subassembly bestimmen. `ExportPanel.py` hat zudem eine
separate, nicht Assembly-sichere Auswahlabfrage.

## Geplantes Verhalten
1. Eine zentrale Resolver-API ermittelt fuer jede Auswahl sowohl die konkrete,
   platzierte Komponente als auch den lokalen Sub-Element-Namen.
2. Ein vollständiger Subelement-Pfad, etwa
   `OuterAssembly.SubAssembly.Wall.Pad.Face1`, wird schrittweise gegen die
   echten Link- und Gruppenobjekte aufgeloest. Die Rueckgabe ist die tiefste
   eindeutige, selektierte Instanz, deren Shape die verwendete Platzierung
   traegt.
3. Direkte `App::Link`-Auswahlen behalten immer Vorrang. Bei mehreren
   gleichartigen Instanzen wird nie stillschweigend geraten: Der explizite
   Pfad wird verwendet oder die Auswahl wird mit einer eindeutigen Fehlermeldung
   abgelehnt.
4. `get_freecad_objects_list()` und `get_freecad_faces_objects_list()` nutzen
   ausschliesslich diesen Resolver. So profitieren MultiJoin, Crosspiece,
   Living Hinge und Hole templates ohne eigene Sonderlogik.
5. Export wird auf dieselbe Objekt-Aufloesung umgestellt, damit ein Export der
   aktuell ausgewählten verschachtelten Komponenten ihre Platzierung verwendet.
6. Nicht auswahlbasierte Generatoren (Box, Rounded Box) bleiben unveraendert.

## Vorgehen
1. `panel.selection` um eine klar benannte Resolverfunktion erweitern, die
   Pfadsegmente, `Group`-Kinder und `LinkedObject`-Ketten zyklussicher
   durchlaeuft. Die bisherige heuristische Dokumentsuche wird nur als
   kontrollierter Rueckfall fuer direkte Objektselektionen beibehalten.
2. Die Objekt- und Face-Listen auf eine gemeinsame strukturierte
   Resolverrueckgabe umstellen. Face-Namen muessen dabei auf den lokalen Namen
   der aufgeloesten Instanz reduziert werden.
3. `ExportPanel.get_freecad_object()` durch den gemeinsamen Resolver ersetzen.
4. Alle Aufrufer im `TreePanel`, Living Hinge und HoleTemplate auf gleiche
   Fehlerbehandlung pruefen. Bestehende bevorzugte Komponentenlisten fuer
   MultiJoin bleiben erhalten.
5. Die FreeCAD-AppImage-Tests um ein verschachteltes Modell erweitern:
   - eine direkte Linkinstanz,
   - eine Subassembly mit innerem Link,
   - zwei Instanzen derselben Quelle,
   - Face-Aufloesung und Objekt-Aufloesung,
   - Export-Eingabe ohne Verlust der Placement-Instanz.
6. In FreeCAD manuell fuer jedes Werkzeug pruefen: MultiJoin, Crosspiece,
   Living Hinge, Hole templates und Export mit einer tief verschachtelten
   Komponente. Kontrollieren, dass kein Quelllink verschoben und keine falsche
   Instanz bearbeitet wird.
7. README und relevante Fachanleitungen um die sichere Auswahlregel
   aktualisieren. Begleitende Memory- und Nutzer-README-Dateien waehrend der
   Umsetzung pflegen.

## Betroffene Dateien
- `panel/selection.py`
- `panel/treepanel.py`
- `panel/livinghinge.py` (falls Fehlerbehandlung angepasst wird)
- `panel/holetemplates.py` (nur fuer gemeinsame Resolvernutzung)
- `ExportPanel.py`
- `test/test_holetemplate_freecad.py` oder ein neuer fokussierter
  Assembly-Auswahltest
- `README.md`
- `docs/interlocking.md`
- `docs/export.md`
- `ai/plans/nested-assembly-selection-support.memory.md`
- `ai/plans/nested-assembly-selection-support.README.md`

## Annahmen und Risiken
- Die genaue Form der `SubElementNames` wird durch die verwendete
  FreeCAD-Assembly-Version bestimmt. Der Resolver muss daher sowohl direkte
  Linkselektion als auch explizite Pfade robust behandeln.
- Eine echte GUI-Auswahl tief verschachtelter Links ist im headless Test nur
  begrenzt simulierbar. Daher sind automatisierte Resolvertests und ein
  manueller Werkzeugtest in FreeCAD beide erforderlich.
- Dieses Vorhaben betrifft zentrale Auswahl-Infrastruktur. Es wird in kleinen,
  jeweils testbaren Schritten umgesetzt, damit normale Part-/Body-Auswahlen
  unveraendert bleiben.