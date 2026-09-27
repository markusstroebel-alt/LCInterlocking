# Mehrere Verbindungen pro Face

Dieses geplante Feature erlaubt mehrere unabhaengige Interlocking-Verbindungen auf
derselben CAD-Flaeche. Beispielsweise kann eine durchgehende Nut mit einer
Schraubverbindung kombiniert werden.

Jede Verbindung erhaelt intern eine eigene ID und erscheint im MultiJoin-Baum als
separater Eintrag. Gleichartige Eintraege erhalten zur Unterscheidung einen Suffix wie
`Face1 (Screw #2)`. Bestehende `Add same faces`-Verknuepfungen bleiben an ihre jeweilige
Master-Verbindung gebunden.

Die Umstellung setzt eine neue MultiJoin-Konfiguration voraus; eine Migration alter
gespeicherter MultiJoins ist nicht vorgesehen.