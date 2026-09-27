# Fortschritt: Kontaktflaechen erkennen und Verbindungstyp aendern

- Plan erstellt, noch nicht zur Umsetzung freigegeben.
- Der Erkennungsbereich soll die aktuell im geoeffneten MultiJoin eingetragenen Parts
  umfassen.
- Verbindungstypen sind heute beim Hinzufuegen einer Face festgelegt. Master-Faces
  muessen den Typ nachtraeglich wechseln koennen; verknuepfte `same Faces` bleiben
  an ihrem Master ausgerichtet.
- Freigabe erteilt. Die Kontakt-Toleranz wird als globale LCInterlocking-Einstellung
  mit einem Default von `0.01 mm` umgesetzt.
- Globale Einstellung, editierbarer Typ fuer Master-Faces und ein Kontaktflaechen-
  Dialog sind umgesetzt. Die Erkennung analysiert nur die Parts des offenen MultiJoin
  und laesst pro Kontaktpaar die Richtung der Verbindung waehlen.
- Die isolierten Simulationen fuer Preferences-Persistenz, Typwechsel und die Erkennung
  eines planaren Gegenflaechenpaars sind erfolgreich. Syntax, Whitespace und
  Editor-Diagnosen sind ebenfalls erfolgreich.
- Offener manueller Test in FreeCAD: Kontaktpaar erkennen, die Tab-Richtung waehlen,
  den Typ auf ScrewInNut wechseln, Vorschau pruefen und die globale Toleranz aendern.