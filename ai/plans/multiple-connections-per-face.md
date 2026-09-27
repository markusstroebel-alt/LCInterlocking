# Plan: Mehrere Verbindungen pro Face

## Ziel
Eine CAD-Flaeche soll mehrere unabhaengige Interlocking-Verbindungen tragen koennen.
Beispiel: Auf `Wall.Face1` wird gleichzeitig eine `TongueGroove`-Nut und eine
`Screw`-Verbindung konfiguriert. Beide Geometrien sollen bei Preview und finalem
MultiJoin in derselben Berechnung akkumulieren.

## Ursache
`TabProperties.tab_name` wird derzeit als `Objektname.Facename` erzeugt, zum Beispiel
`Wall.Face1`. Dieselbe Zeichenkette ist zugleich die eindeutige Identitaet in
`TabsList`, der Tree-Ansicht und beim Entfernen beziehungsweise Verknuepfen von
`Add same faces`. Deshalb wird ein zweiter Eintrag auf derselben CAD-Flaeche mit
"already present" abgewiesen.

## Bedienmodell
- **Add faces** darf eine bereits konfigurierte Face erneut aufnehmen. Der aktuell im
  Task-Panel gewaehlte Verbindungstyp gilt fuer den neuen, unabhaengigen Eintrag.
- Im Baum erscheinen mehrere Verbindungen derselben Face getrennt und eindeutig, etwa
  `Face1 (TongueGroove)` und `Face1 (Screw)`. Die interne ID bleibt unsichtbar.
- **Add same faces** verknuepft weiterhin mehrere Faces mit einem Master-Eintrag.
  Die Verknuepfung verweist auf dessen eindeutige Verbindungs-ID, nicht nur auf den
  Namen der CAD-Flaeche.
- Die automatische Kontaktflaechen-Erkennung darf bereits verwendete Faces erneut
  anbieten. Sie erzeugt einen zusaetzlichen Eintrag mit dem aktuell gewaehlten Typ.

## Vorgehen
1. `lasercut/tabproperties.py`: Eine persistierbare `connection_id` als stabile,
   eindeutige Identitaet jeder Face-Verbindung einfuehren. `face_name` bleibt der
   echte FreeCAD-Subelementname. Es ist keine Migration alter gespeicherter Eintraege
   erforderlich.
2. `panel/tab.py`: `TabsList` auf `connection_id` umstellen:
   - Anlegen mehrerer Eintraege auf derselben Face erlauben,
   - Master-/Link-Aufloesung und Entfernen ueber die ID vornehmen,
   - Link-Eintraege auf die ID des Master-Eintrags beziehen,
   - sichtbare Beschreibungen aus Face und Typ bilden.
3. `panel/treeview.py` und `panel/treepanel.py`: Baumknoten mit `connection_id`
   identifizieren, aber als Label `Face (ConnectionType)` darstellen. Die bisherige
   Face-Duplikatpruefung entfernen beziehungsweise auf die interne ID beschraenken.
4. `panel/contactfaces.py` und `panel/treepanel.py`: Kontaktkandidaten nicht mehr
   wegen einer vorhandenen Verbindung derselben Face ausfiltern. Jede bestaetigte
   Auswahl erzeugt eine neue Verbindung.
5. `lasercut/join.py`: Sicherstellen, dass mehrere TabProperties auf derselben Face
   weiterhin einzeln verarbeitet werden und ihre `toAdd`-/`toRemove`-Geometrien
   gemeinsam im Ergebnis landen. Diagnoseausgaben nennen neben Face und Typ auch die
   Verbindungs-ID.
6. Isolierte Tests erstellen fuer:
   - zwei Typen auf derselben Face,
   - Master plus `Add same faces` mit eindeutiger Link-ID,
   - Entfernen nur einer von zwei Verbindungen auf derselben Face.
7. In FreeCAD manuell pruefen: `TongueGroove` und `Screw` auf einer Face, Preview,
   finalen MultiJoin, Bearbeiten und Entfernen eines einzelnen Eintrags sowie
   automatische Kontaktflaechen-Erkennung mit derselben Face.
8. README und Interlocking-Dokumentation aktualisieren.

## Betroffene Dateien
- `lasercut/tabproperties.py`
- `lasercut/join.py`
- `panel/tab.py`
- `panel/treepanel.py`
- `panel/treeview.py`
- `README.md`
- `docs/interlocking.md`
- `ai/plans/multiple-connections-per-face.memory.md`
- `ai/plans/multiple-connections-per-face.README.md`

## Annahmen und offene Fragen
- Mehrere Verbindungen auf derselben Face werden bewusst gemeinsam boolean-verarbeitet.
  Ueberlappende Geometrien werden nicht als Fehler unterdrueckt; Preview und finale
  Berechnung bleiben die sichtbare Kontrolle.
- `connection_id` darf fuer die Dauer des MultiJoin stabil sein, muss aber keine
  dokumentuebergreifend global eindeutige UUID sein. Ein deterministischer Suffix pro
  Face reicht aus und bleibt fuer serialisierte Daten lesbar.
- Es ist keine Rueckwaertskompatibilitaet fuer bereits gespeicherte MultiJoins
  erforderlich, weil das Tool noch nicht produktiv eingesetzt wird.