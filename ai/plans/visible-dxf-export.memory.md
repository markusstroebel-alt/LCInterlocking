# Umsetzung: Sichtbarer DXF-Export

## Status
- Plan freigegeben.
- Branch `feature/visible-dxf-export` erstellt.
- Bestehende uncommittete Arbeiten werden nicht veraendert.

## Anforderungen
- Exportiert ausschliesslich im FreeCAD-Modellbaum sichtbare Bauteile.
- Eine DXF je Bauteil, mit allen erforderlichen beschrifteten Fräsansichten.
- Jede Ansicht kombiniert Kontur, Durchbrueche und Taschen der jeweiligen
  Spannlage.
- DXF-Layer fuer Estlcam: `KONTUR`, `DURCHBRUCH`, `TEXT` und ein
  `TASCHE_<TIEFE>MM`-Layer je Taschentiefe.

## Umgesetzt
- Die Taschenanalyse erkennt parallele Taschenboeden pro Frässeite und schliesst
  Durchbrueche aus. Eine reale Testplatte mit Taschen von 2 mm und 3 mm auf
  Gegenflaechen wird korrekt erkannt.
- Die Einzelbauteil-Pipeline erzeugt 2D-Geometrie auf `KONTUR`, `DURCHBRUCH`
  und tiefenspezifischen Taschenlayern.
- Der moderne FreeCAD-DXF-Exporter verwendet den internen Namen eines
  `Part::Feature` als DXF-Layer. Deshalb wird pro Layer ein kombiniertes
  Feature erstellt.
- Beschriftungen werden als `Draft.make_shapestring`-Konturgeometrie auf dem
  Layer `TEXT` exportiert. Das funktioniert ohne die nicht installierten
  Legacy-DXF-Libraries.
- Der echte FreeCAD-Test bestaetigt die Layer `KONTUR`, `TASCHE_2_00MM`,
  `TASCHE_3_00MM` und `TEXT` in einer erzeugten DXF.
- `Export visible DXF` ist als eigener Command in der Export-Toolbar
  registriert. Er fragt einen Zielordner ab, exportiert alle im Modellbaum
  sichtbaren Blattobjekte und meldet einzelne Fehler gesammelt.
- Mehrfach vorkommende Labels erhalten kollisionsfreie Dateinamen wie
  `bauteil.dxf` und `bauteil_2.dxf`; ausgeblendete Objekte werden ausgelassen.

## Validierung
- Der echte FreeCAD-Test prueft zweiseitige Taschen, Durchbrueche,
  tiefenspezifische Layer, ShapeString-Text, Modellbaum-Sichtbarkeit,
  Dateinamenskollisionen und Command-Aktivierung.
- Manueller GUI-Check bleibt sinnvoll: sichtbare und ausgeblendete Teile mit
  `Export visible DXF` in Estlcam importieren und die Layer zuordnen.