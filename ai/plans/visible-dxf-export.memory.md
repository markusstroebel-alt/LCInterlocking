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
- DXF-Layer fuer Estlcam: `KONTUR`, `DURCHBRUCH`, `TASCHE`, `TEXT`.

## Naechste Schritte
- Bestehenden Exportcode in eine wiederverwendbare DXF-Pipeline zerlegen.
- Sichtbare Exportkandidaten und Fertigungsseiten mit Taschen analysieren.
- DXF-Ansichten, Texte und Layer erzeugen und im echten FreeCAD testen.