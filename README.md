# Intelligent Child Vaccination Management System 
### Leveraging Machine Learning for Dropout Prediction & Automated Interventions

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-green.svg)](https://nodejs.org/)
[![Flask](https://img.shields.io/badge/Flask-API-black.svg)](https://flask.palletsprojects.com/)

This project is a **Hybrid AI-Logic Command Center** designed to predict child vaccination dropouts and trigger real-time community interventions. Moving beyond traditional, reactive reminder systems, this project utilizes a Community-First Predictive Model to identify geographical "hotspots" and automates localized "Smart-Nudge" alerts via WhatsApp and Email.

---

##  Table of Contents
1. [The Problem & Solution](#-the-problem--solution)
2. [Core Public Health Metrics](#-core-public-health-metrics)
3. [Machine Learning Model](#-machine-learning-model)
4. [System Architecture](#-system-architecture)
5. [Installation & Setup](#-installation--setup)
6. [Running the Application](#-running-the-application)
7. [Testing & Sample Data](#-testing--sample-data)

---

##  The Problem & Solution

**The Gap:** Traditional vaccination tracking systems rely on reactive tracking and overall accuracy models that fail to identify the minority "dropout" class (<15% of patients). Furthermore, they suffer from "alert fatigue" and fail to address complex socio-economic barriers.

**The Solution:** This system integrates predictive AI analytics with a real-time intervention engine. It uses a balanced Random Forest model optimized for recall, paired with a dual-action response system:
1. **Macro-Level (Authority Warning):** Formal SMTP emails to Health Department Officials.
2. **Micro-Level (Community Nudge):** Automated WhatsApp broadcasts to community parents using a Node.js microservice.

---

## Core Public Health Metrics

The system's AI is grounded in real-world public health engineering, utilizing two primary engineered metrics:

* **1. The Dropout Gap (%):** Measures the percentage of children who started the vaccination cycle (BCG) but did not finish (DPT/Fully Immunized). 
  * *Formula:* ((BCG - Fully Immunized) / BCG) * 100
  * *Safety Override:* If this gap mathematically exceeds **50%**, the system automatically triggers a High-Risk alert, regardless of the AI's prediction, preventing dangerous false negatives.
* **2. ASHA Efficiency Ratio:** Measures the availability of Accredited Social Health Activists (ASHA) worker sessions relative to the population. A low ratio indicates a "Logistical Desert" where community mobilization is failing.
  * *Formula:* (ASHA_Sessions / Population) * 1000

---

## Machine Learning Model

* **Algorithm:** Random Forest Classifier (Trained on 15,000 DHS-aligned synthetic records).
* **Optimization:** Utilizes a 1:6 cost-sensitive learning ratio to prioritize minority class (dropout) recall over global accuracy.
* **Accuracy:** **76.67%** (Optimized Research Benchmark).
* **Decision Threshold:** A highly sensitive **0.30 (30%) probability threshold** is used to trigger interventions.
* **Key Feature (SES_Score):** An interaction feature combining parental education and wealth index (Mother_Education × Wealth_Index). This captures the compounding risk of socio-economic vulnerability and proved to be a top-3 predictor.

---

## System Architecture

This project utilizes a **Microservices Architecture** to ensure reliable communication.

    regional_vaccination_system/
    ├── data/                       # Raw DHS-aligned datasets & Processed CSVs
    ├── models/                     # .pkl files (Saved Random Forest Brain)
    ├── scripts/                    # Preprocessing, Training, Confusion Matrix generation
    ├── api/                        # Python/Flask Microservice
    │   ├── templates/dashboard.html     
    │   ├── app.py                  # API Gateway & Risk Logic
    │   └── intervention_engine.py  # SMTP & HTTP Requests to Node
    ├── whatsapp_service/           # Node.js Microservice
    │   ├── package.json            
    │   └── server.js               # Express API & whatsapp-web.js logic
    ├── outputs/                    # Visuals (.png) and Audit Logs (.log)
    └── .env                        # Secure Credentials (Ignored in Git)

---

## Installation & Setup

### 1. Prerequisites
* Python 3.8+
* Node.js v16+
* An Android/iOS device with WhatsApp for QR code linking.

### 2. Clone the Repository

    git clone https://github.com/YOUR_USERNAME/regional-vaccination-system.git
    cd regional-vaccination-system

### 3. Setup Python Backend (Flask API)

    pip install flask pandas scikit-learn joblib requests python-dotenv seaborn matplotlib

### 4. Setup Node.js Backend (WhatsApp Gateway)
*Note: We use the direct GitHub repository for whatsapp-web.js to bypass common Puppeteer Execution Context crashes.*

    cd whatsapp_service
    npm init -y
    npm install express body-parser qrcode-terminal
    npm install github:pedroslopez/whatsapp-web.js#main

### 5. Environment Variables
Create a .env file in the root directory:

    SENDER_EMAIL=your_official_email@gmail.com
    SENDER_PASSWORD=your_gmail_app_password
    WHATSAPP_SERVER_URL=http://localhost:3000/send-whatsapp

---

## Running the Application

You must run two terminals simultaneously.

**Terminal 1: Start the WhatsApp Gateway**

    cd whatsapp_service
    node server.js

*Wait for the QR code to generate in the terminal and scan it with your WhatsApp mobile app (Linked Devices).*

**Terminal 2: Start the AI Brain & Dashboard**
*From the root directory:*

    python api/app.py

*Open your browser and navigate to http://127.0.0.1:5000/*

---

## Testing & Sample Data

Use the web dashboard to test the system's "Gold Standard" prediction patterns.

### Scenario A: High Risk (Logistical Collapse)
Simulates a district with a failing cold chain and no community outreach.
* **Population:** 1,500,000
* **BCG Starts:** 60,000
* **Fully Immunized:** 15,000 *(Creates a massive 75% Dropout Gap)*
* **ASHA Sessions:** 12 *(Creates a near-zero efficiency ratio)*
* **Expected Result:** **HIGH RISK**. System will trigger email and WhatsApp broadcasts.

### Scenario B: Low Risk (Healthy System)
Simulates a district with excellent retention and infrastructure.
* **Population:** 500,000
* **BCG Starts:** 20,000
* **Fully Immunized:** 19,500 *(Close to 0% Dropout Gap)*
* **ASHA Sessions:** 600 *(Healthy 1.2+ ratio)*
* **Expected Result:** **LOW RISK** (~18% Probability). System correctly avoids triggering alerts, solving "Alert Fatigue."

---

## License & Ethics
This is a research prototype developed by Ananya Singh and Vinayak Singh. It adopts a regional, district-level data model to avoid the legal complexities of handling individual Patient Health Information (PHI), making it suitable for scalable public health deployment.