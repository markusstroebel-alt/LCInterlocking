# Umsetzung: Verwaltete Lochschablonen im Baum

## Status
- Plan freigegeben.
- Umsetzung erfolgt auf der vorhandenen Branch
  `feature/connection-hole-templates`.

## Entscheidungen
- Die bestehende Differenzlogik in `lasercut/holetemplate.py` bleibt erhalten.
- Der neue `Part::FeaturePython` speichert nur Objektnamen, um Assembly-
  Scope-Warnungen zu vermeiden.
- Erzeugte Ergebnisobjekte werden als direkte Tree-Kinder beansprucht und bei
  Neuberechnung anhand ihres Zielobjektnamens wiederverwendet.

## Validierung
- Die drei fokussierten Kern-Unit-Tests bestehen.
- Alle beruehrten Python-Dateien kompilieren ohne Fehler.
- `git diff --check` ist sauber.
- Der echte FreeCAD-1.1.3-AppImage-Test besteht, einschliesslich
  Ergebnis-Wiederverwendung und Bereinigung alter Tree-Kinder.

## Umgesetzt
- `HoleTemplateGroup` verwaltet Namensrollen, Ergebnisobjekte, stabile
  Ziel-zu-Ergebnis-Zuordnung und die Entfernung veralteter Ergebnisse.
- `HoleTemplateViewProvider` beansprucht die Ergebnisse als Tree-Kinder und
  oeffnet den Dialog ueber **Edit** wieder.
- Der Dialog erzeugt beim ersten Bestaetigen einen `Part::FeaturePython`-
  Knoten; bei der Bearbeitung uebernimmt er gespeicherte Rollen und
  aktualisiert denselben Knoten.
- Zielkoerper werden ausserhalb des Edit-Modus ausgeblendet, Ergebnisse
  angezeigt; Template-Koerper bleiben sichtbar.
- Der echte FreeCAD-Test deckt Tree-Kinder, Wiederverwendung und Entfernung
  veralteter Ergebnisse ab.