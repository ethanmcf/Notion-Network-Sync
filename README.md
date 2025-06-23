# 🧠 Notion Network Sync

A **monorepo Python system** that containerizes two independent services — a **LinkedIn Scraper** and a **Notion Poller** — built for syncing LinkedIn messages into a Notion database and enriching them using **OpenAI’s GPT API**.

This system is designed to be **automated and scalable**, leveraging:

- 🐳 Docker for containerization
- ⏱️ Kubernetes CronJobs for scheduled execution
- 🧩 SQLite for lightweight internal state tracking
- 🗃️ Notion API to manage contacts and notes
- 🧭 LinkedIn (via [Playwright](https://playwright.dev/)) to scrape recent communications
- 🤖 OpenAI GPT API for natural language formatting and enrichment

---

## 🔧 Services Overview

### 1. `linkedin_scraper`

Scrapes recent LinkedIn messages and updates the corresponding Notion contact pages with up-to-date info.

- ✅ Keeps unread messages as unread
- ⏱️ Runs on a schedule via Kubernetes CronJob
- 📝 Parses messages and detects relevant context
- ✍️ Writes raw notes into the Notion page _(Coming soon)_

### 2. `notion_poller`

Polls the Notion database for pages that have unformatted notes in the **"Formatted Notes"** section and sends them to the GPT API for enrichment.

- 🔎 Detects changes using last modified timestamps
- 🧩 Uses SQLite to track the last sync time per page
- 🪄 Updates the **"Formatted Notes"** section of each Notion page

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/notion-network-sync.git
cd notion-network-sync
```

## 2. Set Up the Notion Database

Create a database in Notion to store your contacts and notes.

Include at **minimum** the following properties:

- `Name` (Title)
- `Company` (Rich Text)
- `Communicated On` (Multi-select)
- `Last Communicated` (Date)

---

## 3. Create a `.env` File

In the root of your project, create a `.env` file with the following keys:

```env
# Notion
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id

# LinkedIn credentials
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password

# OpenAI GPT
GITHUB_TOKEN=your_key
AZURE_OPENAI_ENDPOINT="https://models.github.ai/inference"
```

### 4. Build and Run Locally with Docker Compose

#### LinkedIn Scraper

```bash
docker compose build linkedin-scraper
docker compose run --rm linkedin-scraper
```

### Notion Poller

```
docker compose build notion-poller
docker compose run --rm notion-poller
```
