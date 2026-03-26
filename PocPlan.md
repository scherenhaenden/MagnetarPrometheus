# MagnetarPrometheus

## Projekttitel

MagnetarPrometheus ist ein modulares, erweiterbares und sprachunabhängiges Workflow-Orchestrierungssystem, dessen erste lauffähige Version in Python implementiert wird. Das System dient als zentrales Steuerprogramm für beliebig viele Module. Jedes Modul beschreibt fachliche oder technische Abläufe in Form von Schritten, Regeln, Bedingungen und Folgeaktionen. Die zentrale Engine lädt diese Module, interpretiert deren Definitionen, führt die vorgesehenen Schritte kontrolliert aus, verwaltet den Zustand des laufenden Workflows und entscheidet anhand definierter Regeln oder AI-basierter Auswertung über Verzweigungen, Wiederholungen, Fehlerbehandlung und Abschluss.

Das System soll so entworfen werden, dass es zunächst vollständig in Python als Proof of Concept erstellt werden kann, ohne sich architektonisch an Python zu binden. Später sollen einzelne Teile oder ganze Ausführungskomponenten schrittweise nach TypeScript oder bei Bedarf nach C#, Go oder Rust ausgelagert werden können, ohne dass die Workflow-Definitionen oder die zentrale Modellierung neu geschrieben werden müssen.

## Ziel des Projekts

Das Hauptziel von MagnetarPrometheus ist die Bereitstellung eines zentralen Programms, das Fachlogik nicht hart im Code verdrahtet, sondern über deklarative Module und standardisierte Ausführungseinheiten steuert. Ein Modul soll beschreiben können, welche Eingaben gelesen werden, welche Datenquellen benutzt werden, welche Regeln zur Entscheidung herangezogen werden, wann externe Systeme oder AI-Dienste aufgerufen werden, wie Antworten interpretiert werden und welche Folgeaktionen daraus entstehen.

MagnetarPrometheus soll deshalb nicht nur ein Task Runner sein, sondern eine allgemeine Laufzeitumgebung für zustandsbehaftete, verzweigende und beobachtbare Workflows.

## Nicht-Ziele der ersten Version

Die erste Version von MagnetarPrometheus soll noch kein voll verteiltes Clustersystem, kein Kafka-basiertes Event Mesh, kein grafischer Drag-and-drop-Designer und keine hochkomplexe Multi-Tenant-SaaS-Plattform sein. Die erste Version soll auch keine vollständige BPMN-Engine nach Norm sein. Stattdessen soll die erste Version eine robuste, saubere und erweiterbare Grundlage schaffen, mit der echte Geschäftsprozesse bereits lokal oder serverseitig ausgeführt werden können.

## Leitprinzipien

MagnetarPrometheus basiert auf einigen nicht verhandelbaren Architekturprinzipien. Erstens müssen Workflows als Daten modelliert werden und dürfen nicht ausschließlich implizit im Quellcode verborgen sein. Zweitens muss die Orchestrierung von der konkreten Implementierung eines Schrittes getrennt sein. Drittens muss der Laufzeitkontext sauber versioniert, validiert und nachvollziehbar verändert werden. Viertens muss jeder Schritt beobachtbar, protokollierbar und reproduzierbar sein. Fünftens muss die Architektur so offen sein, dass dieselbe Workflow-Definition später mit anderen Executor-Typen ausgeführt werden kann.

## Kernidee des Systems

Ein Workflow besteht aus einer Menge benannter Schritte. Jeder Schritt hat einen Typ, optionale Konfigurationsparameter, definierte Eingaben, definierte Ausgaben und mindestens eine definierte Art, wie der nächste Schritt bestimmt wird. Ein Schritt kann linear fortfahren, auf Basis von Regeln verzweigen, einen Fehlerpfad auslösen, einen AI-Dienst befragen oder Daten aus dem gemeinsamen Kontext lesen und dort wieder ablegen.

Die Engine ist nicht dafür zuständig, die fachliche Arbeit eines Schrittes inhaltlich zu kennen. Sie ist dafür zuständig, Workflows zu laden, deren Struktur zu validieren, Ausführungsschritte zu starten, Eingaben an Executor-Komponenten zu übergeben, Ergebnisse in den Kontext zurückzuführen und den nächsten Schritt zu bestimmen.

## Grundbegriffe

