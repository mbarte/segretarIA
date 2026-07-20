# SegretarIA

**Project Planning & Roadmap**

Versione: 0.3
Ultimo aggiornamento: 2026-07-20

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

Release 0.2: analisi delle email tramite LLM.

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
LLM Analysis
    ↓
EmailAnalysis
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
* [X] Dependency Injection

---

## Chat

* [X] Router
* [X] AssistantAgent
* [X] PromptBuilder
* [X] LLMService

---

## Email — Release 0.1

### Provider

* [X] EmailProvider
* [X] GraphEmailProvider
* [X] IMAPProvider
* [X] OAuth Device Flow
* [X] Polling Device Flow
* [X] Token cache persistente

### Persistenza

* [X] EmailModel
* [X] AttachmentModel
* [X] Mapper Domain ⇄ SQLAlchemy
* [X] EmailRepository

### Service

* [X] EmailService
* [X] EmailSyncResult
* [X] Deduplicazione tramite Message-ID

### Wiring

* [X] Dependency Injection EmailService
* [X] Endpoint sincronizzazione
* [X] Prima sincronizzazione reale
* [X] Logging sincronizzazione

### Output

* [X] Database popolato con le email

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

## Release 0.1 ✅

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

## Release 0.2 — In corso

Analisi delle email tramite LLM.

Funzionalità:

* AnalysisService
* AnalysisPromptBuilder
* EmailAnalysis domain model
* EmailAnalysisModel (tabella separata)
* EmailAnalysisRepository
* Endpoint di analisi

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
* EmailAttachment
* EmailAnalysis
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
├── summary
├── importance
├── category
├── tasks
└── deadlines
```

Campi futuri (release successive):

* tags
* contacts
* projects
* decisions
* reminders

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

## 2026-07-20

* Release 0.1 completata: prima sincronizzazione reale della mailbox
* EmailProvider usa Microsoft Graph con OAuth Device Flow
* Polling esplicito per autorizzazione device flow
* Token cache persistente in `/storage/msal_cache.bin`
* Database rinominato in `segretarIA.db`

## 2026-07

* focus iniziale esclusivamente sulle email;
* bootstrap iniziale tramite sincronizzazione temporale (`fetch_since`);
* sincronizzazione ordinaria tramite `fetch_unread`;
* deduplicazione tramite `Message-ID`;
* Domain Model separato dai Model SQLAlchemy;
* Repository Pattern adottato come unico punto di accesso ai dati.

---

# Backlog

## Completato ✅

* EmailRepository
* EmailService
* Persistenza
* Sync
* Deduplicazione
* Dependency Injection
* Endpoint sincronizzazione
* Logging
* Prima sincronizzazione reale

## Alta priorità — Release 0.2

* AnalysisService
* AnalysisPromptBuilder
* EmailAnalysis domain model
* EmailAnalysisModel
* EmailAnalysisRepository
* Endpoint analisi

## Media

* Task Extraction (strutturata)
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

Spazio dedicato a nuove idee e sperimentazioni, senza impattare la roadmap principale.
