# Auto‑FAQ

Auto‑FAQ is a simple AI agent that integrates with Gmail to automatically handle Frequently Asked Questions (FAQs).

<img width="1111" height="480" alt="image" src="https://github.com/user-attachments/assets/41dab3d4-ae20-463d-9923-3d93d1b9740f" />


## Features
* Connects with your Gmail account to scan incoming messages and detect FAQ‑type queries.
* Uses custom context (you can supply a knowledge base or configurable FAQ list) to generate appropriate answers.
* Marks FAQs as read and organizes them for later retrieval.
* Detects ad-hoc queries and marks them for human review.

## Getting Started

### Prerequisites
* Python 3.x environment and required dependencies (requirements.txt or similar).
  * Installed spacy model - can be customized

### Installation & Setup
* Clone the repo and install dependencies:
```
git clone https://github.com/22or/Auto‑FAQ.git
cd Auto‑FAQ
pip install -r requirements.txt
```
* Install a spacy model via ``python -m spacy download`` - default required for this repo is ``en_core_web_sm``
* Run the reply script to log into your Gmail account and obtain an API token file:
```
python`gmail/reply script.py``
```
* Fill in custom knowledge base/FAQ context in ``gmail/context.txt`` (e.g., a JSON/CSV of question‑answer pairs).
* (Optional) Fine‑tune or choose a Hugging Face model for your domain.

### Run the agent
* Start the inference server:
```
mlserver start faq
```
* Start the agent service:
```
python 'gmail/reply script.py'
```

The inference server listens on port 8080 by default. 
