# SegretarIA — Project State

Versione: 0.3
Ultimo aggiornamento: 2026-07-20

---

# Vision

SegretarIA è un assistente personale AI completamente locale il cui obiettivo è trasformare le comunicazioni (inizialmente le email) in conoscenza strutturata e azioni operative.

L'obiettivo finale è costruire un assistente capace di:

* leggere automaticamente le comunicazioni;
* comprendere cosa è importante;
* estrarre attività, decisioni e scadenze;
* mantenere una memoria persistente;
* organizzare il lavoro quotidiano;
* rispondere tramite chat in linguaggio naturale;
* operare completamente in locale tramite Docker e Ollama.

---

# Stato generale

La Release 0.1 è completa: la mailbox viene sincronizzata realmente, le email vengono salvate nel database con deduplicazione.

L'attenzione dello sviluppo è ora concentrata sulla Release 0.2:

* analisi delle email tramite LLM;
* estrazione di summary, importance, category, tasks, deadlines.

---

# Stack

## Backend

* Python
* FastAPI
* SQLAlchemy

## AI

* Ollama
* modello Llama per sviluppo CPU

## Database

* SQLite

## Deployment

Docker Compose

Container:

* API
* Ollama

---

# Architettura attuale

## Chat

```text
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

## Email

```text
Graph / IMAP
    ↓
EmailProvider
    ↓
EmailService
    ↓
EmailRepository
    ↓
