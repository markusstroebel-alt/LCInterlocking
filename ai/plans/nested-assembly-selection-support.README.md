# Sichere Auswahl in verschachtelten Assemblys

Die Erweiterung sorgt dafuer, dass alle auswahlbasierten Werkzeuge dieselbe
konkrete Komponente einer verschachtelten Assembly verwenden. Dazu gehoeren
MultiJoin, Crosspiece, Living Hinge, Hole templates und Export.

Eine direkt ausgewaehlte Linkinstanz bleibt immer erhalten. Bei einer Auswahl
innerhalb einer Subassembly wird der gesamte Auswahlpfad ausgewertet, damit die
Placement-Position der sichtbaren Instanz verwendet wird. Mehrdeutige Quellen
werden nicht stillschweigend einer beliebigen Instanz zugeordnet.

Die Regel gilt fuer MultiJoin, Crosspiece, Living Hinge, Hole templates und
Export. Bei mehreren Instanzen desselben Body oder Pad muss immer die sichtbare
Komponente im aussenliegenden Assembly ausgewaehlt werden.