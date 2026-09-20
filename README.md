# Vermietung Second Brain: fiktives Beispiel für sieben Wohnungen

Dieses Repository zeigt ein Markdown-basiertes Second Brain für **sieben fiktive Wohnungen**, die **zwei Personen** gemeinsam verwalten. Sämtliche Kennungen, Flächen, Beträge, Termine und Vorgänge sind frei erfundene Beispieldaten. Es enthält keine echten Adressen, Personennamen, Kontaktdaten, Verträge oder Dokumente.

## Idee

Statt Informationen aus vielen Unterlagen immer neu zusammenzusuchen, hält jede kurze Notiz einen Sachverhalt fest. Ein AI-Client kann anhand von [AGENTS.md](AGENTS.md) zuerst den aktuellen Stand, dann den Index und schließlich nur die passende Notiz lesen. Alle Dateien sind normales Markdown und lassen sich auch ohne AI in einem Texteditor oder Obsidian nutzen.

Die sieben Wohnungen heißen `W01` bis `W07`. Hausweite Themen tragen die Kennung `HAUS`. `Person A` und `Person B` sind lediglich neutrale Rollen für die zwei Vermietungspersonen. Das Beispiel nutzt ein fiktives gemeinsames Haus; das Schema funktioniert auch mit mehreren Häusern, wenn man die Objektkennungen entsprechend erweitert.

## Aufbau

| Datei oder Ordner | Aufgabe |
|---|---|
| [AGENTS.md](AGENTS.md) | Regeln und Befehle für einen AI-Client |
| [_hot.md](_hot.md) | Kurzer aktueller Arbeitsstand |
| [_index.md](_index.md) | Routing und Liste aller Beispielnotizen |
| [Fristen.md](Fristen.md) | Übersicht aus `fristen:` in den Notizen |
| 15 Themenordner | Fachnotizen und jeweils eine `_vorlage.md` |

Jede Fachnotiz beginnt mit Metadaten:

```yaml
---
objekt: W01             # W01 bis W07 oder HAUS
stand: 2026-09-01       # Informationsstand, bei offenen Notizen leer
status: aktuell         # offen, aktuell oder veraltet
quelle: Beispieldatensatz
fristen:
  - "2027-01-15 | Beispieltermin prüfen"
---
```

Danach folgen Titel, eine kurze Zusammenfassung und die fachlichen Felder. Der Dateiname beginnt mit der Objektkennung, etwa `W01_Mietvertrag.md`. Hausweite Informationen liegen unter `HAUS_...`.

## So funktioniert der Arbeitsablauf

| Eingabe an den AI-Client | Ergebnis |
|---|---|
| Eine Frage wie „Welche Beispielmiete gilt für W03?“ | Der Client liest `_hot.md`, `_index.md` und nur die verlinkte Fachnotiz. |
| `Update` | Notizliste und Fristen werden aus allen Fachnotizen neu erstellt; zusätzlich werden Widersprüche, fehlende Felder, kaputte Links und mögliche private Daten gemeldet. |
| `Monatsreview` | Der Client schlägt ältere oder offene Angaben zur Prüfung vor, höchstens vier Fragen pro Runde. Antworten werden in den passenden Notizen gepflegt. |
| `Befüllen` | Offene Felder werden im Dialog geklärt und danach mit `Update` abgeglichen. |

Der AI-Client führt diese Abläufe anhand von `AGENTS.md` aus. Es gibt keinen Hintergrunddienst und keine automatischen Erinnerungen. Eine Änderung per Hand ist ebenfalls möglich; danach sorgt `Update` für konsistente Übersichten.

## Beispiel-Fragen

- „Wie viele fiktive Wohnungen sind im Index?“
- „Welche Beispiel-Kaltmiete steht in W03?“
- „Welche offenen Punkte und Wiedervorlagen gibt es?“
- „Welche Notiz enthält den Musterprozess für einen Mieterwechsel?“

## Zusammenarbeit und Datenschutz

Beide Vermietungspersonen verwenden dieselbe Ordnerstruktur und dieselben Regeln. Gleichzeitige Änderungen an derselben Datei sollten vermieden werden; Konfliktkopien werden beim `Update` gemeldet. Originalverträge, Scans, Fotos, Ausweisdaten, Konto- und Vertragsnummern, E-Mail-Adressen und Telefonnummern gehören nicht in dieses Beispiel. `quelle:` verweist in einem echten, **separat und privat** geführten Arbeitsbestand nur auf den eigenen Ablageort, ohne Dateien oder Zugänge zu veröffentlichen.

Für die praktische Nutzung sollte ein **neuer privater Ordner** aus der Struktur entstehen. Dieses Demo-Repository bleibt ein reines Demo-Repository. Vor jedem Commit die Änderungen und die Git-Historie auf echte Daten prüfen; `.gitignore` allein verhindert nicht, dass sensible Markdown-Texte versehentlich veröffentlicht werden.

Die Beispiele sind keine Rechts-, Steuer- oder Finanzberatung. Fristen und Vertragsklauseln müssen für reale Fälle anhand aktueller Unterlagen und Regeln geprüft werden. Steuerunterlagen und Buchhaltung sind hier bewusst nicht Teil des Konzepts.