Der Begriff Workflow bezeichnet die vollständige Definition eines ausführbaren Prozesses. Ein Workflow besitzt eine eindeutige Kennung, Metadaten, eine Startdefinition, optionale globale Einstellungen und eine Menge von Schritten.

Der Begriff Step bezeichnet eine atomare Ausführungseinheit. Ein Step kann etwa E-Mails lesen, Daten aus einem Speicher laden, Regeln anwenden, einen Prompt für ein AI-Modell erzeugen, eine API aufrufen, Dateien transformieren oder Entscheidungen klassifizieren.

Der Begriff Context bezeichnet den zur Laufzeit geführten Zustand des Workflows. Der Context enthält Eingabedaten, Zwischenergebnisse, Entscheidungen, technische Statusinformationen, Korrelationen, Fehler und alle Daten, die für Folgeentscheidungen benötigt werden.

Der Begriff Module bezeichnet eine logisch zusammengehörige Sammlung von Workflow-Definitionen, Step-Implementierungen, Validierungsregeln, optionalen Mappern und optionalen Ressourcen wie Prompt-Templates oder Regeldateien.

Der Begriff Executor bezeichnet die technische Laufzeitkomponente, die einen Step eines bestimmten Typs tatsächlich ausführt. Zunächst gibt es einen Python-internen Executor. Später können HTTP-, gRPC-, TypeScript-, C#-, Go- oder Rust-Executor ergänzt werden.

## Fachliches Zielbild

Ein Modul soll beschreiben können, dass zuerst E-Mails aus einem Postfach gelesen werden. Danach sollen Inhalte, Anhänge, Absenderdaten oder Betreffinformationen extrahiert werden. Anschließend sollen Regeln geladen werden, beispielsweise aus YAML, JSON oder einer Datenbank. Danach kann eine AI-Komponente gefragt werden, welche fachliche Kategorie vorliegt oder welche Aktion empfohlen wird. Die AI-Antwort darf aber nicht blind ausgeführt werden, sondern wird gegen definierte Regeln oder Policies ausgewertet. Anschließend wird entschieden, ob etwa eine Rechnung gespeichert, ein Ticket erstellt, eine Eskalation ausgelöst, eine Antwort generiert oder der Workflow angehalten werden soll.

Das bedeutet, MagnetarPrometheus ist bewusst für hybride Entscheidungslogik gebaut. Starre Regeln und flexible AI-Interpretation sollen zusammenarbeiten, ohne dass die Architektur unkontrollierbar wird.

## Zielarchitektur der ersten Version

Die erste Version besteht aus fünf Hauptschichten. Die erste Schicht ist die Workflow-Definition. Diese wird als YAML oder JSON gespeichert und beschreibt die Struktur des Ablaufs. Die zweite Schicht ist die Engine. Sie übernimmt Laden, Validieren, Starten, Stoppen, Fortsetzen und Steuern des Workflows. Die dritte Schicht ist der Context Store, der den Laufzeitstatus verwaltet. In der ersten Version genügt In-Memory mit optionaler Persistenz in JSON oder SQLite. Die vierte Schicht sind die Executors, welche konkrete Step-Typen ausführen. Die fünfte Schicht ist die Beobachtbarkeitsschicht mit Logging, Run-Historie, Statusereignissen und Fehlerdiagnose.

## Architekturentscheidung für den Start

Die erste Implementierung wird in Python geschrieben. Python ist für die erste Version die geeignetste Wahl, weil die Entwicklungsgeschwindigkeit hoch ist, die AI-Integration besonders einfach ist, dynamische Konfiguration unkompliziert verarbeitet werden kann und schnelle Proof-of-Concepts mit sauberer Erweiterbarkeit möglich sind.

Wichtig ist aber, dass Python nicht als endgültige Plattform des gesamten Systems verstanden wird. Python ist die erste Runtime der zentralen Engine. Die Verträge, Datenformate und Moduldefinitionen werden so entworfen, dass einzelne Steps oder ganze Ausführungsbereiche später in andere Sprachen ausgelagert werden können.

## Datengetriebene Definition statt harter Verdrahtung

Workflows müssen deklarativ sein. Die Workflow-Definition darf nicht bloß eine Hilfsdatei sein, sondern muss die maßgebliche Beschreibung des Ablaufs bilden. Die Engine soll aus der Definition erkennen können, welche Schritte existieren, welcher Schritt zuerst gestartet wird, wie Verzweigungen funktionieren, welche Eingaben ein Schritt benötigt, welcher Executor benutzt wird und wie Fehlerpfade behandelt werden.