SQLite
```

---

# Struttura del progetto

```text
app/
├── agents/
├── api/
│   └── routes/
│       ├── chat.py
│       └── email.py
├── core/
│   ├── config.py
│   ├── dependencies.py
│   └── logging.py
├── database/
│   ├── engine.py
│   ├── models.py
│   └── mappers.py
├── domain/
│   ├── email.py
│   └── task.py
├── models/
│   ├── chat.py
│   └── agent.py
├── prompts/
│   ├── system.py
│   └── builder.py
├── providers/
│   ├── auth/
│   │   ├── base.py
│   │   ├── microsoft.py
│   │   ├── models.py
│   │   └── token_cache.py
│   ├── base.py
│   ├── graph.py
│   └── imap.py
├── repositories/
│   └── email.py
├── services/
│   ├── llm.py
│   ├── database.py
│   └── email.py
├── tests/
├── tools/
└── main.py
```

---

# Componenti implementati

## Chat

* FastAPI Router
* PromptBuilder
* AssistantAgent
* LLMService

---

## Database

* SQLite
* SQLAlchemy
* DatabaseService
* Conversation
* EmailModel
* AttachmentModel

---

## Domain

Le entità di dominio sono implementate tramite dataclass.

Attualmente:

* Email
* EmailAttachment
* Task (base)

Il dominio rimane completamente indipendente dall'infrastruttura.

---

## Repository

Implementati:

* EmailRepository
* Mapper Domain ⇄ SQLAlchemy

Responsabilità:

* persistenza;
* recupero;
* deduplicazione tramite Message-ID.

---

## Email

Implementato il Provider Pattern.

```text
EmailProvider
├── GraphEmailProvider
└── IMAPProvider
```

Entrambi restituiscono esclusivamente oggetti `Email`.

Il resto dell'applicazione non conosce il protocollo utilizzato.

---

## EmailService

Implementato.

Responsabilità:

* bootstrap iniziale;
* sincronizzazione incrementale;
* deduplicazione;
* orchestrazione del flusso email.

Espone due modalità operative:

* `initialize()` — prima esecuzione, recupero email degli ultimi mesi
* `sync()` — esecuzioni successive, solo email non lette

---

## Autenticazione

Implementata un'astrazione `AuthenticationProvider`.

Attualmente disponibile:

* MicrosoftAuthenticator

basato su:

* MSAL
* OAuth2 Device Flow
* Polling esplicito per autorizzazione
* Token cache persistente in `/storage/msal_cache.bin`

---

## Microsoft Graph

Supportato.

Implementato:

* OAuth Device Flow con polling
* Token cache persistente
* Lettura delle email
* Mapping verso Email
* Recupero email non lette (`fetch_unread`)
* Recupero email da una data (`fetch_since`)

---

## IMAP

Supportato.

Implementato:

* connessione IMAP;
* OAuth2 XOAUTH2;
* parsing MIME;
* mapping Email;
* recupero email non lette;
* recupero email da una data (`fetch_since`).

Per account Exchange moderni il provider consigliato rimane Microsoft Graph.

---

## Dependency Injection

Gestita tramite `@lru_cache` e factory functions in `core/dependencies.py`.

Servizi principali creati come singleton:

* `get_llm_service()`
* `get_prompt_builder()`
* `get_assistant_agent()`
* `get_database_service()`
* `get_email_repository()`
* `get_email_provider()`
* `get_email_service()`

---

## Endpoint

| Endpoint | Metodo | Descrizione |
|---|---|---|
| `POST /api/chat` | POST | Chat con l'assistente |
| `POST /api/email/initialize` | POST | Prima sincronizzazione |
| `POST /api/email/sync` | POST | Sync incrementale |
| `GET /` | GET | Health check base |
| `GET /api/health` | GET | Health check dettagliato |

---

# Decisioni architetturali

## Domain indipendente

Il dominio non conosce:

* FastAPI;
* SQLAlchemy;
* Graph;
* IMAP.

Lavora esclusivamente con dataclass.

---

## Repository Pattern

L'accesso al database avviene esclusivamente tramite Repository.

I Service non utilizzano direttamente SQLAlchemy.

---

## Service Layer

Ogni servizio ha una sola responsabilità.

Attualmente:

* LLMService → comunicazione con Ollama;
* EmailService → logica applicativa delle email;
* DatabaseService → gestione delle sessioni SQLAlchemy.

---

## Provider Pattern

Ogni sorgente implementa `EmailProvider`.

Questo rende semplice aggiungere in futuro:

* Gmail API;
* filesystem;
* provider personalizzati.

---

## Bootstrap della mailbox

Alla prima esecuzione:

* recupero delle email degli ultimi mesi (`fetch_since`).

Nelle sincronizzazioni successive:

* recupero esclusivamente delle email non lette (`fetch_unread`).

---

## Database

SQLite rimane il database principale.

Conterrà progressivamente:

* email;
* analisi email;
* task;
* decisioni;
* promemoria;
* memoria persistente.

---

## Vector Database

Previsto nelle release successive.

Qdrant conterrà esclusivamente:

* embeddings;
* ricerca semantica;
* supporto RAG.

---

# Testing

Attualmente sono disponibili test per:

* Repository;
* Mapper;
* EmailService.

È prevista la migrazione completa a `pytest` con database dedicato ai test.

---

# Prossimi step

Ordine previsto:

1. ~~Dependency Injection di EmailService~~ ✅
2. ~~Endpoint di sincronizzazione~~ ✅
3. ~~Prima sincronizzazione reale della mailbox~~ ✅
4. Analisi delle email tramite LLM (Release 0.2)
5. TaskRepository
6. Generazione automatica di TODO.md
7. Report giornalieri
8. Memoria persistente
9. RAG
10. Tool Calling

---

# Stato della roadmap

## Completato

### Infrastruttura

* Docker
* FastAPI
* Ollama
* SQLite
* SQLAlchemy
* Dependency Injection di base

### Chat

* Router
* PromptBuilder
* AssistantAgent
* LLMService

### Email

* EmailProvider
* GraphEmailProvider
* IMAPProvider
* Microsoft OAuth Device Flow
* Token cache persistente
* EmailModel
* AttachmentModel
* Mapper
* EmailRepository
* EmailService
* Deduplicazione tramite Message-ID
* DI EmailService / EmailRepository
* Endpoint sincronizzazione (`/api/email/initialize`, `/api/email/sync`)
* Logging sincronizzazione
* Polling Device Flow

### Release 0.1

* Prima sincronizzazione reale della mailbox ✅

## In corso

* Analisi delle email tramite LLM (Release 0.2)

## Pianificato

* Task Management
* Report automatici
* Memoria persistente
* RAG
* Tool Calling
* Assistente personale autonomo
