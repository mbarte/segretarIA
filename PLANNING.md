# SegretarIA

**Project Planning & Roadmap**

Versione: 0.2
Ultimo aggiornamento: 2026-07-17

---

# Vision

SegretarIA è un assistente personale AI completamente locale.

L'obiettivo finale è costruire un agente capace di:

* leggere email;
* comprendere comunicazioni;
* estrarre conoscenza;
* ricordare informazioni importanti;
* organizzare attività;
* produrre report;
* rispondere in linguaggio naturale;
* utilizzare strumenti (tool);
* diventare un assistente personale autonomo.

Il progetto segue una filosofia incrementalista:

> Ogni release deve essere realmente utilizzabile.

---

# Filosofia del progetto

Principi fondamentali:

* semplicità prima della complessità;
* responsabilità singola per ogni componente;
* dominio indipendente dall'infrastruttura;
* codice facilmente estendibile;
* preferire composizione ad accoppiamento;
* imparare costruendo un progetto reale.

---

# Obiettivo attuale

Realizzare una **Release 0.1 realmente utilizzabile**, in grado di sincronizzare una casella email e costruire la memoria locale del sistema.

Pipeline attuale:

```
Email Provider

↓

EmailService

↓

EmailRepository

↓

SQLite

↓

LLM

↓

Task Extraction

↓

Markdown Reports

↓

Chat
```

---

# Stato del progetto

## Infrastruttura

* [X] Docker
* [X] FastAPI
* [X] Ollama
* [X] SQLite
* [X] SQLAlchemy
* [X] Dependency Injection base

---

## Chat

* [X] Router
* [X] AssistantAgent
* [X] PromptBuilder
* [X] LLMService

---

## Email

### Provider

* [X] EmailProvider
* [X] GraphEmailProvider
* [X] IMAPProvider
* [X] OAuth Device Flow

### Persistenza

* [X] EmailModel
* [X] AttachmentModel
* [X] Mapper Domain ⇄ SQLAlchemy
* [X] EmailRepository
* [X] EmailService
* [X] EmailSyncResult
* [X] Gestione duplicati tramite Message-ID

### Da completare

* [ ] Dependency Injection EmailService
* [ ] Endpoint sincronizzazione
* [ ] Prima sincronizzazione reale
* [ ] Logging sincronizzazione

---

# Bootstrap iniziale

Prima esecuzione:

* Inbox
* email degli ultimi mesi (configurabile)

Esecuzioni successive:

* sincronizzazione incrementale
* recupero delle email non lette

Questo riduce drasticamente il tempo della prima sincronizzazione e rende il sistema facilmente estendibile.

---

# Roadmap

## Release 0.1

Obiettivo:

Prima sincronizzazione reale della mailbox.

Funzionalità:

* EmailService
* Repository
* Persistenza SQLite
* Deduplicazione
* Endpoint di sincronizzazione
* Prima sincronizzazione reale

Output:

Database popolato con le email.

---

## Release 0.2

Analisi delle email tramite LLM.

Output:

Per ogni email:

* summary
* importance
* category
* tasks
* deadlines

---

## Release 0.3

Generazione documentazione operativa.

Output:

* TODO.md
* TODAY.md
* REPORT.md

---

## Release 0.4

Task Management.

Introduzione di:

* TaskRepository
* TaskService
* aggiornamento automatico dei task

---

## Release 0.5

Chat contestuale.

L'utente potrà chiedere:

* cosa devo fare?
* quali email importanti?
* cosa è cambiato oggi?
* quali attività sono in ritardo?

---

## Release 0.6

Memoria persistente.

Introduzione di:

* MemoryService
* DecisionRepository
* ReminderRepository

---

## Release 0.7

RAG.

Introduzione di:

* embeddings
* Qdrant
* ricerca semantica

---

## Release 0.8

Calendario.

---

## Release 0.9

Filesystem.

---

## Release 1.0

Tool Calling.

---

## Release 1.1

Scheduler.

---

## Release 1.2

Assistente autonomo.

---

# Dominio