## Beispiel einer Workflow-Definition

```yaml
id: email_triage
name: Email Triage Workflow
version: 1.0.0
start_step: fetch_emails

settings:
  max_retries_per_step: 3
  stop_on_unhandled_error: true

steps:
  fetch_emails:
    type: email.fetch
    executor: python
    config:
      mailbox: support@company.com
      unread_only: true
    next: extract_email_data

  extract_email_data:
    type: email.extract
    executor: python
    next: load_rules

  load_rules:
    type: rules.load
    executor: python
    config:
      source: ./rules/email_rules.yaml
    next: ai_decision

  ai_decision:
    type: ai.classify
    executor: python
    config:
      model: openai:gpt-5.4
      prompt_template: ./prompts/email_classification.txt
    next:
      mode: conditional
      conditions:
        - when: "context['ai']['decision'] == 'create_ticket'"
          go_to: create_ticket
        - when: "context['ai']['decision'] == 'store_invoice'"
          go_to: store_invoice
        - when: "context['ai']['decision'] == 'manual_review'"
          go_to: manual_review

  create_ticket:
    type: ticket.create
    executor: python
    next: end

  store_invoice:
    type: invoice.store
    executor: python
    next: end

  manual_review:
    type: review.queue
    executor: python
    next: end
```

Dieses Format ist nur ein Ausgangspunkt. Die endgültige Spezifikation darf erweitert werden, muss aber von Anfang an stabil genug sein, damit künftige Executor-Typen und neue Module dasselbe Grundmodell verstehen.

## Struktur des Laufzeitkontexts

Der Context ist das zentrale Datenelement jeder Ausführung. Er muss sauber strukturiert sein und darf nicht zu einer unkontrollierten Sammelmap werden. Der Context soll mindestens folgende Bereiche kennen. Der erste Bereich sind Metadaten zum Run, also Run-ID, Workflow-ID, Startzeit, aktueller Status und Korrelationen. Der zweite Bereich enthält die fachlichen Input-Daten. Der dritte Bereich enthält Zwischenergebnisse einzelner Steps. Der vierte Bereich enthält Entscheidungen, Klassifikationen, regelbasierte Bewertungen und AI-Antworten. Der fünfte Bereich enthält technische Informationen wie Retry-Zähler, Step-Historie und Fehlerzustände. Der sechste Bereich enthält optionale Artefakte wie erzeugte Dateien, Nachrichten oder externe Referenzen.

Eine mögliche Struktur kann so aussehen.

```json
{
  "run": {
    "id": "run-20260326-0001",
    "workflow_id": "email_triage",
    "status": "running",
    "current_step": "ai_decision"
  },
  "input": {
    "source": "mailbox",
    "mailbox": "support@company.com"
  },
  "data": {
    "emails": [],
    "rules": {},
    "attachments": []
  },
  "ai": {
    "decision": null,
    "raw_response": null,
    "confidence": null
  },
  "history": [],
  "errors": []
}
```

## Anforderungen an den Context

Jeder Step darf nur klar definierte Teile des Context lesen und verändern. Es muss nachvollziehbar sein, welche Felder vor einem Step vorhanden sein müssen und welche Felder nach dem Step zusätzlich gesetzt oder verändert werden. Für jede Step-Implementierung ist daher eine Eingabe- und Ausgabe-Spezifikation zu dokumentieren. In der ersten Version genügt dafür Pydantic-basierte Validierung. Später kann dies durch strengere Schemata, Versionierung und Migrationslogik erweitert werden.

## Ablaufmodell der Engine

Die Engine lädt eine Workflow-Definition, validiert deren Struktur und erzeugt einen Run-Kontext. Danach ermittelt sie den Startschritt. Anschließend führt sie den Workflow in einer kontrollierten Schleife aus. In jeder Iteration werden der aktuelle Step und dessen Definition geladen. Die Engine bestimmt den zuständigen Executor, übergibt den aktuellen Context, erhält ein Ergebnisobjekt zurück, verarbeitet den Rückgabestatus, aktualisiert den Context, protokolliert die Ausführung und bestimmt den nächsten Step. Dieser Vorgang wird wiederholt, bis ein Endzustand erreicht ist oder ein definierter Abbruch erfolgt.

