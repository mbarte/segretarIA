# SegretarIA — Project State

Version: MVP Architecture v2

---

# Vision

SegretarIA è un assistente personale completamente locale il cui obiettivo è trasformare le comunicazioni (inizialmente email) in conoscenza strutturata e azioni operative.

L'obiettivo non è semplicemente interrogare un LLM, ma costruire un vero "segretario digitale" capace di:

- leggere automaticamente le comunicazioni;
- comprendere cosa è importante;
- ricordare ciò che serve nel tempo;
- organizzare attività e scadenze;
- mantenere una memoria persistente;
- permettere interrogazioni in linguaggio naturale.

L'intero sistema deve poter funzionare localmente tramite Docker, mantenendo il pieno controllo dei dati.

---

# MVP attuale

L'obiettivo del primo MVP è:

```
Email

↓

Parsing

↓

LLM

↓

Task estratti

↓

SQLite

↓

Markdown Reports

↓

Chat
```

Ovvero:

- leggere realmente una casella email;
- salvare le email nel database;
- estrarre attività;
- produrre TODO e report;
- permettere interrogazioni tramite chat.

---

# Obiettivi futuri

Successivamente il progetto evolverà verso:

- memoria persistente avanzata;
- RAG tramite Qdrant;
- classificazione automatica;
- gestione clienti;
- calendario;
- filesystem;
- tool calling;
- scheduler automatico;
- assistente realmente autonomo.

---

# Stack

## Backend

- Python
- FastAPI
- SQLAlchemy

## AI

- Ollama
- Llama (CPU)

## Database

SQLite

## Deployment

Docker Compose

Container:

- API
- Ollama

---

# Architettura

Attualmente il flusso della chat è:

```
HTTP Request

↓

FastAPI Router

↓

AssistantAgent

↓

PromptBuilder

↓

LLMService

↓

Ollama

↓

Response
```

Il flusso email è invece in costruzione:

```
Email Provider

↓

EmailService

↓

SQLite

↓

LLM

↓

Task Extraction

↓

Markdown Reports
```

---

# Architettura generale prevista

```
                AssistantAgent
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     LLMService   EmailService   MemoryService
        │              │              │
        │        EmailProvider        │
        │         ┌──────────┐        │
        │         │          │        │
        │      IMAP      Microsoft Graph
        │
     Ollama
```

---

# Struttura del progetto

```
app/

├── agents/
│
├── api/
│
├── core/
│
├── database/
│
├── domain/
│
├── models/
│
├── prompts/
│
├── providers/
│   ├── auth/
│   ├── base.py
│   ├── graph.py
│   └── imap.py
│
├── services/
│
├── tools/
│
└── main.py
```

---

# Stato dei componenti

## Chat

Completata.

Sono implementati:

- Router
- PromptBuilder
- AssistantAgent
- LLMService

Il sistema conversa correttamente con Ollama.

---

## Database

Completato.

SQLite inizializzato.

SQLAlchemy configurato.

---

## Domain Model

Il dominio utilizza dataclass.

Principali entità:

- Email
- Task

Le API continuano ad usare Pydantic.

---

# Email

È stato introdotto il concetto di EmailProvider.

```
EmailProvider

├── IMAPProvider

└── GraphEmailProvider
```

Entrambi restituiscono lo stesso modello Email.

Il resto dell'applicazione non conosce il protocollo utilizzato.

---

# Autenticazione

È stata introdotta un'astrazione AuthenticationProvider.

Attualmente è implementato:

```
MicrosoftAuthenticator
```

basato su:

- MSAL
- OAuth2 Device Flow

---

# Microsoft Graph

Supportato.

Implementato:

- OAuth Device Flow
- Token cache persistente
- Lettura email
- Mapping verso Email dataclass

Provider:

```
GraphEmailProvider
```

---

# IMAP

Supportato.

Implementato:

- connessione IMAP
- OAuth2 XOAUTH2
- parsing MIME
- mapping Email

Attualmente è mantenuto principalmente per compatibilità e per eventuali mailbox che espongono IMAP OAuth.

Per account Exchange moderni il provider consigliato è Microsoft Graph.

---

# Decisioni architetturali

## Domain indipendente

Il dominio non conosce:

- Graph
- IMAP
- HTTP

Riceve solamente oggetti Email.

---

## Provider Pattern

Ogni sorgente implementa EmailProvider.

Questo rende semplice aggiungere:

- Gmail API
- Exchange
- filesystem
- provider custom

---

## Authentication

Gli scope appartengono ai provider.

Esempio:

```
GraphEmailProvider

↓

Mail.Read
```

```
IMAPProvider

↓

IMAP.AccessAsUser.All
```

L'autenticatore rimane riutilizzabile.

---

## SQLite

Continua ad essere il database principale.

Conterrà:

- email
- task
- decisioni
- memoria

---

## Qdrant

Previsto successivamente.

Conterrà esclusivamente:

- embeddings
- ricerca semantica
- RAG

---

# Componenti completati

- Docker
- FastAPI
- Ollama
- Chat
- PromptBuilder
- AssistantAgent
- LLMService
- SQLite
- SQLAlchemy
- Dependency Injection
- EmailProvider
- IMAPProvider
- GraphEmailProvider
- Microsoft OAuth Device Flow

---

# Prossimo step

Implementare EmailService.

Responsabilità:

- usare EmailProvider;
- sincronizzare le email;
- evitare duplicati;
- salvare nel database;
- fornire le email agli altri servizi.

Flusso previsto:

