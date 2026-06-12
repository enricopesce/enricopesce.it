---
title: Autenticazione SAML su OpenVPN con domini OCI IAM Identity
description: "Guida per integrare l'autenticazione SAML nel tuo server OpenVPN usando OCI IAM Identity Domains."
date: 2023-01-20T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  image: static/one.webp
  alt: Domini IAM Identity
  caption: Domini IAM Identity
keywords:
- "oci iam identity domains"
- "autenticazione saml"
- "openvpn mfa"
- "oracle cloud sso"
tags:
- "OCI"
- "IAM"
- "SAML"
- "OpenVPN"
- "Sicurezza"
categories:
- "Identita e Sicurezza"
faq:
  - question: "Cos'è OCI IAM Identity Domains?"
    answer: "OCI IAM Identity Domains è il servizio di gestione delle identità enterprise di Oracle Cloud Infrastructure. Gestisce il ciclo di vita degli utenti, il single sign-on (SSO), l'autenticazione multi-fattore e l'integrazione con provider di identità esterni tramite SAML 2.0 o OIDC."
  - question: "Posso usare SAML per aggiungere MFA a OpenVPN su Oracle Cloud?"
    answer: "Sì. Puoi configurare OpenVPN per delegare l'autenticazione a OCI IAM Identity Domains via SAML 2.0. Gli utenti si autenticano tramite il portale Identity Domain, che può applicare policy MFA prima di concedere l'accesso VPN."
  - question: "OCI IAM Identity Domains è disponibile nel Free Tier?"
    answer: "OCI IAM Identity Domains è incluso senza costi in tutte le tenancy OCI per le funzionalità di gestione identità di base. Il Free Tier include fino a 2 Identity Domain con SSO e MFA."
---

La gestione di identita' e accessi e' un obiettivo cruciale in un'organizzazione che cresce.

Oltre alla necessita' di semplificare la gestione degli utenti e migliorare la sicurezza, l'integrazione con servizi esterni diventa sempre piu' rilevante.

Oracle OCI offre un servizio completo per gestire identita' e accesso chiamato [IAM with Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm).

Nel dettaglio:

> Un identity domain e' un contenitore per gestire utenti e ruoli, federare e fare provisioning degli utenti, integrare applicazioni tramite Oracle Single Sign-On (SSO) e amministrare provider SAML/OAuth. Rappresenta una popolazione di utenti in Oracle Cloud Infrastructure e le relative impostazioni di sicurezza, come MFA.

In questo post vediamo come integrare l'autenticazione con MFA di OpenVPN Access Server usando un dominio OCI IAM Identity.

Per ridurre la complessita' dello scenario, utenti e password sono creati direttamente in un nuovo dominio IAM separato, senza integrazione con directory esterne.

Partiamo da un'istanza gia' creata per l'appliance OpenVPN sul servizio [OCI Compute](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm).

Il primo passaggio e' creare il dominio nel servizio IAM dal menu **Identity & Security -> Domains**.

In questo scenario non dobbiamo sincronizzare utenti da una directory esterna, come AD o LDAP, e il tipo gratuito e' sufficiente. In un workload aziendale reale e' invece consigliato il dominio Oracle App Premium.

![Tipi di dominio IAM Identity](static/one.webp "Tipi di dominio IAM Identity")

Segui i form e inserisci i dettagli dell'account principale. Dopo pochi secondi la directory viene creata con il tuo utente come primo utente.

Ora devi recuperare alcuni dati dalla console amministrativa di OpenVPN e salvarli.

Salva **SP Identity** e **SP ACS** dalla sezione SAML della console web amministrativa di OpenVPN.

![SP Identity e ACS](static/two.webp "SP Identity e ACS")

Copia anche il certificato SP in un file locale chiamato _certificate.pem_ dalla stessa pagina.

![Certificato SP](static/three.webp "Certificato SP")

Per integrare OpenVPN Access Server dobbiamo aggiungere una nuova applicazione nel dominio.

![Nuova applicazione](static/four.webp "Nuova applicazione")

Scegli l'applicazione SAML:

![Applicazione](static/five.webp "Applicazione")

Inserisci il nome e, opzionalmente, un'icona personalizzata. Premi **Next**; le altre opzioni sono facoltative.

![Aggiunta di una applicazione SAML](static/six.webp "Aggiunta di una applicazione SAML")

Inserisci _Entity ID_ e _Assertion Consumer URL_, carica il file _certificate.pem_ salvato prima e premi **Finish**.

![Configurazione dell'applicazione SAML](static/seven.webp "Configurazione dell'applicazione SAML")

Scarica il file dei metadati IdP dal pulsante del dominio IAM Identity.

![Download dei metadati IdP](static/eight.webp "Download dei metadati IdP")

Carica il file dei metadati scaricato dal dominio IAM Identity nella sezione IdP della pagina SAML di OpenVPN.

![Import del file metadati IdP](static/eight.webp "Import del file metadati IdP")

La configurazione SAML e' completa.

Attiva l'autenticazione SAML nella sezione OpenVPN per abilitarla.

Ora puoi provare l'autenticazione SAML dalla pagina web di OpenVPN.
