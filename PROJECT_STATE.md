
# Local AI Secretary — Project State

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
