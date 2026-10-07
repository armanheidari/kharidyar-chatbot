# 🛒 خریدیار (Kharidyar) - Persian Conversational E-Commerce Chatbot

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ParsBERT](https://img.shields.io/badge/ParsBERT-BERT--Base-FF6F00?logo=huggingface&logoColor=white)](https://huggingface.co/HooshvareLab/bert-base-parsbert-uncased)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)

**خریدیار (Kharidyar)** is an end-to-end intelligent conversational AI assistant designed for online retail and grocery shopping in Persian (Farsi). It integrates advanced Persian Natural Language Processing (NLP), a fine-tuned Transformer-based Named Entity Recognition (NER) pipeline, intent and sentiment classification, a multi-turn dialogue state manager, real-time shopping cart and inventory synchronization, and a Retrieval-Augmented Generation (RAG) LLM agent.

Originally developed as an academic project at **Allameh Tabataba'i University (دانشگاه علامه طباطبائی)**, the system is designed to provide a natural, human-like shopping experience from item selection to checkout and customer support.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project & Directory Structure](#-project--directory-structure)
- [Supported Intents & Dialogue Capabilities](#-supported-intents--dialogue-capabilities)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Installation & Setup](#-step-by-step-installation--setup)
  - [1. Clone Repository & Setup Environment](#1-clone-repository--setup-environment)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Setup MySQL Database](#3-setup-mysql-database)
  - [4. Configure API Keys & Environment](#4-configure-api-keys--environment)
  - [5. Verify Pretrained Models](#5-verify-pretrained-models)
  - [6. Run the Application](#6-run-the-application)
- [Web Interface & Usage](#-web-interface--usage)
- [Model Training & Dataset Generation](#-model-training--dataset-generation)
- [Database Schema](#-database-schema)
- [License & Authors](#-license--authors)

---

## ✨ Key Features

- **Persian Natural Language Understanding (NLU)**:
  - Custom preprocessing tailored for Persian text using `hazm` (formal and informal normalization, spacing correction, lemmatization, stemming, number abstraction).
  - 10 Intent classes classified via `LinearSVC` with TF-IDF vectorization.
  - Sentiment analysis (positive/neutral vs. negative). Negative sentiment dynamically pivots the dialogue tree into an empathetic customer support flow.
- **ParsBERT-Powered Named Entity Recognition (Slot Filling)**:
  - Fine-tuned `HooshvareLab/bert-base-parsbert-uncased` models built on TensorFlow/Keras to extract item names, quantities, measurement units, and replacement items.
- **Dynamic Shopping Cart & Inventory Management**:
  - Live inventory tracking in MySQL. If an item is out of stock or insufficient, the bot informs the user.
  - Multi-item purchasing (e.g. `۲ کیلو سیب و ۳ پاکت شیر میخوام`).
  - Unit validation (matches valid units like کیلو, گرم, بسته, پاکت, بطری, عدد to specific products).
  - Flexible cart modifications (e.g. replace item with another product, update quantities).
  - Per-user cart caching in `Temp/Cart_{customer_id}.json` with automatic checkout committing to MySQL.
- **Order Lifecycle Management**:
  - Order finalizing with confirmation step.
  - Live order tracking (`tracking`) reporting order statuses (`progress`, `delivered`, `completed`, `returned`).
  - Order cancellation (`deleting`) with business logic enforcement (e.g. 8-hour cancellation policy, ownership verification).
  - Returns & refunds (`returning`) with automated eligibility verification.
- **RAG & Generative LLM Integration**:
  - Semantic search over store catalogue using `SentenceTransformer` (`paraphrase-multilingual-MiniLM-L12-v2`) and KNN cosine similarity.
  - Generative responses and customer service negotiation powered by `meta-llama/Llama-3-70b-chat-hf` via Together AI and LangChain.
  - Automated dissatisfaction root-cause extraction: automatically extracts order ID and dissatisfaction reason and registers a report in MySQL.
- **FastAPI Web Application & Real-time WebSockets**:
  - High-performance FastAPI server.
  - WebSocket streaming endpoint (`/ws`) for typing-animation token streaming.
  - Responsive RTL frontend with interactive chat window, sound effects, and real-time live cart drawer.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([User / Browser]) <--> |HTTP / WebSocket Stream| FastAPI[FastAPI Server :5050]
    
    subgraph Web_Layer [API & Presentation]
        FastAPI --> UI[Jinja2 RTL Interface + Vanilla JS]
        FastAPI --> ControlFlow[ControlFlow Dialogue Manager]
    end

    subgraph NLU_Layer [Natural Language Understanding]
        ControlFlow --> HazmPrep[Hazm Persian Preprocessing]
        HazmPrep --> IntentClassifier[Intent Classifier (SVM + TF-IDF)]
        HazmPrep --> SentimentClassifier[Sentiment Classifier (SVM + TF-IDF)]
        HazmPrep --> ParsBERT[ParsBERT Slot Filling / NER (TensorFlow)]
    end

    subgraph Business_Layer [Cart & State Management]
        ControlFlow --> CartMgr[Cart Manager]
        CartMgr <--> TempCart[(Temp JSON Cart Storage)]
    end

    subgraph Storage_Layer [Relational Database]
        ControlFlow <--> MySQL[(MySQL 8.4 Database)]
        CartMgr <--> MySQL
    end

    subgraph LLM_Layer [RAG & Customer Support]
        ControlFlow --> ChatbotAgent[ChatbotAgent]
        ChatbotAgent --> SentenceTrf[Sentence-Transformers (MiniLM-L12)]
        SentenceTrf --> KNN[Catalogue KNN Retrieval]
        ChatbotAgent --> LLaMA[LLaMA-3-70B via Together AI]
    end
```

---

## 📁 Project & Directory Structure

```plaintext
kharidyar-chatbot/
├── API/                              # Web application & server components
│   ├── static/                       # Static web assets (CSS styles, JS, fonts, images)
│   │   ├── app.js                    # Frontend WebSocket client and cart UI handler
│   │   ├── style.css                 # Main styling (RTL layout, chat bubbles, cart drawer)
│   │   └── images/                   # UI icons and backgrounds
│   ├── templates/                    # Jinja2 HTML templates
│   │   ├── base.html                 # Main chat and cart interface
│   │   └── base-old.html             # Legacy UI template
│   ├── app.py                        # Core dialogue state manager (ControlFlow class)
│   ├── main.py                       # FastAPI application entry point & WebSocket route
│   └── app.log                       # Server and model runtime log output
│
├── Cart/                             # Shopping cart module
│   ├── cart.py                       # Cart class: add/remove/edit, pricing, MySQL sync
│   └── test.ipynb                    # Cart integration notebook
│
├── Database/                         # Database scripts & configurations
│   ├── data/                         # Local database mount directories
│   ├── init-scripts/                 # Initialization SQL scripts for Docker containers
│   ├── create_tables.sql             # MySQL DDL: schema, tables, triggers, seed data
│   ├── database.py                   # Singleton Database class: queries, order tracking, reports
│   └── docker-compose.yml            # Docker Compose service for MySQL 8.4 on port 24000
│
├── Datasets/                         # Datasets for training & evaluation
│   ├── intention_dataset.csv         # Full labeled intent dataset
│   ├── intention_dataset_without_faq.csv # Intent dataset excluding FAQ categories
│   ├── sentiment_dataset.csv         # Labeled Persian sentiment dataset
│   ├── chitchat_dataset.csv          # Chitchat and greetings data
│   ├── ner_dataset_0.json            # Synthetic NER dataset for buying & inquiring slots
│   ├── ner_dataset_1.json            # Synthetic NER dataset for cart editing slots
│   ├── ner_dataset_2.json            # Synthetic NER dataset for scheduling/tracking slots
│   └── hotel_r/                      # Reference sentiment & stopword resources
│
├── IntentionData/                    # Intent dataset generator
│   ├── data.py                       # Entity vocabularies (items, units, days, events)
│   ├── templates.py                  # Persian sentence templates for intents
│   ├── data_augmentor.py             # Synonym replacement & data augmentation
│   └── main.py                       # Synthetic intent dataset synthesis pipeline
│
├── IntentionModel/                   # Intent classification modeling
│   ├── preprocessor.py               # Hazm Persian normalizer, lemmatizer, stemmer
│   ├── model.py                      # Scikit-learn Pipeline with LinearSVC & grid search
│   ├── data_analysis.ipynb           # Exploratory data analysis for intents
│   └── main.py                       # Model training, hyperparameter tuning & export
│
├── LLM Chatbot/                      # RAG & Generative AI engine
│   ├── chatbot.py                    # Agent wrapper with Pandas/CSV conversation buffer
│   ├── generative_model.py           # LangChain chains with Together AI (LLaMA-3-70B)
│   ├── retrival_model.py             # SentenceTransformer embedding & KNN retriever
│   ├── prompts.py                    # Structured Persian prompts for QA, returns, customer service
│   ├── history.py                    # CustomizedChatMessageHistory implementation
│   ├── kharidyar-catalogue.txt       # Store product catalogue used as RAG knowledge base
│   └── llm_main.py                   # ChatbotAgent initialization & pipeline compilation
│
├── Models/                           # Serialized models and weights
│   ├── intention_recognizer_model.pkl           # Trained intent classifier
│   ├── intention_recognizer_model_2.pkl         # Secondary intent classifier
│   ├── intention_recognizer_model_without_faq.pkl
│   ├── sentiment_recognizer_model.pkl           # Primary sentiment classifier
│   ├── sentiment_recognizer_model_2.pkl         # Optimized sentiment classifier
│   ├── ner_model_0/                  # ParsBERT checkpoint for buying/inquiring entities
│   ├── ner_model_1/                  # ParsBERT checkpoint for cart editing entities
│   └── ner_model_2/                  # ParsBERT checkpoint for tracking/returning entities
│
├── NERData/                          # Synthetic NER dataset generator
│   ├── NER_Data_Generator.py         # Slot annotation engine (BIO/token alignment)
│   ├── NER_Data_Templates.py         # Persian slot-filling sentence templates
│   └── NER_Data_Main.py              # Generation orchestrator for ner_dataset_*.json
│
├── NERModel/                         # Deep learning NER module
│   ├── ner_preprocessing.py          # ParsBERT tokenizer alignment & slot encoding
│   ├── model.py                      # Custom NERDetector Keras model (TFBertModel + Dense)
│   ├── model_testing.ipynb           # Model evaluation and token inspection notebook
│   └── main.py                       # Training loop and checkpoint export for NER
│
├── NLU/                              # Unified NLU coordinator
│   ├── nlu.py                        # Central NLU inference coordinator
│   └── main.py                       # NLU model loader and runtime config assembler
│
├── Results/                          # Evaluation metrics and analysis charts
│   ├── hyperparameter_tuning_intention_model.xlsx
│   ├── hyperparameter_tuning_sentiment_model.xlsx
│   └── *.png                         # Dataset distribution and token count plots
│
├── Sentiment Identification/         # Sentiment classifier development
│   ├── data_manipulator.py           # Sentiment data preparation & balancing
│   ├── data_analysis.ipynb           # Sentiment dataset EDA
│   └── main.py                       # Sentiment SVM training with RandomizedSearchCV
│
├── Temp/                             # Runtime cart caches (e.g., Cart_1.json)
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore patterns
└── README.md                         # Project documentation
```

---

## 🗣️ Supported Intents & Dialogue Capabilities

| Intent | Persian Description | Example Queries | Handled By |
|---|---|---|---|
| `buying` | خرید محصول | «دو تا شیر و یک کیلو سیب میخوام» | NLU (ParsBERT NER) ➔ Cart Manager ➔ MySQL |
| `editting` | ویرایش سبد خرید | «سیب رو به ۳ کیلو تغییر بده» / «شیر رو با دوغ عوض کن» | NLU ➔ Cart Manager |
| `finishing` | نهایی‌سازی و ثبت سفارش | «سفارشم رو ثبت کن» ➔ تایید نهایی («بله» / «خیر») | Cart Manager ➔ MySQL `orders` |
| `tracking` | پیگیری وضعیت سفارش | «سفارش شماره ۱۲۳ چی شد؟» | Database `order_tracking()` |
| `returning` | مرجوع کردن سفارش | «میخوام سفارشم رو مرجوع کنم» | Database `refund_order()` + Policy Check |
| `deleting` | لغو سفارش ثبت شده | «سفارش شماره ۴۵ رو لغو کن» | Database `delete_order()` (8-hour window check) |
| `inquiring` | استعلام کالا و محصولات | «شیر کم‌چرب دارید؟ قیمتش چنده؟» | RAG (Catalogue KNN) + MySQL Description |
| `customer-service` | پشتیبانی و ثبت شکایت | «سفارشم ناقص بود و بسته‌بندی خراب بود» | LLaMA-3 Agent ➔ Reason Extraction ➔ MySQL `report` |
| `chitchat` | گفتگوی عمومی و معرفی | «سلام، تو کی هستی؟» | LLM Prompt grounded in Kharidyar identity |
| `scheduling` | زمان‌بندی تحویل | «سفارشم فردا صبح ارسال بشه» | Dialogue State Machine |

> [!NOTE]
> **Sentiment Redirection**: If a user's utterance yields a negative sentiment (`sentiment == -1`), Kharidyar immediately switches to `customer-service` mode. It converses with the user to diagnose the dissatisfaction, asks for the order ID, registers the report into the `report` table, and prompts the user whether they would like to initiate an automated refund.

---

## 💻 Prerequisites

Ensure you have the following installed on your system:

- **Operating System**: Linux, macOS, or Windows (tested on Windows with PowerShell).
- **Python**: Version **3.10** or **3.11** (recommended `3.11.x`).
- **Docker & Docker Compose**: For containerized MySQL 8.4 database hosting.
- **Hardware**:
  - Minimum: 8 GB RAM, Multi-core CPU.
  - Recommended: 16 GB RAM + NVIDIA GPU with CUDA for faster ParsBERT inference.
- **Together AI Account**: An API key from [Together AI](https://www.together.ai/) to access `meta-llama/Llama-3-70b-chat-hf`.

---

## 🚀 Step-by-Step Installation & Setup

### 1. Clone Repository & Setup Environment

Navigate to your workspace directory and create a virtual environment:

```bash
# Clone the repository (or navigate to existing directory)
cd kharidyar-chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
# source venv/bin/activate
```

### 2. Install Dependencies

Install all required Python libraries:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> [!TIP]
> If you encounter issues installing `tensorflow` and `torch` side-by-side, ensure your `pip` version is up-to-date. In `requirements.txt`, `tf_keras==2.16.0` is explicitly pinned to support Keras 3 with legacy Keras model checkpoints.

### 3. Setup MySQL Database

The application connects to a MySQL 8.4 database by default on port `24000`:
- **Database Name**: `kharidyar`
- **Username**: `root`
- **Password**: `12345678`
- **Port**: `24000`

#### Option A: Running with Docker Compose (Recommended)

Start the MySQL service using Docker Compose:

```bash
cd Database
docker compose --profile db up -d
```

Once the container is healthy, apply the database schema:

```bash
# Execute schema inside the container
docker exec -i mysql_kharidyar mysql -u root -p12345678 kharidyar < create_tables.sql
cd ..
```

#### Option B: Using an Existing Local MySQL Server

If you already have a local MySQL server installed:
1. Open MySQL CLI or a client (e.g. MySQL Workbench, DBeaver).
2. Execute the commands in [Database/create_tables.sql](file:///Database/create_tables.sql).
3. If using standard port `3306`, update the port in [Database/database.py](file:///Database/database.py#L23):
   ```python
   def __init__(self, host: str = "localhost", user: str = "root", password: str = "12345678", database: str = "kharidyar", port: str = "3306")
   ```

### 4. Configure API Keys & Environment

The LLM module communicates with Together AI for LLaMA-3 inference. By default, an API key is set in [LLM Chatbot/generative_model.py](file:///LLM%20Chatbot/generative_model.py#L26).

To configure your own key, set the `TOGETHER_API_KEY` in `generative_model.py`:

```python
self.llm = ChatTogether(
    together_api_key="your_together_ai_api_key_here",
    model=config["model_name"],
)
```

### 5. Verify Pretrained Models

Verify that the following model files exist in the `Models/` folder:
- `intention_recognizer_model_2.pkl`
- `intention_recognizer_model_without_faq.pkl`
- `sentiment_recognizer_model_2.pkl`
- `ner_model_0/` (`checkpoint`, `ner_checkpoint.data*`, `ner_checkpoint.index`)
- `ner_model_1/`
- `ner_model_2/`

*(If the ParsBERT checkpoints are missing, you can regenerate and train them using the instructions in [Model Training](#-model-training--dataset-generation).)*

### 6. Run the Application

Launch the FastAPI application server:

```bash
# Navigate to API directory and start uvicorn
cd API
python main.py
```

Or via direct Uvicorn command from the project root:

```bash
uvicorn API.main:app --host 0.0.0.0 --port 5050 --reload
```

The server will be available at:
👉 **http://localhost:5050/** (automatically redirects to `http://localhost:5050/ui/new`)

---

## 🖥️ Web Interface & Usage

1. Open your browser and navigate to **`http://localhost:5050/ui/new`**.
2. **Chat Window**: Type your shopping requests in Persian:
   - `سلام خریدیار`
   - `دو تا شیر و یک کیلو موز میخوام`
   - `قیمت سیب چنده؟`
   - `سفارشم رو ثبت کن`
3. **Interactive Cart Drawer**: When items are recognized and validated, they automatically appear in the right-side shopping cart with real-time price updates.
4. **WebSocket Streaming**: Responses are streamed word-by-word via the `/ws` endpoint for a responsive conversation.

### Running in CLI Mode (Testing Without Browser)

You can also test the dialogue loop directly in the terminal:

```bash
cd API
python app.py
```

```plaintext
You: سلام دو تا شیر میخوام
Bot: {'status': 'cart', 'message': ['شیر به سبد خرید اضافه شد.'], 'content': [[2, 'پاکت', 'شیر']], 'current_price': 56000.0}
```

---

## 🔬 Model Training & Dataset Generation

### 1. Generating Synthetic Datasets

The project uses rule-based Persian templating engines to generate diverse shopping interactions:

```bash
# Generate Intent Dataset
python IntentionData/main.py

# Generate NER / Slot-Filling Datasets
python NERData/NER_Data_Main.py
```

### 2. Training Intent Classifier

To train the SVM intent classifier and perform randomized hyperparameter optimization:

```bash
python IntentionModel/main.py
```

Tuning results and performance metrics are automatically logged to `Results/hyperparameter_tuning_intention_model.xlsx`.

### 3. Training Sentiment Classifier

To train the SVM sentiment detector:

```bash
cd "Sentiment Identification"
python main.py
```

### 4. Training ParsBERT NER Models

To fine-tune ParsBERT on the generated slot-annotated datasets:

```bash
python NERModel/main.py
```

The script compiles `TFBertModel` with a classification head and exports checkpoints to `Models/ner_model_0`, `Models/ner_model_1`, and `Models/ner_model_2`.

---

## 🗄️ Database Schema

The system uses a relational MySQL schema defined in `Database/create_tables.sql`:

- **`users`**: Customer profiles (`customer_id`, `name`, `email`, `phone`, `password`).
- **`products`**: Available catalogue items (`product_id`, `name`, `price`).
- **`product_unit`**: Measurement units supported per product (`unit`).
- **`inventory`**: Real-time stock counts (`count`). Triggers prevent negative inventory.
- **`orders`**: Customer orders (`order_id`, `customer_id`, `total_price`, `status`, `updated_time`).
  - Statuses: `progress`, `delivered`, `completed`, `returned`.
- **`order_products`**: Items linked to an order with quantities (`order_id`, `product_id`, `amount`).
- **`products_description`**: Descriptive metadata for RAG and product inquiries.
- **`chat_history`**: Audit log of conversational turns (`author`, `input_text`, `input_timestamp`).
- **`report`**: Registered customer dissatisfaction complaints (`user_id`, `order_id`, `report`).

---

## 👥 Authors & Academic Credits

- **Institution**: Allameh Tabataba'i University (دانشگاه علامه طباطبائی), Computer Science Department.
- **Project Name**: خریدیار (Kharidyar Chatbot).
- **Core Developers**: Arman Heidari, Jonathan Sina, and collaborators.

---

## 📜 License

This project is licensed under the terms included in the [LICENSE](file:///LICENSE) file.