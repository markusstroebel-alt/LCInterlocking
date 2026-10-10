# Plan: Verwaltete Lochschablonen im Baum

## Ziel
Der Befehl **Hole templates** soll nicht mehr bei jeder Ausfuehrung eine neue
`HoleTemplates`-Gruppe mit losen Ergebnisobjekten anlegen. Stattdessen erzeugt
er ein eigenes `Part::FeaturePython`-Objekt `HoleTemplate`, das als ein
Baumknoten alle erzeugten Ergebnisse verwaltet, im Kontextmenue bearbeitbar
bleibt und bei der Neuberechnung vorhandene Ergebnisse wiederverwendet.

## Geplantes Verhalten
1. Beim Bestaetigen des Task-Panels entsteht ein `HoleTemplate`-Objekt mit
   ViewProvider und einem Kindknoten fuer die generierten Zielteile.
2. Das Objekt speichert die Rollen als Namen, nicht als `PropertyLink`, damit
   Assembly-Container keine Scope-Warnungen erzeugen.
3. `generatedParts` verknuepft die erzeugten `Part::Feature`-Ergebnisse nur
   mit dem verwaltenden Objekt. `claimChildren()` zeigt diese im Baum unter
   `HoleTemplate` an.
4. Eine erneute Berechnung verwendet Ergebnisobjekte mit derselben stabilen
   Ziel-Namenszuordnung wieder, aktualisiert ihre Shapes und entfernt veraltete
   Ergebnisse.
5. Im Edit-Modus werden die erzeugten Teile ausgeblendet und die beteiligten
   Ausgangsteile sichtbar. Nach Bestaetigung wird diese Sichtbarkeit umgedreht.
   Bei `App::Link`-Assembly-Komponenten werden keine Objekte verschoben.
6. Das Kontextmenue des `HoleTemplate`-Objekts bietet **Edit**, um das
   bestehende Task-Panel mit den gespeicherten Template- und Zielrollen zu
   oeffnen.

## Vorgehen
1. `panel/holetemplates.py` in drei zusammenarbeitende Bereiche trennen:
   `HoleTemplateGroup` fuer persistente Eigenschaften und Berechnung,
   `HoleTemplateViewProvider` fuer Baum/Edit-Modus sowie das bestehende
   Task-Panel fuer Rollenwahl und Vorschau.
2. Im Task-Panel gespeicherte Namen in FreeCAD-Objekte aufloesen und beim Edit
   die drei Listen anhand der bestehenden Rollen vorbelegen. Abgebrochene
   Bearbeitungen stellen die vorherigen Namen wieder her.
3. Die Differenzberechnung weiterhin ueber `lasercut/holetemplate.py` ausfuehren
   und die Ergebnisse mit einer stabilen `namesMapping`-Zuordnung aktualisieren.
4. Die bisher direkt erzeugte `HoleTemplates`-Dokumentgruppe entfernen. Neue
   Resultate werden ausschliesslich durch den ViewProvider unter dem
   `HoleTemplate`-Feature beansprucht.
5. Tests ergaenzen fuer die persistente Namenszuordnung, Wiederverwendung und
   Entfernung alter Ergebnisse; den realen FreeCAD-AppImage-Test um die
   FeaturePython-Eigenschaften und Tree-Kinder erweitern.
6. README und `docs/hole_templates.md` auf die neue Bearbeitung im Baum
   aktualisieren. Die zugehoerige Memory- und Nutzer-README-Datei werden
   waehrend der Umsetzung fortgeschrieben.

## Betroffene Dateien
- `panel/holetemplates.py`
- `lasercut/holetemplate.py` (nur falls eine kleine, testbare Aufloesehilfe
  gebraucht wird)
- `test/test_holetemplate.py`
- `test/test_holetemplate_freecad.py`
- `README.md`
- `docs/hole_templates.md`
- `ai/plans/hole-template-tree-management.memory.md`
- `ai/plans/hole-template-tree-management.README.md`

## Annahmen und offene Punkte
- Bestehende, bereits erzeugte lose `HoleTemplates`-Gruppen werden nicht
  automatisch migriert; sie bleiben unveraendert im Dokument.
- Die Liste der Quellobjekte bleibt als Namen gespeichert, weil direkte Links
  aus einem Ergebniscontainer in eine Assembly Scope-Warnungen ausloesen.
- Das neue `HoleTemplate`-Objekt selbst wird auf der bestehenden
  `feature/connection-hole-templates`-Branch weiterentwickelt; es wird kein
  zweiter paralleler Feature-Branch angelegt.