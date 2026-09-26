# Assembly-MultiJoin-Verkettung

## Zweck
Bewahrt Assembly-Komponenten beim Erzeugen eines MultiJoin und ermoeglicht weitere
Interlocking-Verbindungen zwischen bereits erzeugten Teilen und weiteren Assembly-Komponenten.

## Erwarteter Ablauf
Ein erstes MultiJoin bearbeitet beispielsweise `Base` und `Wall`. `Base` bleibt dabei im Assembly.
Danach kann das erzeugte `Base_tab` mit einer weiteren Assembly-Komponente wie `Wall001` in einem
zweiten MultiJoin verbunden werden.

## Diagnose
Die FreeCAD-Konsole zeigt Meldungen mit dem Praefix `[LCInterlocking]`. Diese nennen die
aufgeloeste Assembly-Komponente und ob ein Link im Assembly behalten oder ein normales Teil in
die Ursprungsgruppe verschoben wurde.