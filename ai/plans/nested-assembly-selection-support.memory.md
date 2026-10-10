# Umsetzung: Sichere Auswahl in verschachtelten Assemblys

## Status
- Plan freigegeben.
- Branch `feature/nested-assembly-selection-support` erstellt.
- Vorhandene, uncommittete Lochschablonen-Aenderungen wurden unveraendert in
  den neuen Branch uebernommen.

## Entscheidungen
- Die Auswahlaufloesung wird zentral in `panel.selection` umgesetzt.
- Direkte `App::Link`-Instanzen haben immer Vorrang.
- Verschachtelte Pfade muessen die verwendete Instanz und ihre zusammengesetzte
  Placement-Transformation eindeutig liefern; bei Mehrdeutigkeit wird nicht
  geraten.

## Validierung
- Die drei fokussierten Kern-Unit-Tests bestehen.
- Alle auswahlbetroffenen Python-Module kompilieren ohne Fehler.
- `git diff --check` ist sauber.
- Der echte FreeCAD-1.1.3-AppImage-Test besteht mit verschachtelter
  Pfadauflösung, persistenter Wiederauflösung, Tree-Face-Pfad,
  HoleTemplate-Differenz und Export-Shape.
- Die gespeicherte Reproduktion `Assembly4.FCStd` bestaetigt die Aufloesung
  einer direkt ausgewaehlten Unterkomponente: `Base001` wird als
  `Assembly001__LCI_PATH__Base001.` mit ihrer Parent-Link-Placement aufgeloest
  und erzeugt den erwarteten HoleTemplate-Boolean-Abtrag.
- Der Recompute der ungespeicherten `Assembly4`-Kopie migriert den alten
  Targetnamen `Base001` auf den Parent-Link-Pfad und erzeugt danach drei
  Ergebnisse einschliesslich der Base.
- Manueller GUI-Check bleibt fuer MultiJoin, Crosspiece, Living Hinge,
  Hole templates und Export mit einem realen verschachtelten Assembly-Dokument
  empfohlen.

## Umgesetzt
- `panel.selection` erzeugt fuer verschachtelte Subelementpfade eine stabile
  Referenz aus Rootobjekt und Pfad. Die Referenz loest die von
  `getSubObject()` gelieferte, effektiv platzierte Shape erneut auf.
- Direkte Auswahlen eines Kindes in einer verlinkten Assembly erkennen nun
  ebenfalls den Parent-Link und speichern dessen Subpfad, auch wenn FreeCAD
  keinen vollstaendigen Auswahlpfad mitliefert.
- Alte direkte Referenzen werden beim Aufloesen sowie beim HoleTemplate-
  Recompute auf den kanonischen Parent-Link-Pfad migriert.
- Wenn FreeCAD keine Element-Sichtbarkeit fuer einen Parent-Link unterstuetzt,
  loest HoleTemplate dessen konkretes Kindobjekt auf und blendet nur dieses
  aus; die restliche verschachtelte Assembly bleibt sichtbar.
- MultiJoin, Crosspiece, TreePanel, Living Hinge, Hole templates und Export
  verwenden diese Referenzen fuer Recompute, Vorschau und Baumselektion.
- Crosspiece behandelt Assembly- und Nested-Quellen wie MultiJoin: Sie werden
  nicht in Ursprungsgruppen verschoben oder dort verlinkt.
- Der echte FreeCAD-Test prueft verschachtelte Pfadauflösung, Persistenz,
  Baumselektionspfad, Boolean-Differenz, HoleTemplate-Recompute und Export.