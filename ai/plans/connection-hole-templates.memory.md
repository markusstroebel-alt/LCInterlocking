# Umsetzung: Lochschablonen fuer Assembly-Verbindungen

## Status
- Plan freigegeben.
- Branch `feature/connection-hole-templates` erstellt.
- Der Arbeitsbaum enthielt vor Branch-Erstellung nur den neuen Plan als
  unversionierte Datei.

## Entscheidungen
- Schablonen- und Zielkoerper erhalten im Dialog getrennte Rollen.
- Die erste Version erzeugt pro Zielteil ein neues `Part::Feature` und
  veraendert keine Quellobjekte.
- Assembly-Komponenten werden ueber die bestehende Auswahlhilfe aufgeloest.
- Der geometrische Kern wird ohne Qt umgesetzt und mit FreeCAD-Python-Formen
  verifiziert.

## Umgesetzt
- `lasercut/holetemplate.py` validiert Rollen und schneidet nur raeumliche
  Ueberlappungen aus Zielkoerpern aus.
- `panel/holetemplates.py` stellt Rollenwahl, Vorschau und Ergebnisobjekte
  bereit; der Befehl ist als `hole_templates` registriert.
- `panel/selection.py` loest auch Objekt-Mehrfachauswahl auf Assembly-Links
  auf.
- Ein fokussierter `unittest` prueft mehrere Schablonen, fehlende Schnitte und
  unzulaessige Doppelrollen.
- README, eigene Dokumentation und Werkzeug-Icon sind ergaenzt.
- Die drei fokussierten Tests bestehen; alle beruehrten Python-Dateien
  kompilieren ohne Fehler, und `git diff --check` ist sauber.
- Der echte OpenCascade-Geometrietest mit FreeCAD 1.1.3 besteht: Ein Zylinder
  schneidet zwei ueberlappende Platten, ein entfernter Koerper erzeugt kein
  Ergebnis. Die FUSE-freie Ausfuehrung verwendet
  `FreeCAD.AppImage --appimage-extract-and-run --console` mit einem Python-
  Skript ueber die Standardeingabe.

## Validierung
- Automatisierte Kern-, Syntax-, Whitespace- und echte FreeCAD-
  Geometriepruefungen sind abgeschlossen.

## Nachtraeglicher Assembly-Fix
- Ergebnisobjekte und die `HoleTemplates`-Gruppe speichern ihre Herkunft als
  `PropertyString` beziehungsweise `PropertyStringList` statt als
  `PropertyLink`. Damit entstehen keine unzulaessigen Links aus dem Ergebnis-
  Container in eine Assembly.
- Eine direkt ausgewaehlte `App::Link`-Instanz wird unveraendert verwendet.
  Bei mehreren Instanzen eines Quellobjekts wird keine beliebige Instanz mehr
  gewaehlt; der Auswahlpfad muss die konkrete Komponente bestimmen.
- Der reale FreeCAD-Test prueft beide Regeln erfolgreich.