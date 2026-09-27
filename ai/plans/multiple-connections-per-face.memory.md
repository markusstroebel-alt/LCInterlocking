# Fortschritt: Mehrere Verbindungen pro Face

- Umsetzung am Branch `feature/multiple-connections-per-face` begonnen, nachdem der Nutzer
  den Plan freigegeben hat.
- Ursache bestaetigt: `tab_name` entspricht derzeit `Objektname.Facename` und dient
  zugleich als Face-Bezeichner, Speicher-ID, Baum-ID und Link-Ziel. Das blockiert jeden
  zweiten Verbindungseintrag auf derselben CAD-Flaeche.
- Ziel: eine separate `connection_id` einfuehren, damit zum Beispiel TongueGroove und
  Screw auf `Wall.Face1` unabhaengig bearbeitet, entfernt und berechnet werden koennen.
- Keine Rueckwaertskompatibilitaet oder Migration alter gespeicherter MultiJoins
  erforderlich; das Tool ist noch nicht produktiv im Einsatz.
- Erledigt: `connection_id` ist persistierbar und zugleich die interne `tab_name`-ID.
  `TabsList`, Baum, Link-Aufloesung, Entfernen und Kontaktflaechen-Erkennung verwenden
  dadurch eindeutige Verbindungseintraege statt CAD-Faces als Identitaet.
- Erledigt: Mehrfach gleiche Typen erhalten im Baum einen sichtbaren Suffix wie
  `Face1 (Screw #2)`; Typwechsel aktualisieren das Label.
- Geprueft: isolierter Python-Test fuer zwei unabhaengige Typen auf einer Face, zwei
  gleiche Typen, Link-ID und Labels; AST-Parse und `git diff --check` bestanden.
- Geprueft: Das Entfernen einer Screw-Verbindung laesst TongueGroove und eine zweite
  Screw-Verbindung auf derselben Face unveraendert bestehen. Die vier geaenderten
  Python-Dateien haben keine Editor-Diagnosen.
- Offen: finaler FreeCAD-Manuelltest mit TongueGroove plus Screw auf derselben Face.