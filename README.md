# resonant

A full-stack web application that leverages FastAPI for the backend and Svelte for the frontend to provide factual, well-researched, and engaging explanations of famous artworks using AI-powered deep reasoning.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Backend Setup (FastAPI)](#backend-setup-fastapi)  
  - [Frontend Setup (Svelte)](#frontend-setup-svelte)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Acknowledgements](#acknowledgements)  

---

## Project Overview

This project offers an AI-powered art explainer that connects users with live, factual insights about famous paintings. The backend uses FastAPI to handle API requests and interface with AI models, while the frontend is built with Svelte to deliver a dynamic, responsive user experience.

---

## Features

- Fast and responsive API powered by FastAPI  
- Interactive, modern frontend built using Svelte  
- AI-generated explanations about artworks  
- Clean, modular codebase for both backend and frontend  
- Easy to extend with new features or artworks  

---

## Tech Stack

- **Backend:** FastAPI, Python 3.9+  
- **Frontend:** Svelte, JavaScript/TypeScript  
- **AI Integration:** Perplexity’s deep reasoning API
- **Others:** Uvicorn (ASGI server), Axios or Fetch for API calls  

---

## Getting Started

### Prerequisites

- Python 3.9 or later  
- Node.js 14+ and npm or yarn  
- Git  

### Clone the Repository

```
git clone https://github.com/yourusername/ai-art-explainer.git
cd ai-art-explainer
```

resonant/ \
├── backend/               # FastAPI backend \
│   ├── main.py            # FastAPI app entrypoint \
│   ├── api/               # API route modules \   
│   └── requirements.txt   # Python dependencies \
│\
├── frontend/              # Svelte frontend \
│   ├── src/               # Svelte source files \
│   ├── public/            # Static assets \
│   ├── package.json       # Frontend dependencies and scripts \
│   └── svelte.config.js   # Svelte config \
│\
└── README.md              # This file \

### Set up backend

```
pip install the requirements
Run main.py
```

### Set up backend

```
npm install node modules
npm run dev
```
