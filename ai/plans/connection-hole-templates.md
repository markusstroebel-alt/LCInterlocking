# Plan: Lochschablonen fuer Assembly-Verbindungen

## Ziel
Ein neues Workbench-Werkzeug erzeugt aus ausgewählten Verbindungs- oder
Beschlagkörpern (zum Beispiel Schrauben, Bolzen, Scharnieren oder Auszügen)
Bohr- beziehungsweise Ausfrässchablonen. Die Schablonengeometrie wird von den
ausgewählten Zielteilen abgezogen; die Originalkörper bleiben unverändert.
Das Werkzeug arbeitet sowohl mit normalen `Part::Feature`-Objekten als auch
mit Komponenten aus der FreeCAD-Assembly-Workbench (`App::Link`).

## Geplantes Verhalten
1. Der Nutzer markiert alle beteiligten Körper und startet den neuen Befehl
   **Lochschablonen** in der LCInterlocking-Workbench.
2. Ein Task-Panel übernimmt die Auswahl und zeigt zwei explizite Listen:
   **Schablonenkörper** (Schraube, Beschlag oder sonstiges Werkzeugvolumen)
   und **Zielkörper** (Teile, die die Ausschnitte erhalten). Ein ausgewählter
   Körper kann nicht zugleich in beiden Listen stehen.
3. Für jedes Ziel wird nur der geometrische Schnitt mit der Vereinigung der
   Schablonenkörper abgezogen. Nicht schneidende Körper erzeugen keinen
   Ausschnitt. Dadurch entstehen für Schrauben echte Durchgangslöcher und bei
   Scharnieren oder Auszügen die jeweils überdeckten Taschen.
4. Das Ergebnis wird als neuer `Part::Feature`-Körper je Zielteil erzeugt,
   inklusive nachvollziehbarer Namen und Links auf Quelle, Ziel und
   Schablonenkörper. Ursprungsobjekte werden nicht verändert oder verschoben.
5. Bei ungültiger Auswahl, leerer Schnittmenge oder fehlender Form erscheint
   eine konkrete Meldung. Für Assembly-Links wird die bestehende Auswahl-
   auflösung genutzt, damit das Ergebnis am aktuell platzierten Link entsteht.

## Vorgehen
1. Einen kleinen Geometriekern ergänzen, der gültige Formkörper prüft, die
   Schablonengeometrie vereinigt, sie mit jedem Ziel schneidet und das Resultat
   als Differenz berechnet. Die Logik bleibt unabhängig von Qt testbar.
2. Einen neuen Befehl mit Task-Panel anlegen. Das Panel übernimmt die aktuelle
   Mehrfachauswahl, erlaubt die Rollenwahl, zeigt eine Vorschau der erzeugten
   Resultate und führt die Berechnung erst nach Bestätigung aus.
3. Die bestehende Auswahlhilfe für Assembly-Komponenten erweitern oder direkt
   wiederverwenden, sodass `App::Link`-Instanzen samt ihrer Placement-Formen
   korrekt verwendet werden.
4. Ergebnisobjekte in einer eigenen Dokumentgruppe ablegen. Ihre Eigenschaften
   dokumentieren die Quell-, Ziel- und Schablonenobjekte, damit die Herkunft
   im Baum nachvollziehbar bleibt und eine spätere Aktualisierung möglich ist.
5. Den Befehl samt Icon in der Workbench registrieren und die Nutzung im
   README sowie in einer eigenen Dokumentationsseite beschreiben.
6. Tests für den Geometriekern ergänzen: Schraube durch zwei Platten, mehrere
   Schablonenkörper, nicht schneidende Objekte, ungültige Rollenwahl und ein
   Assembly-Link mit Placement. Danach Syntax- und Editor-Prüfungen ausführen.
7. Manuell in FreeCAD prüfen: Zwei Assembly-Teile mit einer Schraube, einem
   Scharnier und einem Auszug markieren, Rollen setzen und kontrollieren, dass
   nur die Zielteile neue Ausschnitte erhalten und alle Originale bestehen
   bleiben.

## Voraussichtlich betroffene Dateien
- `InitGui.py`
- neues Modul unter `lasercut/` fuer die Differenz- und Ergebnislogik
- neues Panel unter `panel/` fuer Auswahl, Rollen und Vorschau
- `panel/selection.py`
- `README.md`
- neue Dokumentationsseite unter `docs/`
- neue Tests unter `test/` oder dem vorhandenen Testmuster
- nach Freigabe: `ai/plans/connection-hole-templates.memory.md`
- nach Freigabe: `ai/plans/connection-hole-templates.README.md`

## Offene Fragen und Annahmen
- Die Begriffe *Schablonenkörper* und *Zielkörper* werden im Dialog bewusst
  explizit getrennt. Eine automatisch ungerichtete Differenz aller markierten
  Körper könnte bestehende Steckverbindungen oder absichtliche Überlappungen
  zerstören.
- Eine erste Version bildet die exakte Überlappungsgeometrie ab. Zusätzliche
  Spielwerte fuer Bohrungen oder Taschen bleiben ein möglicher Folgeschritt.
- Scharniere und Auszüge werden als ihre tatsächlichen Körpervolumina
  verarbeitet. Sollen bei diesen Beschlägen ausschliesslich ihre
  Befestigungsbohrungen statt ihrer gesamten Kontur verwendet werden, braucht
  es dafür eine eigene Erkennung oder ein separates Eingabemodell.
- Die Ergebnisobjekte sind zunächst bewusst erzeugte Kopien. Eine
  parametriche Live-Aktualisierung bei Änderungen der Assembly ist erst dann
  sinnvoll, wenn die stabile Objektverknüpfung in der Praxis verifiziert ist.