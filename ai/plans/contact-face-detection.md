# Plan: Kontaktflaechen erkennen und Verbindungstyp aendern

## Ziel
Ein geoeffneter MultiJoin soll aus seinen aktuell eingetragenen Parts moegliche
Kontaktflaechen erkennen. Der Anwender waehlt aus den vorgeschlagenen Paaren aus,
welche als Verbindungen angelegt werden. Bereits konfigurierte Master-Faces sollen
ihren Verbindungstyp nachtraeglich von `Tab` zu `Screw`, `WoodScrew`, `ScrewInNut`
oder `Continuous` wechseln koennen.

## Umfang
- Die Analyse umfasst ausschliesslich `self.parts` des aktuell geoeffneten MultiJoin,
  nicht alle Objekte des Dokuments oder der Assembly.
- Die Kontakt-Toleranz ist eine globale LCInterlocking-Einstellung und wird sowohl
   fuer neue Erkennungen als auch im Treffer-Dialog verwendet.
- Sie betrachtet planare Flaechen verschiedener Parts und findet Gegenflaechen mit
  gegenlaeufigen Normalen, passendem Abstand innerhalb einer Toleranz und einer
  ueberlappenden Flaeche.
- Treffer werden zuerst in einer Auswahl angezeigt. Es werden keine Verbindungen
  ohne explizite Auswahl angelegt.
- Der Typwechsel ist nur an einer Master-Face moeglich. Mit `Add same faces`
  verknuepfte Faces uebernehmen weiterhin die Konfiguration ihres Masters.

## Vorgehen
1. `panel/tab.py`: Eine zentrale Liste der unterstuetzten Verbindungstypen und eine
   Umstellungsmethode fuer Master-`TabProperties` einfuehren. Gemeinsame Werte wie
   Anzahl, Breite, Verschiebung, Laenge und Dog-Bone bleiben erhalten; nur
   typ-spezifische Werte werden aus den vorhandenen Defaults initialisiert. Label und
   Beschreibung werden mit dem neuen Typ aktualisiert.
2. `panel/treepanel.py`: Im Eigenschaftenbereich einer Master-Face eine
   `Connection type`-Auswahl anbieten. Nach einer Aenderung muss das passende
   Eingabe-Widget ohne Verlust der gemeinsamen Werte erneut aufgebaut werden.
3. `lasercut/preferences.py` und `panel/preferencespage.py`: Einen persistenten
   globalen Default fuer die Kontakt-Toleranz anbieten.
4. `panel/contactfaces.py` (neu): Geometriehelfer fuer planare Face-Kandidaten
   erstellen. Kandidaten enthalten beide Objekte, Face-Namen und ausreichend
   Informationen fuer die vorhandene Face-Konfiguration. Die globale Toleranz wird
   fuer Ebenenabstand und Flaechenueberlappung angewendet.
5. `panel/treepanel.py`: Schaltflaeche fuer die Analyse der aktuell eingetragenen
   Parts und einen Auswahl-Dialog fuer Kandidaten ergaenzen. Ausgewaehlte Paare
   werden mit einer vom Anwender gewaehlten Richtung als normale Master-Faces in die
   vorhandene Face-Liste uebernommen. Pro Kontaktpaar darf nur eine der beiden
   Flaechen die Verbindung erzeugen, damit Tabs und Aussparungen nicht doppelt
   angelegt werden.
6. Den vorhandenen Assembly-Auswahlpfad verwenden, damit Instanzen weiterhin mit
   ihrem `App::Link` und nicht versehentlich mit dem externen Quell-Body angelegt
   werden.
7. Unit-nahe Tests bzw. isolierte FreeCAD-Attrappen fuer Typwechsel und
   Kontakt-Kandidatenerkennung ergaenzen; danach Syntax-, Whitespace- und
   Editor-Diagnosepruefungen ausfuehren. Manuell in FreeCAD pruefen: zwei, drei und
   keine Kontaktflaechen sowie Assembly-Instanzen.
8. README und Interlocking-Dokumentation mit Bedienablauf und Grenzen der
   Erkennung aktualisieren.

## Betroffene Dateien
- `panel/tab.py`
- `panel/treepanel.py`
- `panel/contactfaces.py` (neu)
- `lasercut/tabproperties.py`
- `lasercut/preferences.py`
- `panel/preferencespage.py`
- `README.md`
- `docs/interlocking.md`
- `ai/plans/contact-face-detection.memory.md`
- `ai/plans/contact-face-detection.README.md`

## Annahmen und offene Fragen
- Fuer den ersten Schritt werden nur planare, sich gegenueberliegende Flaechen
  vorgeschlagen; Kanten-, Punktkontakte und gekruemmte Flaechen bleiben ausgeschlossen.
- Die geometrische Kontakt-Toleranz erhaelt einen globalen Default von `0.01 mm`
   und ist auf der LCInterlocking-Preferences-Seite editierbar.
- Bei einem Kandidatenpaar waehlt der Anwender, welche der beiden Flaechen als
   Master-Face eingetragen wird. Die andere Flaeche dient nur zur Identifikation des
   Kontakts, weil die bestehende Join-Geometrie den Gegenpart selbst berechnet.
- Ein Wechsel des Verbindungstyps soll keine bereits berechnete MultiJoin-Kette
  automatisch aktualisieren; nachgelagerte MultiJoins muessen wie bisher einzeln
  bestaetigt werden.