## Rückgabemodell eines Steps

Ein Step darf nicht nur rohe Daten zurückgeben, sondern ein standardisiertes Ergebnisobjekt. Dieses Ergebnisobjekt muss mindestens enthalten, ob die Ausführung erfolgreich war, welche Daten in den Context geschrieben werden sollen, ob ein expliziter nächster Step vorgeschlagen wird, ob ein Fehler eingetreten ist und ob technische Metadaten wie Dauer, Warnungen oder externe Referenzen vorliegen.

Ein mögliches internes Modell ist folgendes.

```python
from pydantic import BaseModel
from typing import Any, Dict, Optional, List

class StepResult(BaseModel):
    success: bool
    output: Dict[str, Any] = {}
    next_step: Optional[str] = None
    warnings: List[str] = []
    error_code: Optional[str] = None
    error_message: Optional[str] = None
```

## Step-Vertrag

Jeder Step-Typ muss einen technischen Vertrag einhalten. Der Vertrag beschreibt, welchen Namen der Typ besitzt, welche Konfiguration er erwartet, welche Context-Felder er liest, welche Context-Felder er schreibt und in welchem Format das Ergebnis geliefert wird. Dieser Vertrag ist wichtiger als die konkrete Sprache der Implementierung. Nur so können später Python- und TypeScript-Implementierungen dieselben Step-Typen bedienen.

## Executor-Modell

Die Engine ruft nicht direkt beliebige Klassen hartverdrahtet auf. Stattdessen benutzt sie Executor-Komponenten. Ein Executor ist dafür zuständig, einen Step eines bestimmten Typs oder eines bestimmten technischen Ausführungsmodells auszuführen. In der ersten Version reicht ein PythonExecutor, der intern registrierte Python-Step-Implementierungen ausführt. Das Modell muss jedoch so gestaltet sein, dass später weitere Executors hinzukommen.

Der PythonExecutor führt lokale Python-Klassen oder Funktionen aus. Ein HttpExecutor ruft externe Dienste per HTTP auf. Ein GrpcExecutor ruft andere Prozesse mit stark typisierten Protokollen auf. Ein ProcessExecutor könnte lokale Binärprogramme starten. Ein TsExecutor wäre technisch gesehen eine spezielle Ausprägung eines externen Executors und würde in der Praxis meist über HTTP, gRPC oder Prozessaufrufe angebunden.

## Warum der Executor zentral ist

Der Executor ist die entscheidende Entkopplungsschicht. Solange Workflows Steps nur über Typ, Executor-Art und Konfiguration referenzieren, ist das System nicht an Python gefesselt. Ein Step-Typ wie `invoice.store` kann heute lokal in Python laufen und morgen als TypeScript-Service angesprochen werden, ohne dass der Workflow fachlich geändert werden muss. Nur die technische Zuordnung ändert sich.

## Modulkonzept

Ein Modul ist eine deploybare, logisch zusammengehörige Einheit. Es kann einen oder mehrere Workflows enthalten. Es kann eigene Step-Implementierungen bereitstellen. Es kann Prompts, Regeln, Mapper, Beispielkonfigurationen und Validierungslogik enthalten. Ein Modul muss eine Manifest-Datei besitzen, damit die Engine weiß, welche Workflows, Step-Typen und Ressourcen das Modul bereitstellt.

Eine mögliche Modulstruktur lautet wie folgt.

```text
modules/
  email_module/
    manifest.yaml
    workflows/
      email_triage.yaml
    steps/
      fetch_emails.py
      extract_email_data.py
      load_rules.py
      ai_classify.py
    prompts/
      email_classification.txt
    rules/
      email_rules.yaml
```

## Inhalt eines Modul-Manifests

Das Manifest muss den Modulnamen, die Version, eine Beschreibung, die Liste enthaltener Workflows, die registrierten Step-Typen und optionale Abhängigkeiten deklarieren. Das Manifest dient der Engine dazu, Module beim Start oder zur Laufzeit systematisch zu laden.

## Verzweigungen und Entscheidungslogik

MagnetarPrometheus muss Verzweigungen als erstklassiges Konzept unterstützen. Verzweigungen dürfen nicht nur durch hart im Step-Code codierte Entscheidungen entstehen. Die Workflow-Definition muss Bedingungen beschreiben können. Diese Bedingungen dürfen auf den Context zugreifen. Für die erste Version reicht eine sichere und eingeschränkte Auswertung einfacher Ausdrücke. Langfristig sollte eine kleine, kontrollierbare Expressions-Sprache oder ein Policy-Layer eingeführt werden.

