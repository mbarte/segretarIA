# Configurazione Microsoft Entra (OAuth2 Outlook)

Per consentire al Local AI Secretary di leggere le email Outlook tramite IMAP è necessario registrare un'applicazione in Microsoft Entra.

Questa operazione è richiesta una sola volta.

---

## 1. Creare un account Azure

Se non si dispone già di un tenant Microsoft Entra:

1. Creare un account Azure gratuito.
2. Accedere al portale Microsoft Entra.
3. Verificare di avere un tenant Microsoft Entra disponibile.

---

## 2. Registrare una nuova applicazione

Aprire:

```
Microsoft Entra
→ App registrations
→ New registration
```

Configurare:

| Campo                   | Valore                                                                   |
| ----------------------- | ------------------------------------------------------------------------ |
| Name                    | Local AI Secretary                                                       |
| Supported account types | Accounts in any organizational directory and personal Microsoft accounts |

Lasciare vuota la Redirect URI e completare la registrazione.

---

## 3. Recuperare gli identificativi

Nella pagina **Overview** dell'applicazione annotare:

- Application (client) ID
- Directory (tenant) ID

Questi valori dovranno essere inseriti nel file `.env`.

---

## 4. Configurare l'autenticazione

Aprire:

```
Authentication
```

Selezionare:

```
Add a platform

↓

Mobile and desktop applications
```

Aggiungere la seguente Redirect URI:

```
http://localhost
```

Abilitare inoltre:

```
Allow public client flows

YES
```

Non è necessario creare un Client Secret.

L'applicazione utilizza il flusso OAuth2 Authorization Code con PKCE, progettato per applicazioni desktop e locali.

---

## 5. Configurare i permessi Microsoft Graph

Aprire:

```
API permissions
```

Aggiungere le seguenti **Delegated permissions**:

```
offline_access
openid
profile
email
IMAP.AccessAsUser.All
```

Se disponibile, concedere anche il consenso amministrativo:

```
Grant admin consent
```

---

## 6. Configurare il file `.env`

```env
EMAIL_PROVIDER=imap

IMAP_SERVER=outlook.office365.com
IMAP_PORT=993

EMAIL_ADDRESS=your_email@outlook.com

AZURE_CLIENT_ID=<Application Client ID>
AZURE_TENANT_ID=<Directory Tenant ID>

OAUTH_REDIRECT_URI=http://localhost
```

Non è richiesto alcun `CLIENT_SECRET`.

---

## 7. Primo accesso

Al primo avvio dell'applicazione verrà aperto automaticamente il browser per effettuare il login Microsoft.

Dopo l'autenticazione:

- verrà richiesto il consenso ai permessi IMAP;
- verrà salvato localmente un Refresh Token;
- i successivi avvii utilizzeranno automaticamente il Refresh Token per ottenere nuovi Access Token senza richiedere ulteriori login.

---

## Sicurezza

Il progetto utilizza OAuth2 Authorization Code con PKCE.

Questo approccio:

- non richiede Client Secret;
- evita di salvare la password dell'account Microsoft;
- consente il rinnovo automatico dei token;
- segue le linee guida Microsoft per applicazioni deskto


Configurazione Microsoft Entra (Outlook OAuth2)

Per consentire all'applicazione di accedere alle email tramite IMAP utilizzando OAuth2, è necessario registrare un'applicazione in Microsoft Entra.

1. Creare un account Azure

Se non si dispone già di un tenant Microsoft Entra:

Creare un account Azure gratuito.
Accedere al portale Microsoft Entra.
Verificare di avere un tenant Microsoft Entra disponibile.
2. Registrare una nuova applicazione

Aprire:

Microsoft Entra
→ App registrations
→ New registration

Compilare:

Name:
Local AI Secretary

Supported account types:
Accounts in any organizational directory and personal Microsoft accounts

Lasciare vuota la Redirect URI per il momento e completare la registrazione.

3. Annotare gli identificativi

Nella pagina Overview dell'applicazione annotare:

Application (client) ID

Directory (tenant) ID

Questi valori dovranno essere inseriti nel file .env.

4. Configurare l'autenticazione

Aprire:

Authentication

Selezionare:

Add a platform

↓

Mobile and desktop applications

Aggiungere la Redirect URI:

http://localhost

Abilitare inoltre:

Allow public client flows

YES

Non è necessario creare un Client Secret.

L'applicazione utilizza il flusso OAuth2 Authorization Code con PKCE, pensato per applicazioni desktop e locali.

5. Configurare i permessi Microsoft Graph

Aprire:

API permissions

Aggiungere le seguenti Delegated permissions di Microsoft Graph:

offline_access
openid
profile
email
IMAP.AccessAsUser.All

Se disponibile, concedere anche il consenso amministrativo:

Grant admin consent
6. Configurare il file .env

Inserire:

EMAIL_PROVIDER=imap

IMAP_SERVER=outlook.office365.com
IMAP_PORT=993

EMAIL_ADDRESS=your_email@outlook.com

AZURE_CLIENT_ID=<Application Client ID></application>
AZURE_TENANT_ID=<Directory Tenant ID></directory>

OAUTH_REDIRECT_URI=http://localhost

Non è richiesto alcun CLIENT_SECRET.

7. Primo accesso

Al primo avvio dell'applicazione verrà aperto automaticamente il browser per effettuare il login Microsoft.

Dopo l'autenticazione:

verrà richiesto il consenso ai permessi IMAP;
verrà salvato localmente un Refresh Token;
i successivi avvii utilizzeranno automaticamente il Refresh Token per ottenere nuovi Access Token senza richiedere ulteriori login.
Sicurezza

Il progetto utilizza OAuth2 Authorization Code con PKCE.

Questo approccio:

non richiede Client Secret;
evita di salvare la password dell'account Microsoft;
consente il rinnovo automatico dei token;
segue le linee guida Microsoft per applicazioni desktop.
