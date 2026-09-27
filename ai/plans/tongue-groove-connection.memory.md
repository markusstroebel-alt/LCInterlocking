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
- Offener manueller FreeCAD-Test: volle Hoehe, halbe Hoehe zentriert, Side A, Side B und
  einen Assembly-Gegenpart mit Preview und finalem MultiJoin pruefen.