Entità previste:

* Email
* Attachment
* Task
* Decision
* Reminder
* Contact
* Project

Le entità di dominio rimangono completamente indipendenti da:

* SQLAlchemy
* Graph
* IMAP
* FastAPI

---

# Tassonomia delle email

Categorie previste:

## Operative

* task
* richieste
* approvazioni

## Informative

* newsletter
* report
* comunicazioni

## Commerciali

* clienti
* offerte
* ordini

## Personali

* banca
* assicurazione
* sanità

## Eventi

* meeting
* appuntamenti

## Amministrative

* fatture
* ricevute
* pagamenti

L'assegnazione sarà effettuata automaticamente dall'LLM.

---

# Modello di analisi

```
EmailAnalysis

summary
importance
category
tags
tasks
deadlines
contacts
projects
decisions
reminders
```

Nelle prime release verranno implementati solamente:

* summary
* importance
* category
* tasks

Gli altri campi saranno aggiunti progressivamente.

---

# Regole architetturali

* un servizio = una responsabilità;
* un repository = accesso esclusivo al database;
* EmailService è l'unico punto di accesso agli EmailProvider;
* nessun componente del dominio dipende dall'infrastruttura;
* AssistantAgent orchestra ma non implementa logica di business;
* PromptBuilder costruisce esclusivamente il prompt.

---

# Workflow di sviluppo

Ogni nuova funzionalità seguirà questo ordine:

1. Domain
2. SQLAlchemy Model
3. Mapper
4. Repository
5. Service
6. Dependency Injection
7. Endpoint/API
8. Test
9. Integrazione con l'Agent

---

# Testing

Attualmente:

* test repository
* test mapper
* test EmailService

Roadmap:

* migrazione completa a pytest;
* fixture per database dedicato;
* fake provider;
* integration test;
* end-to-end test.

---

# Decision Log

## 2026-07

Decisioni principali:

* focus iniziale esclusivamente sulle email;
* bootstrap iniziale tramite sincronizzazione temporale (`fetch_since`);
* sincronizzazione ordinaria tramite `fetch_unread`;
* deduplicazione tramite `Message-ID`;
* Domain Model separato dai Model SQLAlchemy;
* Repository Pattern adottato come unico punto di accesso ai dati.

---

# Backlog

## Alta priorità

* Dependency Injection EmailService
* Endpoint sincronizzazione
* Prima sincronizzazione reale
* Logging

## Media

* Task Extraction
* TaskRepository
* TODO.md
* Report

## Bassa

* MemoryService
* Qdrant
* Tool Calling
* Scheduler
* Calendario

---

# Idee future

Spazio dedicato a nuove idee e sperimentazioni, senza impattare la roadmap principal

# SegretarIA

**Project Planning & Roadmap**

Versione: 0.1
Ultimo aggiornamento: YYYY-MM-DD

---

# Vision

SegretarIA è un assistente personale AI completamente locale.

L'obiettivo finale è costruire un agente in grado di:

- leggere email;
- comprendere comunicazioni;
- estrarre conoscenza;
- ricordare informazioni importanti;
- organizzare attività;
- produrre report;
- rispondere in linguaggio naturale;
- utilizzare strumenti (tool);
- diventare un assistente personale autonomo.

Il progetto è sviluppato con una filosofia incrementalista:

> Ogni release deve essere realmente utilizzabile.

---

# Filosofia del progetto

Principi fondamentali.

- semplicità prima della complessità;
- ogni componente deve avere una responsabilità chiara;
- dominio indipendente dall'infrastruttura;
- codice facilmente estendibile;
- evitare framework pesanti quando possibile;
- imparare costruendo.

---

# MVP corrente

L'MVP è focalizzato esclusivamente sulla gestione delle email.

Obiettivo:

```
Email

↓

Database

↓

LLM

↓

Task

↓

Markdown

↓

Chat
```

Tutto il resto arriverà in release successive.

---

# Stato del progetto

## Infrastruttura

- [X] Docker
- [X] FastAPI
- [X] Ollama
- [X] SQLite
- [X] SQLAlchemy
- [X] Dependency Injection

