
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