Es muss außerdem möglich sein, dass ein Step einen expliziten `next_step` zurückgibt. Dies ist besonders nützlich bei AI-basierten Entscheidungen. Trotzdem soll die Engine entscheiden, ob dieser Vorschlag akzeptiert wird. Das erlaubt Governance und zusätzliche Sicherheitsregeln.

## Rollen von Regeln und AI

AI darf Entscheidungen vorbereiten, klassifizieren oder Handlungsempfehlungen erzeugen. Die endgültige Ausführungssteuerung sollte in kritischen Fällen jedoch durch Regeln abgesichert werden. Dadurch werden Fehlklassifikationen, Halluzinationen oder unzulässige Folgeaktionen reduziert. AI dient in MagnetarPrometheus also als intelligenter Interpretations- oder Bewertungsbaustein, nicht als unkontrollierter Ersatz für die komplette Prozesslogik.

## AI-Integration

Die AI-Integration muss als eigener Step-Typ oder als Familie von Step-Typen modelliert werden. Es soll mindestens Schritte für Klassifikation, Extraktion, Zusammenfassung, Regelinterpretation und nächste Handlungsempfehlung geben. Jeder AI-Step muss das verwendete Modell, das Prompt-Template, optionale Temperatur- oder Striktheitsparameter, Timeouts und Validierungsregeln für die Antwort kennen.

Jede AI-Antwort muss in MagnetarPrometheus sowohl roh als auch normalisiert gespeichert werden. Rohantworten sind wichtig für Debugging und Nachvollziehbarkeit. Normalisierte Antworten sind wichtig für die weitere maschinelle Verarbeitung.

## Regelverarbeitung

Regeln müssen zunächst in einfachen Formaten vorliegen können, etwa YAML oder JSON. Eine Regeldatei kann definieren, welche Absender priorisiert werden, wie Betreffmuster zu bewerten sind, welche Dokumenttypen wohin gespeichert werden, wann eine manuelle Prüfung nötig ist oder welche AI-Antworten überhaupt zulässig sind. Regeln werden von einem dedizierten Step geladen und in den Context übernommen.

## Fehlerbehandlung

Fehlerbehandlung ist ein Kernbestandteil und darf nicht nachträglich improvisiert werden. Jeder Step kann erfolgreich, fehlgeschlagen, teilweise erfolgreich oder in einem manuellen Review-Zustand enden. Fehler müssen kategorisiert werden. Mindestens zu unterscheiden sind technische Fehler, externe Systemfehler, Validierungsfehler, Konfigurationsfehler und fachliche Ablehnungen.

Die Engine muss pro Step definierte Retry-Regeln kennen. Ein API-Timeout kann erneut versucht werden. Eine ungültige Konfiguration darf nicht wiederholt werden. Ein AI-Step mit nicht parsebarer Antwort kann mit anderem Prompt oder strengerem Output-Format erneut ausgeführt werden. Ein Fehlerpfad muss in der Workflow-Definition referenzierbar sein.

## Idempotenz

Jeder Step, der externe Aktionen ausführt, etwa Speichern, Senden, Erstellen oder Aktualisieren, muss idempotent entworfen werden oder eine Idempotenzstrategie deklarieren. Dies ist besonders wichtig bei Retries. Die Engine muss im Run-Kontext festhalten können, ob eine externe Aktion bereits erfolgreich ausgeführt wurde, damit sie nicht versehentlich doppelt erfolgt.

## Persistenzstrategie

Die erste Version kann mit In-Memory-State und optionalem JSON- oder SQLite-Backup arbeiten. Dennoch muss die Architektur so aufgebaut sein, dass später echte Persistenzadapter eingesetzt werden können. Deshalb soll der Context Store über ein Interface abstrahiert werden. Spätere Implementierungen könnten SQLite, PostgreSQL, Redis oder andere Speicherlösungen nutzen.

Es soll möglich sein, Runs zu speichern, wiederaufzunehmen, ihren Status abzufragen und abgeschlossene Runs historisch zu analysieren.

## Logging und Beobachtbarkeit

