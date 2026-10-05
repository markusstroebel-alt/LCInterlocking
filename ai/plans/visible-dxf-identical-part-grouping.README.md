# Identische Bauteile im sichtbaren DXF-Export

Der Command **Export visible DXF** erkennt gleiche sichtbare Fertigungsteile
und erzeugt dafuer nur eine DXF-Datei. Die Beschriftung im `TEXT`-Layer zeigt
die benoetigte Stueckzahl als `MENGE <Anzahl>`.

Gleichheit bezieht sich auf die fertige Fräsgeometrie, nicht auf die Position,
Orientierung, den Baum-Namen oder das Quellobjekt. Unterschiedliche Konturen,
Durchbrueche oder Taschen bleiben getrennte DXF-Dateien.

Die Menge wird in der Konturansicht im DXF-`TEXT`-Layer ausgegeben.