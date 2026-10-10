# Plan: Ausgewaehlte Bodies zu Lochschablonen hinzufuegen

## Ziel
Der Dialog **Hole templates** soll beim ersten Start und beim spaeteren
**Edit** aktuelle FreeCAD-Auswahlen aufnehmen koennen. So lassen sich weitere
Schrauben, Beschlaege oder Zielkoerper zu einer bestehenden `HoleTemplate`-
Operation hinzufuegen, ohne sie neu anzulegen.

## Geplantes Verhalten
1. Der Dialog erhaelt eine Schaltflaeche **Add selected bodies** oberhalb der
   Liste **Selected bodies**.
2. Sie liest die aktuelle 3D-Auswahl ueber `panel.selection` ein, loest
   Assembly-Komponenten wie der Startbefehl auf und fuegt nur neue Objekte zur
   verfuegbaren Liste hinzu.
3. Bereits als Template oder Ziel zugeordnete Bodies werden nicht dupliziert.
   Die Schaltflaeche meldet klar, wenn keine neuen Bodies ausgewaehlt sind.
4. Im Edit-Modus kann der Nutzer Bodies vor dem Klick im 3D-Fenster markieren,
   **Add selected bodies** druecken und sie anschliessend als Template oder
   Ziel zuordnen. Beim Bestaetigen wird die vorhandene Operation mit den neuen
   Rollen neu berechnet und ihre bestehenden Ergebnisobjekte weiterverwendet.
5. Bei der erstmaligen Erstellung bleibt die bereits beim Befehlstart
   uebernommene Auswahl bestehen; der Button ermoeglicht lediglich weitere
   Bodies nach dem Oeffnen des Dialogs.

## Vorgehen
1. In `HoleTemplatePanel` eine Hilfsfunktion fuer alle bereits gelisteten
   Namen einfuehren und mit ihr doppelte Eintraege verhindern.
2. Den Button mit einer Assembly-sicheren Abfrage von
   `selection.get_freecad_objects_list()` verbinden. Neue Objekte werden in
   `objects_by_name` registriert und der verfuegbaren Liste hinzugefuegt.
3. Bei leerer Auswahl oder wenn alle ausgewaehlten Objekte bereits gelistet
   sind, eine kurze Status- beziehungsweise Warnmeldung ausgeben.
4. Einen testbaren Helfer oder einen FreeCAD-AppImage-Test ergaenzen, der
   prueft, dass neue Bodies aufgenommen und bestehende nicht verdoppelt werden.
5. README, `docs/hole_templates.md` und die begleitenden Memory-/README-Dateien
   auf den erweiterten Edit-Workflow aktualisieren. Syntax-, Unit-,
   Whitespace- und FreeCAD-Tests ausfuehren.

## Betroffene Dateien
- `panel/holetemplates.py`
- `test/test_holetemplate_freecad.py`
- `README.md`
- `docs/hole_templates.md`
- `ai/plans/hole-template-add-selected-bodies.memory.md`
- `ai/plans/hole-template-add-selected-bodies.README.md`

## Annahmen
- Die aktuelle Auswahl wird erst beim Klick auf **Add selected bodies**
  gelesen. Dadurch kann der Dialog offen bleiben, waehrend der Nutzer im
  3D-Fenster weitere Komponenten auswaehlt.
- Der Button fuegt neue Bodies zunaechst neutral zu **Selected bodies** hinzu;
  ihre Rolle wird weiterhin bewusst durch **Set as template** oder
  **Set as target** festgelegt.