MagnetarPrometheus muss jeden Run, jeden Step, jede Übergabe an einen Executor, jede Rückgabe und jeden Fehler sauber protokollieren. Logging ist nicht nur für Fehleranalyse nötig, sondern auch für Auditierbarkeit. Für jeden Step-Lauf sollten mindestens Startzeit, Endzeit, Dauer, Eingabereferenz, Ergebnisstatus und Fehlerdetails protokolliert werden.

Zusätzlich soll es eine strukturierte Run-Historie geben, in der sichtbar ist, welche Schritte in welcher Reihenfolge durchlaufen wurden. Für die erste Version reicht strukturiertes Logging in JSON und eine lokale Historie im Context. Später können OpenTelemetry, Grafana, Loki oder vergleichbare Systeme ergänzt werden.

## Sicherheitsprinzipien

Das System wird potenziell mit E-Mails, AI-Anfragen, Dateiinhalten, Regeln und externen APIs arbeiten. Deshalb müssen Secrets, API-Keys und Zugangsdaten strikt außerhalb der Workflow-Dateien gespeichert werden. Konfigurierbare Parameter für sensible Daten dürfen nur auf Umgebungsvariablen oder Secret Stores verweisen.

Außerdem darf die Auswertung von Bedingungen im Workflow nicht beliebig Code ausführen. Für die erste Version kann eine stark eingeschränkte Expressions-Auswertung verwendet werden. Ein unkontrolliertes `eval` über untrusted Daten ist ausdrücklich zu vermeiden.

## Konfigurationsmodell

MagnetarPrometheus benötigt eine globale Systemkonfiguration. Diese definiert Pfade zu Modulen, Logging-Konfiguration, Standard-Executoren, AI-Provider, Secret-Referenzen, Default-Timeouts und Persistenzadapter. Zusätzlich besitzt jedes Modul eigene Konfigurationsdaten. Zusätzlich besitzt jeder Workflow seine eigene Ablaufdefinition. Damit entsteht eine dreistufige Konfiguration aus globaler Ebene, Modulebene und Workflow-Ebene.

## Empfohlene Projektstruktur für die erste Implementierung

```text
magnetar_prometheus/
  app/
    main.py
    bootstrap.py
  core/
    engine.py
    workflow_loader.py
    workflow_validator.py
    context_manager.py
    executor_router.py
    models/
      workflow.py
      step_definition.py
      step_result.py
      run_context.py
  executors/
    base.py
    python_executor.py
    http_executor.py
  registry/
    step_registry.py
    module_registry.py
  modules/
    email_module/
      manifest.yaml
      workflows/
        email_triage.yaml
      steps/
        fetch_emails.py
        extract_email_data.py
        load_rules.py
        ai_classify.py
        create_ticket.py
        store_invoice.py
        manual_review.py
      prompts/
        email_classification.txt
      rules/
        email_rules.yaml
  infrastructure/
    logging/
      logger_factory.py
    persistence/
      base_store.py
      memory_store.py
      sqlite_store.py
    ai/
      base_ai_client.py
      openai_client.py
  tests/
    unit/
    integration/
  config/
    app.yaml
  README.md
```

## Technische Kernklassen der ersten Version

Die Klasse `WorkflowLoader` lädt Workflow-Dateien und Modul-Manifeste. Die Klasse `WorkflowValidator` prüft Struktur und Pflichtfelder. Die Klasse `Engine` steuert die Ausführung. Die Klasse `ExecutorRouter` ermittelt den passenden Executor. Die Klasse `ContextManager` erstellt, aktualisiert und speichert den Laufzeitkontext. Die Klasse `StepRegistry` kennt lokal verfügbare Python-Step-Implementierungen. Die Klasse `ModuleRegistry` verwaltet geladene Module.

## Startpunkt der Anwendung

Die Anwendung soll über einen klaren Bootstrap-Prozess verfügen. Beim Start werden die globale Konfiguration geladen, Module erkannt, Manifeste gelesen, Workflows registriert, Step-Typen an das Registry-System gebunden und die Engine vorbereitet. Danach kann entweder ein bestimmter Workflow manuell gestartet oder später über API, CLI oder Trigger-Systeme aktiviert werden.

## Trigger-Modell der ersten Version

