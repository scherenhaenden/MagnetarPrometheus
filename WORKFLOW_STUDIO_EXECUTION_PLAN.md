# MagnetarPrometheus UI Workflow Studio
## Ausführungsplan, Fortschritt und Start von Teil 1

Version: 2026-04-09  
Sprache: Deutsch (Produktinhalt) + Spanisch (Arbeitsanweisung)

## Ziel dieses Dokuments
Dieses Markdown setzt deine Vorgabe um:
1. Regeln ernsthaft lesen und strukturiert arbeiten.
2. Einen klaren Umsetzungsplan für die Zielarchitektur definieren.
3. Den Fortschritt in einer Tabelle transparent machen.
4. Sofort mit **Teil 1 (Studio-Skelett)** starten.

## Umsetzungsplan (Phasen)

### Phase 1 — echtes Studio-Skelett
- Neue Editor-Route (`/studio`) in der Angular-App.
- Erstes Studio-Layout mit 5 Kernbereichen:
  - Node-Bibliothek
  - Canvas
  - Inspector
  - Toolbar
  - Debug/Logs/Run-Daten
- Sichtbarer Navigationseintrag zum Studio.
- Routing-Smoketest auf neue Route erweitern.

### Phase 2 — produktiver MVP
- Quick Add und direkte Next-Node-Vorschläge.
- Undo/Redo-Stack für Editor-Aktionen.
- Inline-Validierung am Graph und im Inspector.
- Run direkt aus dem Studio inklusive Node-Status.
- Basis Import/Export (Studio + Runtime).

### Phase 3 — starkes Produkterlebnis
- Templates, Teilgraphen und Subflows.
- Fortgeschrittene Run-Visualisierung inkl. Timeline.
- Dokumentations-Export (Markdown/PDF/Snapshot).
- Versionsvergleich und bessere In-Produkt-Doku.
- Kontextbezogene intelligente Vorschläge.

### Phase 4 — High-End
- Kollaboration in Echtzeit.
- Sharing/Publishing-Modelle.
- Marketplace/Plugin-basierte Nodes.
- Assistenten für Workflow-Aufbau.

## Fortschrittstabelle

| Teil | Beschreibung | Status | Fortschritt |
|---|---|---:|---:|
| Teil 1 | Studio-Skelett (Route, Layout, Navigation, Test) | In Arbeit | 75% |
| Teil 2 | MVP-Funktionen (Quick Add, Undo/Redo, Validation, Run) | Offen | 0% |
| Teil 3 | Produktstärke (Templates, Subflows, Doku-Export, Diff) | Offen | 0% |
| Teil 4 | High-End (Realtime-Kollaboration, Publishing, Marketplace) | Offen | 0% |

## Start mit Teil 1 (heute umgesetzt)

- Editor-Route `/studio` wurde in den App-Routenbaum aufgenommen.
- Neuer Feature-Screen `WorkflowStudioPage` wurde erstellt.
- Studio-Layout als 5-Bereich-Skelett wurde implementiert.
- Link „Workflow Studio“ wurde in die Seitennavigation integriert.
- Routing-Spec wurde um Navigation auf `/studio` erweitert.

## Nächster konkreter Schritt in Teil 1
Als nächstes wird der Canvas-Placeholder in eine erste interaktive `GraphCanvas`-Komponente überführt (Pan/Zoom + Grundselektion als Basis für Teil 2).