```
Graph / IMAP

↓

EmailProvider

↓

EmailService

↓

SQLite
```

---

# Roadmap immediata

1. EmailService
2. Persistenza email su SQLite
3. Gestione UID / Message-ID
4. Task Extraction tramite LLM
5. TaskService
6. Generazione TODO.md
7. Report giornaliero
8. Memoria persistente
9. RAG
10. Tool Calling

---

# Stato del progetto

Il progetto ha ormai completato tutta l'infrastruttura di base.

La parte rimanente riguarda principalmente la logica applicativa:

- acquisizione delle email;
- persistenza;
- estrazione della conoscenza;
- orchestrazione dei servizi.

Da questo punto in avanti lo sviluppo sarà focalizzato sulla costruzione del vero assistente personale piuttosto che sull'infrastruttura tecnic

# SegretarIA — Project State

## Obiettivo

Costruire un assistente AI locale che:

* legge email tramite IMAP;
* identifica comunicazioni importanti;
* estrae attività, scadenze e decisioni;
* aggiorna file Markdown (TODO, report settimanali, memoria);
* mantiene memoria persistente;
* permette interrogazioni tramite chat;
* rimane completamente locale tramite Docker + Ollama.

Obiettivo MVP:
ottenere entro pochi giorni un sistema che ogni mattina possa analizzare le email e produrre un riepilogo operativo.

---

# Stack

## Backend

* Python
* FastAPI
* Uvicorn

## AI

* Ollama in container Docker
* Modello iniziale: llama leggero per sviluppo locale CPU

## Database

* SQLite
* SQLAlchemy

## Deployment

* Docker Compose

Container attuali:

* API FastAPI
* Ollama

Configurazione porte:

* FastAPI: 5000
* Ollama container: 1435 (per evitare conflitto con Ollama locale)

---

# Architettura attuale

Flusso:

```
HTTP Request

    ↓

FastAPI Router

    ↓

AssistantAgent

    ↓

PromptBuilder

    ↓

LLMService

    ↓

Ollama

    ↓

AgentResponse
```

---

# Struttura progetto attuale

```
app/

├── agents/
│   └── assistant.py
│
├── api/
│   ├── router.py
│   └── routes/
│       └── chat.py
│
├── core/
│   ├── config.py
│   ├── dependencies.py
│   └── logging.py
│
├── database/
│   ├── engine.py
│   └── models.py
│
├── domain/
│   ├── email.py
│   └── task.py
│
├── models/
│   ├── chat.py
│   └── agent.py
│
├── prompts/
│   ├── system.py
│   └── builder.py
│
├── services/
│   ├── llm.py
│   └── database.py
│
├── tools/
│   └── base.py
│
└── main.py
```

---

# Componenti completati

## Docker

Funzionante.

Volume persistenti configurati.

---

## FastAPI

Funzionante.

Endpoint:

```
POST /api/chat
```

---

## Ollama

Funzionante.

Risponde correttamente tramite FastAPI.

---

## LLMService

Responsabilità:

* comunicare con Ollama;
* ricevere una lista di messaggi;
* restituire la risposta del modello.

---

## AssistantAgent

Responsabilità:

* orchestrare il flusso;
* utilizzare PromptBuilder;
* chiamare LLMService.

---

## PromptBuilder

Responsabilità:

* costruire il prompt;
* separare system prompt e user message.

---

## Dependency Injection

Gestita tramite FastAPI Depends e lru_cache.

Servizi principali creati una sola volta.

---

## Database

SQLite inizializzato.

Database:

```
secretary.db
```

creato correttamente.

SQLAlchemy configurato.

---

# Decisioni architetturali

## Domain model

Gli oggetti interni saranno modellati con dataclass.

Esempi:

```
Email
Task
Document
Customer
```

Pydantic sarà usato principalmente per API e validazione esterna.

---

## ID database

Scelta attuale:

INTEGER PRIMARY KEY

Motivazione:

* applicazione personale;
* database locale;
* semplicità.

UUID eventualmente in futuro se servirà sincronizzazione.

---

## Embedding

Previsti ma non ancora implementati.

Decisione:

* SQLite per dati strutturati;
* Qdrant futuro per vector storage.

Architettura prevista:

```
SQLite

- email
- task
- clienti
- decisioni


Qdrant

- embeddings
- ricerca semantica
- RAG
```

---

# Componenti ancora da implementare

## Priorità alta

## EmailService

Obiettivo:

```
IMAP

↓

Email dataclass

↓

Email importanti

↓

LLM

↓

Task estratti

↓

TODO.md
```

---

## Parsing email

Da implementare:

* mittente;
* oggetto;
* corpo;
* allegati;
* UID;
* data;
* stato letto/non letto.

---

## Task extraction

Il modello dovrà estrarre:

* attività;
* priorità;
* scadenze;
* persone coinvolte.

---

## Report generator

Output:

```
TODO.md

REPORT_SETTIMANA.md

MEMORIA.md
```

---

# Funzionalità future

* memoria persistente avanzata;
* Qdrant;
* RAG;
* classificazione automatica email;
* gestione cartelle email;
* filesystem tool;
* calendario;
* gestione clienti/progetti;
* scheduler giornaliero;
* tool calling.

---

# Prossimo step

Implementare EmailService.

Prima progettare:

* interfaccia EmailProvider;
* modello Email;
* provider IMAP;
* gestione UID per evitare di rileggere email già processate.

Obiettivo:

leggere realmente la casella email e alimentare l'agente.