Für den Anfang reicht ein manuelles Trigger-Modell. Ein Workflow kann per CLI oder direktem Python-Aufruf gestartet werden. Später können Trigger für E-Mail-Ereignisse, Zeitpläne, Dateieingänge, HTTP-Webhooks oder Queue-Nachrichten ergänzt werden. Das Trigger-Modell soll deshalb schon jetzt als eigene Schicht betrachtet werden, auch wenn es zunächst minimal umgesetzt wird.

## Beispiel für eine Step-Basisklasse in Python

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from core.models.step_result import StepResult

class BaseStep(ABC):
    @abstractmethod
    def run(self, context: Dict[str, Any], config: Dict[str, Any]) -> StepResult:
        pass
```

## Beispiel für die Engine-Schleife

```python
class Engine:
    def __init__(self, workflow_loader, executor_router, context_manager, logger):
        self.workflow_loader = workflow_loader
        self.executor_router = executor_router
        self.context_manager = context_manager
        self.logger = logger

    def run(self, workflow_id: str, initial_context: dict | None = None) -> dict:
        workflow = self.workflow_loader.load_workflow(workflow_id)
        context = self.context_manager.create(workflow_id, initial_context or {})
        current_step_name = workflow.start_step

        while current_step_name != "end":
            step_def = workflow.steps[current_step_name]
            executor = self.executor_router.get_executor(step_def.executor)
            result = executor.execute(step_def, context)
            context = self.context_manager.apply_step_result(context, current_step_name, result)
            current_step_name = self._resolve_next_step(step_def, context, result)

        context["run"]["status"] = "completed"
        return context
