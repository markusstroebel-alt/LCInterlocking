# Verwaltete Lochschablonen im Baum

Jede bestaetigte Lochschablonen-Operation wird als ein `HoleTemplate`-Eintrag
im FreeCAD-Baum gespeichert. Darunter erscheinen nur die erzeugten
Zielteil-Kopien. Die verbundenen Schrauben, Beschlaege und Ausschnittvolumina
werden nicht als einzelne Baumobjekte angelegt.

Mit **Edit** im Kontextmenue kann die Rollenwahl erneut geoeffnet werden. Die
bereits zugeordneten Template- und Zielkoerper werden vorbefuellt; beim
Bestaetigen aktualisiert die Operation ihre vorhandenen Ergebnisse statt neue
Gruppen anzulegen.

Die urspruenglichen Zielkoerper bleiben im Dokument erhalten, werden nach der
Berechnung aber ausgeblendet. Template-Koerper, etwa Schrauben oder Beschlaege,
bleiben sichtbar.