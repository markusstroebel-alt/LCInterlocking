# Sichtbarer DXF-Export

Der neue Export erstellt fuer jedes im FreeCAD-Modellbaum sichtbare Bauteil eine
DXF-Datei. Die Datei enthaelt alle benoetigten Fräsansichten des Bauteils
nebeneinander.

Jede Ansicht zeigt die Aussenkontur, Durchbrueche und Taschen der entsprechenden
Spannlage. Beschriftungen enthalten Bauteilname, Bearbeitungsseite,
Materialstaerke und Taschentiefen. Die DXF-Layer `KONTUR`, `DURCHBRUCH`,
`TASCHE` und `TEXT` sind fuer die direkte Zuordnung in Estlcam vorgesehen.

Ausgeblendete Objekte werden nicht exportiert. Die aktuelle 3D-Auswahl hat
keinen Einfluss auf den Export.

Der Command **Export visible DXF** befindet sich in der Export-Toolbar. Nach
der Wahl eines Zielordners erzeugt er eine DXF-Datei je sichtbarem Bauteil.
Gleiche Bauteilnamen werden automatisch nummeriert.