```

## Regeln für `_resolve_next_step`

Die Methode `_resolve_next_step` muss die Priorität der Entscheidungsquellen klar definieren. Erstens darf ein Step-Ergebnis einen expliziten `next_step` vorschlagen. Zweitens kann die Workflow-Definition eine lineare Fortsetzung vorgeben. Drittens kann die Definition ein bedingtes Regelwerk enthalten. Viertens kann im Fehlerfall ein definierter Fehlerpfad verwendet werden. Diese Priorisierung muss fest dokumentiert sein, damit die Laufzeit reproduzierbar bleibt.

## Mindestanforderungen an Tests

Bereits die erste Version muss testbar sein. Es sollen Unit-Tests für Workflow-Validierung, Next-Step-Auflösung, Context-Aktualisierung und Executor-Routing existieren. Zusätzlich sollen Integrations-Tests für mindestens einen echten End-to-End-Workflow vorhanden sein. Besonders wichtig sind Tests für Verzweigungen, Fehlerpfade und AI-Antwortnormalisierung.

## Anforderungen an Coding Style und Erweiterbarkeit

Der Code soll klar getrennte Verantwortlichkeiten haben. Es dürfen keine versteckten Seiteneffekte zwischen Core, Infrastructure und Modulen entstehen. Jeder technische Bereich soll über Interfaces oder zumindest klar abgegrenzte Klassen entkoppelt werden. Step-Implementierungen dürfen keine Kenntnis von internen Details der Engine benötigen. Sie sollen nur den Context und ihre Konfiguration kennen.

## Migrationsfähigkeit zu TypeScript und anderen Sprachen

Die spätere Migration einzelner Teile nach TypeScript ist ausdrücklich vorgesehen. Damit das sauber funktioniert, muss bereits die erste Version folgende Bedingungen erfüllen. Erstens müssen Workflow-Dateien sprachneutral bleiben. Zweitens müssen Step-Typen als Verträge dokumentiert sein. Drittens darf der zentrale Context nicht nur implizit Python-spezifische Datentypen enthalten. Viertens müssen Executoren austauschbar sein. Fünftens sollen neue externe Executor-Arten ohne Umbau der Engine ergänzt werden können.

Ein späterer TypeScript-Dienst kann dann beispielsweise einen Step `document.classify` übernehmen. Der Workflow bleibt gleich. Der Executor-Typ wird auf `http` oder `grpc` gestellt. Die Engine ruft dann den TypeScript-Dienst an. So erfolgt Migration nicht als Rewrite, sondern als schrittweise Verlagerung technischer Verantwortung.

## PoC-Umfang der ersten umsetzbaren Version

Die erste konkrete Version von MagnetarPrometheus soll bewusst klein, aber vollständig sein. Sie soll genau einen lauffähigen Workflow enthalten, etwa einen E-Mail-Triage-Workflow. Sie soll lokal gestartete Module laden können. Sie soll Python-Schritte ausführen können. Sie soll mindestens lineare Abläufe und eine bedingte Verzweigung unterstützen. Sie soll den Context im Speicher halten und am Ende als JSON ausgeben können. Sie soll Logging für Step-Start, Step-Ende und Fehler schreiben. Sie soll mindestens eine AI-Integration besitzen, auch wenn diese zunächst gegen eine einfache Mock-Komponente läuft.

## Konkrete Umsetzungsreihenfolge

Die erste Umsetzungsphase beginnt mit dem Domänenmodell. Es werden die Modelle für Workflow, StepDefinition, StepResult und RunContext definiert. Danach wird die Workflow-Ladeschicht gebaut. Danach folgt die Validierung. Anschließend wird die Engine-Schleife erstellt. Danach wird der PythonExecutor implementiert. Danach wird das Registry-System für lokale Step-Typen aufgebaut. Danach wird ein erstes Beispielmodul erstellt. Danach folgen Logging, Tests und minimale Persistenz.

## Erstes Beispielmodul

Das erste Modul sollte bewusst den vollständigen Weg vom Input bis zur Verzweigung zeigen. Ein E-Mail-Modul ist dafür gut geeignet. Es kann zunächst mit Mock-Daten arbeiten, statt sofort reale Mailboxen anzubinden. Der Workflow könnte beispielhaft E-Mail-Daten lesen, Absender und Betreff extrahieren, Regeln laden, einen AI-Schritt zur Kategorisierung ausführen und danach anhand des Ergebnisses einen von drei Pfaden gehen. Dadurch wird die gesamte Architektur sichtbar, ohne sich sofort in Infrastrukturdetails zu verlieren.

## Versionierungsstrategie

Workflow-Definitionen und Module sollen Versionen besitzen. Auch der Context kann später ein Schema-Level erhalten. In der ersten Version reicht eine einfache semantische Versionsangabe im Manifest und in der Workflow-Definition. Später kann daraus ein Migrationssystem entstehen.

## Erweiterungen nach der ersten Version

Nach dem erfolgreichen PoC können mehrere Ausbaustufen folgen. Dazu gehören Persistenz in SQLite oder PostgreSQL, pausierbare und fortsetzbare Runs, echte Mailbox-Anbindung, Webhook-Trigger, HTTP-API zum Starten und Überwachen von Workflows, externe Executor-Prozesse, parallele Pfade, Sub-Workflows, Dead-Letter-Mechanismen und ein UI für Run-Historie und Debugging.

## Architekturentscheidung zur Parallelität

Parallelität soll nicht in die erste Version gezwungen werden. Die Engine der ersten Version arbeitet seriell. Dennoch soll das Domänenmodell nicht ausschließen, dass später Schritte oder Teilpfade parallel ausgeführt werden können. Deshalb sollten Step-Ergebnisse und Run-Zustände so modelliert werden, dass mehrere aktive Branches später theoretisch abbildbar sind.

## Abschließende Projektdefinition

MagnetarPrometheus ist ein zentrales, modulbasiertes Workflow-Orchestrierungssystem mit deklarativ beschriebenen Abläufen, kontrollierter Step-Ausführung, zustandsbehaftetem Context, regel- und AI-gestützter Entscheidungslogik und austauschbaren Executor-Komponenten. Die erste Version wird als Python-PoC implementiert, jedoch ausdrücklich so entworfen, dass einzelne technische Ausführungseinheiten später ohne Architekturbruch nach TypeScript oder andere Sprachen ausgelagert werden können. Das System trennt Orchestrierung, Definition, Ausführung und technische Infrastruktur sauber voneinander und bildet damit eine belastbare Grundlage für komplexe, verzweigende, beobachtbare und langfristig sprachunabhängige Geschäftsprozesse.

## Sofort umsetzbare nächste Schritte

Als unmittelbarer nächster Schritt sollen jetzt die Pydantic-Modelle für Workflow, StepDefinition, StepResult und RunContext erstellt werden. Danach soll die minimale `WorkflowLoader`-Klasse inklusive Laden einer YAML-Datei implementiert werden. Danach soll eine erste `Engine` mit serieller Ausführung entstehen. Parallel dazu wird ein erstes Modul `email_module` mit einem Beispielworkflow und drei bis fünf Mock-Steps angelegt. Sobald diese Basis läuft, kann auf derselben Grundlage die echte Erweiterung beginnen.
