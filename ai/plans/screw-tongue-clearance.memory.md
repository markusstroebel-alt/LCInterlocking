# Fortschritt: Schraubenfreiraum in TongueGroove

- Ursache bestaetigt: `MaterialElement` schneidet `toRemove` nur aus dem
  zugehoerigen Part. Screw-Freiraeume im Gegenpart schneiden daher nicht in die
  TongueGroove-Feder des Quellparts.
- Nutzer hat die Prioritaetsregel freigegeben: Schraubenfreiraum schneidet die
  ueberlappende Feder aus.
- Branch `feature/screw-tongue-clearance` angelegt.
- Erledigt: `JoinContext` sammelt Screw-Slots und die Schraubenbohrung fuer den
  Gegenpart. Nach der gesamten Verbindungsberechnung erhalten nur passende
  TongueGroove-Quellparts diese Volumen als `toRemove`.
- Geprueft: isolierter Kontexttest fuer drei Screw-Freiraeume auf gleicher Face
  und gleichem Gegenpart; abweichende Face und abweichender Gegenpart bleiben
  unveraendert. AST-Parse und `git diff --check` bestanden.
- Offen: Editor-Diagnosen, finaler FreeCAD-Manuelltest und Commit.