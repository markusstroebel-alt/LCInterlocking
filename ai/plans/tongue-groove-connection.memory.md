# Fortschritt: Durchgehende Feder-und-Nut-Verbindung

- Plan erstellt, noch nicht zur Umsetzung freigegeben.
- Gewuenschter Anwendungsfall: Schubladenboden mit einer durchgehenden, nur teilweise
  materialhohen Feder und einer beispielsweise `10 mm` tiefen Nut im Gegenpart.
- Die ausgewaehlte Master-Face erzeugt die Feder; der tatsaechlich geschnittene
  Gegenpart erhaelt die Nut.
- Seitenlage der Teilhoehe wird als `Center`, `Side A` oder `Side B` ueber die lokale
  Dickenachse der Face modelliert und im Preview kontrolliert.
- Umsetzung gestartet: `TongueGroove` ist als persistierbarer Verbindungstyp mit globalen
  Defaults, Preset-Unterstuetzung und einem eigenen Widget vorhanden.
- Die Geometrie erzeugt eine einzelne, vollbreite Feder und eine Nut mit Bodenfreiraum.
  Der Gegenpart wird mit der bestehenden Intersectionslogik bestimmt.
- Isolierte Tests fuer globale Defaults, Umwandlung eines alten Tab-Faces, die drei
  Hoehenlagen und den Fall `6 mm` Material / `3 mm` Side A / `10 mm` Tiefe sind erfolgreich.
- Nachbesserung fuer unterschiedlich lange Faces: Feder und Nut werden nun auf ihr tatsaechliches
  Schnittvolumen mit dem Gegenpart begrenzt. Eine laengere Master-Face erzeugt damit nur im
  Bereich der kuerzeren Nutseite Geometrie. Die isolierte Ueberlappungs-Simulation ist erfolgreich.
- Nachbesserung fuer Slot-width-Tolerance: Die Nut erhaelt die Toleranz jetzt symmetrisch in
  Face-Breite und Materialhoehe. Der Mass-Test bestaetigt bei `80 x 3 mm` Feder und `0.2 mm`
  Toleranz eine zentrierte `80.2 x 3.2 mm` Nut.
- Korrektur fuer Side A und Side B: Die Feder wird nicht verschoben. Die Slot-width-Tolerance
  erweitert ausschliesslich den Nutkoerper um seine Nennkontur. Bei `0.2 mm` Toleranz wird die
  Nut auf jeder Seite um `0.1 mm` erweitert; die Feder bleibt buendig auf der gewaehlten Seite.
  Die isolierte Simulation ist erfolgreich.
- Log-Auswertung bei zwei Faces: `Wall.Face4` verbindet sich mit `Wall002`; `Wall.Face1` prueft
  `Wall002` und `Base`, findet aber in der positiven Face-Normalenrichtung keine Ueberlappung.
  Nachbesserung: TongueGroove prueft nun zuerst die bisherige Richtung und bei fehlender
  Ueberlappung die Gegenrichtung. Die erste passende Richtung gilt sowohl fuer Feder als auch
  Nut. Die isolierte Rueckwaertsrichtungs-Simulation ist erfolgreich.
- Offener manueller FreeCAD-Test: volle Hoehe, halbe Hoehe zentriert, Side A, Side B und
  einen Assembly-Gegenpart mit Preview und finalem MultiJoin pruefen; dabei auch eine laengere
  Master-Face als die Nutseite testen.