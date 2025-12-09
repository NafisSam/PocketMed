<p align="center">
  <!-- Add your logo inside /assets/logo.png -->
  <img src="asset/logo.png" alt="PocketMed Logo" width="180"/>
</p>

<h1 align="center">PocketMed</h1>
<h3 align="center">Your care, uninterrupted.</h3>

---

## ⭐ Overview

PocketMed is a **personal medical file** that lives on your phone and travels with you everywhere.  
It stores your key health information and uses an LLM engine to provide **short, safe, personalized answers** to your medical questions — starting with diabetes.

This MVP demonstrates how real patient data  
→ is structured,  
→ fed into an LLM,  
→ and turned into **personalized health insights**, not generic internet answers.

---

## 📁 Core Features

### 📌 1) Personal Medical File  
A simple, always-available snapshot of your health:
- Age  
- Gender  
- Diabetes type  
- Disease duration  
- Current medications  
- Comorbidities  
- Latest HbA1c  

---

### 🤖 2) Smart, Personalized Answer Engine  
PocketMed tailors every answer **based on the user’s real clinical profile**, not one-size-fits-all information.

Two users may ask the same question —  
PocketMed gives **different answers** depending on their data.

---

### 🛡 3) Short, Safe, Clear Responses  
- Fully in English or Persian (depending on user input)  
- No prescribing / no dosing / no treatment orders  
- Medical terms appear cleanly (e.g., *HbA1c*, *Metformin*)  

---

## 🧠 How It Works

```mermaid
flowchart LR
A[Patient Profile] --> B[Structured Prompt]
B --> C[LLM Engine]
C --> D[Personalized Answer]
