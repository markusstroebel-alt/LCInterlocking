# Umsetzung: Ausgewaehlte Bodies hinzufuegen

## Status
- Plan freigegeben.
- Umsetzung erfolgt auf `feature/connection-hole-templates`.

## Entscheidungen
- Neue Bodies werden immer zuerst neutral unter `Selected bodies` eingefuegt.
- Doppelte Namen ueber alle drei Listen werden ignoriert.
- Die aktuelle FreeCAD-Auswahl wird erst beim Klick auf den neuen Button
  aufgeloest, damit sie waehrend eines offenen Edit-Dialogs veraendert werden
  kann.

## Validierung
- Die drei fokussierten Kern-Unit-Tests bestehen.
- Alle beruehrten Python-Dateien kompilieren ohne Fehler.
- `git diff --check` ist sauber.
- Der echte FreeCAD-1.1.3-AppImage-Test besteht einschliesslich der
  Deduplizierung neuer Bodies.

## Umgesetzt
- `_new_objects()` filtert bereits vorhandene Objektnamen aus einer neuen
  Auswahl.
- **Add selected bodies** liest die aktuelle, Assembly-sicher aufgeloeste
  FreeCAD-Auswahl beim Klick und fuegt nur neue Bodies zu `Selected bodies`
  hinzu.
- Der reale FreeCAD-Test prueft, dass ein bestehender Body nicht doppelt und
  ein neuer Body genau einmal aufgenommen wird.
- README und Fachanleitung beschreiben die Erweiterung im offenen Dialog.