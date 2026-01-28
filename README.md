<a name="readme-top"></a>

<div align="center">
  <h1>Meilisearch Admin</h1>

  <p align="center">
    <b>English</b> | <a href="README_zh.md">简体中文</a>
  </p>

  <p>
    A modern web-based administration interface for Meilisearch instances
  </p>

  <p>
    <a href="https://github.com/itbaymax/meilisearch-admin/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/python-3.10+-green.svg" alt="Python" />
    </a>
    <a href="https://vuejs.org/">
      <img src="https://img.shields.io/badge/vue-3.x-brightgreen.svg" alt="Vue" />
    </a>
    <a href="https://www.meilisearch.com/">
      <img src="https://img.shields.io/badge/meilisearch-1.x-ff69b4.svg" alt="Meilisearch" />
    </a>
  </p>
</div>

## Table of Contents

- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Contributing](#contributing)

## About

**Meilisearch Admin** is a full-featured web administration panel for managing Meilisearch search engine instances. It provides a user-friendly interface to replace traditional curl commands and code-based configurations, making Meilisearch management accessible and efficient.

### Why Meilisearch Admin?

- **Visual Management**: Intuitive UI for managing indexes, documents, and settings
- **Multi-Instance Support**: Manage multiple Meilisearch instances from a single dashboard
- **Real-time Search Preview**: Test search queries with instant results
- **Complete Settings Control**: Configure all index settings through the interface
- **Task Monitoring**: Track indexing tasks and their status
- **API Key Management**: Securely manage API keys with visibility controls

## Features

| Module | Description |
|--------|-------------|
| **Project Management** | Add and manage multiple Meilisearch instances |
| **Index Management** | Create, configure, and delete indexes |
| **Document Operations** | Add, edit, delete, and search documents |
| **Settings Configuration** | Full control over index settings (attributes, ranking rules, synonyms, etc.) |
| **Task Monitoring** | View and manage indexing tasks |
| **API Key Control** | Create and manage API keys with fine-grained permissions |
| **Search Preview** | Real-time search testing with ranking scores |
| **Multi-language** | English and Chinese interface |
| **Theme Support** | Tech, Pink, Dark, and Light themes |

## Architecture

```
meilisearch-admin/
├── backend/                 # Python Flask API Server
│   ├── api/                 # RESTful API endpoints
│   ├── models/              # SQLAlchemy ORM models
│   ├── services/            # Meilisearch client service
│   └── utils/               # Utilities and helpers
├── frontend/                # Vue 3 + Vite Application
│   ├── src/
│   │   ├── api/             # HTTP client and API calls
│   │   ├── components/      # Reusable Vue components
│   │   ├── views/           # Page components
│   │   ├── store/           # Pinia state management
│   │   └── router/          # Vue Router configuration
│   └── dist/                # Production build output
├── config/                  # YAML configuration files
├── bin/                     # Startup scripts
├── data/                    # SQLite database storage
└── logs/                    # Application logs
```

### Tech Stack

**Backend:**
- Python 3.10+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- Meilisearch Python Client

**Frontend:**
- Vue 3 (Composition API)
- Vite (Build Tool)
- Pinia (State Management)
- Tailwind CSS (Styling)
- Vue Router

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- A running Meilisearch instance

### Installation

<details open>
<summary><b>Option 1: Local Development</b></summary>

<br/>

**1. Clone the repository**
```bash
git clone https://github.com/itbaymax/meilisearch-admin.git
cd meilisearch-admin
```

**2. Setup Python environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**3. Setup Frontend**
```bash
cd frontend
npm install
npm run build
cd ..
```

**4. Start the application**
```bash
# Start Frontend
cd frontend && npm run dev

# Start backend server
python -m backend.app

# Frontend: http://localhost:8080
# Backend API: http://localhost:5000
```

</details>

<details>
<summary><b>Option 2: Development Mode (Hot Reload)</b></summary>

<br/>

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Flask with debug mode
python -m backend.app
# Backend API: http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend Dev Server: http://localhost:8080
```

</details>

<details>
<summary><b>Option 3: Docker Deployment (Recommended for Production)</b></summary>

<br/>

**1. Deploy with docker-compose (One-Click)**
```bash
# Clone the repository
git clone https://github.com/itbaymax/meilisearch-admin.git
cd meilisearch-admin

# Build and start services
docker-compose up -d

# Access: http://localhost:8080
```

**2. Build with Docker manually**
```bash
# Build image
docker build -t meilisearch-admin:latest .

# Run container
docker run -d -p 8080:80 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config:ro \
  --name meilisearch-admin \
  meilisearch-admin:latest
```

**3. Container Management**
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Volume Mounts:**

| Mount Path | Description |
|------------|-------------|
| `./data:/app/data` | SQLite database persistence |
| `./logs:/app/logs` | Application logs persistence |
| `./config:/app/config:ro` | Configuration files (read-only) |

**Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `TZ` | Timezone | `Asia/Shanghai` |
| `FLASK_ENV` | Runtime environment | `production` |

</details>

### First Steps

1. Open `http://localhost:5000` in your browser
2. Click "Add Project" to register your Meilisearch instance
3. Enter the Meilisearch URL (e.g., `http://localhost:7700`) and API Key
4. Start managing your indexes!

## Screenshots

> Screenshots will be added here. The following sections are placeholders for future documentation.

![Home](docs/images/1-home-data.png)

### Project Dashboard

![Project Dashboard](docs/images/5-project-list.png)
*Main dashboard showing all registered Meilisearch instances with key metrics*

### Index Management

![Index Management](docs/images/11-indexs-settings-general.png) 
*Index list view with document counts, status, and quick actions*

### Index Settings

![Index Settings](docs/images/13-indexs-settings-attributes.png)
*Comprehensive settings panel with left sidebar navigation*

### Search Preview

![Search Preview](docs/images/8-project-search.png) 
*Real-time search testing with table/JSON view and ranking scores*

### Task Monitor

![Task Monitor](docs/images/7-project-tasks.png)
*Task list with status filtering and detailed information*

### API Keys

![API Keys](docs/images/9-project-apikeys.png)
*API key management with visibility toggle and permission control*

### Theme Support

![Themes-dark](docs/images/14-project-theme-dark.png)
![Themes-light](docs/images/15-project-theme-light.png)
*Multiple theme options: Tech, Pink, Dark, and Light*

### I18N

![ZH](docs/images/16-project-i18n.png)
*多语言切换：English、中文*

## Configuration

Configuration is managed via YAML files in the `config/` directory.

```yaml
# config/config.yaml
server:
  host: 0.0.0.0
  port: 5000
  debug: true

database:
  type: sqlite
  path: data/meilisearch_admin.db

logging:
  level: INFO
  path: logs/
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `DATABASE_URL` | Database connection string | SQLite |
| `LOG_LEVEL` | Logging level | `INFO` |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <a href="#readme-top">Back to Top</a>
</p>