---

## Chat

- [X] Router
- [X] AssistantAgent
- [X] PromptBuilder
- [X] LLMService

---

## Email

- [X] EmailProvider
- [X] IMAPProvider
- [X] GraphProvider
- [X] OAuth Device Flow

Da completare:

- [ ] EmailRepository
- [ ] EmailService
- [ ] Sync
- [ ] Deduplicazione
- [ ] Persistenza

---

# Architettura

```
AssistantAgent
        │
        ▼
EmailService
        │
        ▼
EmailRepository
        │
        ▼
SQLite
```

L'LLM non deve conoscere il database.

Il database non deve conoscere Ollama.

Il dominio non deve conoscere Graph o IMAP.

---

# Roadmap

## Release 0.2

### Obiettivo

Sincronizzare realmente una mailbox.

Funzionalità:

- sincronizzazione
- salvataggio
- deduplicazione
- logging

Output:

database popolato.

---

## Release 0.3

Analisi email.

Estrazione:

- summary
- importance
- category
- tasks
- deadlines

Salvataggio nel database.

---

## Release 0.4

Generazione report.

Output:

- TODO.md
- TODAY.md
- REPORT.md

---

## Release 0.5

Chat intelligente.

L'utente potrà chiedere:

- cosa devo fare?
- quali email importanti?
- quali scadenze?

---

## Release 0.6

Memoria persistente.

Introduzione MemoryService.

---

## Release 0.7

RAG.

Introduzione:

- embeddings
- Qdrant
- ricerca semantica

---

## Release 0.8

Calendario.

---

## Release 0.9

Filesystem.

---

## Release 1.0

Tool Calling.

---

## Release 1.1

Scheduler.

---

## Release 1.2

Assistente autonomo.

---

# Dominio

## Email

Responsabilità:

- rappresentare una comunicazione.

Non deve contenere logica.

---

## Task

Attività estratte dall'LLM.

---

## Decision

Decisioni prese durante una comunicazione.

---

## Reminder

Informazioni da ricordare.

---

## Contact

Persona coinvolta.

---

## Project

Progetto a cui appartiene una comunicazione.

---

# Tassonomia delle email

Ogni email potrà appartenere ad una categoria.

## Operative

- task
- richieste
- approvazioni

## Informative

- newsletter
- comunicazioni
- report

## Commerciali

- offerte
- clienti
- ordini

## Personali

- banca
- assicurazione
- sanità

## Eventi

- meeting
- appuntamenti

## Amministrative

- fatture
- ricevute
- pagamenti

Le categorie potranno essere assegnate automaticamente dall'LLM.

---

# Modello di analisi

Ogni email produrrà un oggetto strutturato.

```
EmailAnalysis

summary

importance

category

tags

tasks

deadlines

contacts

projects

decisions

reminders
```

Inizialmente verranno utilizzati solo:

- summary
- importance
- category
- tasks

Gli altri campi saranno implementati progressivamente.

---

# Regole architetturali

- un servizio = una responsabilità;
- niente accesso diretto al database fuori dai repository;
- niente chiamate dirette al provider fuori da EmailService;
- il dominio non dipende dall'infrastruttura;
- il PromptBuilder non contiene logica di business;
- AssistantAgent orchestra ma non implementa logica.

---

# Decision Log

## 2026-07

Scelta di mantenere il focus iniziale esclusivamente sulle email.

Motivazione:

- ottenere rapidamente una prima versione stabile;
- utilizzare realmente SegretarIA durante lo sviluppo;
- aggiungere le funzionalità avanzate solo successivamente.

---

# Backlog

## Alta priorità

- EmailRepository
- EmailService
- Persistenza
- Sync
- Deduplicazione

## Media

- Task Extraction
- TODO.md
- Report

## Bassa

- Memoria
- Qdrant
- Tool Calling
- Scheduler
- Calendario

---

# Idee future

(sezione libera)

Qui annoteremo qualsiasi idea senza impattare la roadmap.
