# Workflow für größere Änderungen

## Was zählt als "größere Änderung"
Neue Features, neue Module/Panels, strukturelle Änderungen, API-Änderungen oder Refactorings über mehrere Dateien hinweg. Ausgenommen sind kleine Bugfixes, Tippfehler und reine Doku-Updates — diese können direkt umgesetzt werden.

## Pflichtablauf vor der Umsetzung
1. Vor jeder größeren Änderung einen Plan in `ai/plans/<feature-name>.md` erstellen. Der Plan enthält mindestens:
   - Ziel/Beschreibung der Änderung
   - Geplantes Vorgehen (Schritte)
   - Betroffene Dateien/Module
   - Offene Fragen/Annahmen
2. Den Plan dem Nutzer zur Freigabe vorlegen und explizit abwarten, bevor mit der Umsetzung begonnen wird. Ohne Freigabe nicht implementieren.
3. Erst nach Freigabe einen eigenen Feature-Branch anlegen (`git checkout -b feature/<feature-name>`) und darauf arbeiten.
4. Zusätzlich zum Plan zwei weitere Dateien im selben Ordner anlegen:
   - `ai/plans/<feature-name>.memory.md`: eigene Erinnerungsdatei für den Agenten (Fortschritt, Zwischenstand, offene Todos, Entscheidungen) — während der Umsetzung laufend aktualisieren.
   - `ai/plans/<feature-name>.README.md`: kurze, nutzerfreundliche Beschreibung des Features (Zweck, Nutzung, relevante Dateien) — am Ende der Umsetzung finalisieren.

## Während der Umsetzung
- Feingranular committen: nach jedem sinnvollen Zwischenschritt ein Commit, damit einzelne Schritte bei Bedarf zurückgenommen werden können.
- Bei Unklarheiten in Anforderung oder Plan immer nachfragen statt Annahmen zu raten.
- Die Erinnerungsdatei (`*.memory.md`) nach jedem wichtigen Schritt aktualisieren, damit der Kontext auch in einer neuen Konversation wiederhergestellt werden kann.
