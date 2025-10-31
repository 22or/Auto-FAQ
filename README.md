# Auto-FAQ

An intelligent AI agent that integrates with Gmail to automatically detect and respond to Frequently Asked Questions (FAQs). Auto-FAQ uses natural language processing and machine learning to understand incoming queries, match them against your knowledge base, and send appropriate automated responses.

All automated replies include a clear footer:
```
This is an automated response. If this did not answer your question, reply again.
```

This ensures recipients know they're interacting with an AI agent and can easily escalate if needed.

<img width="1111" height="480" alt="image" src="https://github.com/user-attachments/assets/f98117a9-14bb-4e38-a859-b6a8a5904824" />

## Features

- **Intelligent FAQ Detection**: Uses spaCy NLP and confidence scoring to identify FAQ queries
- **Gmail Integration**: Seamlessly connects with your Gmail account via the Gmail API
- **Automated Responses**: Sends helpful replies automatically with clear automation disclaimers
- **Custom Knowledge Base**: Configure your own FAQ content in natural language format
- **Smart Filtering**: Marks FAQs as read and organizes messages for easy retrieval
- **Human Review Queue**: Flags ad-hoc queries that require personal attention
- **Confidence-Based Decision Making**: Only responds when confident in the answer

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account (for Gmail API access)
- pip package manager

### Gmail API Setup

Before running Auto-FAQ, you need to set up the Gmail API:

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Gmail API**
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Select "Desktop app" as the application type
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project root

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/22or/Auto-FAQ.git
   cd Auto-FAQ
```

2. **Install Python dependencies**
```bash
   pip install -r requirements.txt
```

3. **Download the spaCy language model**
```bash
   python -m spacy download en_core_web_sm
```
   
   *Note: You can customize the spaCy model based on your needs*

4. **Authenticate with Gmail**
```bash
   python gmail/reply_script.py
```
   
   This will:
   - Open a browser for Google authentication
   - Generate a `token.json` file for future API access
   - Store your credentials securely

5. **Configure your knowledge base**
   
   Edit `gmail/context.txt` with your FAQ content. The spaCy model (`en_core_web_sm`) can understand natural language, so format your FAQs naturally:
```
   Q: What are your business hours?
   A: We're open Monday through Friday, 9 AM to 5 PM EST.
   
   Q: How do I reset my password?
   A: Click the "Forgot Password" link on the login page and follow the instructions.
   
   Q: What is your return policy?
   A: We accept returns within 30 days of purchase with original receipt.
```

## Running Auto-FAQ

Auto-FAQ requires two processes running simultaneously:

### 1. Start the MLServer Inference Server
```bash
mlserver start faq
```

The inference server will start on `http://localhost:8080` by default.

### 2. Start the Agent Service
```bash
python gmail/reply_script.py
```

The agent will:
- Monitor your Gmail inbox continuously
- Process incoming messages
- Send automated replies to detected FAQs
- Mark messages appropriately

## Project Structure
```
Auto-FAQ/
├── gmail/
│   ├── reply_script.py      # Main agent service
│   ├── context.txt          # Your FAQ knowledge base
│   └── ...                  # Additional Gmail utilities
└── ml server/                     # MLServer model configuration
```

## Customization

### Using Different spaCy Models

The default model is `en_core_web_sm`, but you can use larger or specialized models:
```bash
# For better accuracy (larger model)
python -m spacy download en_core_web_md

# For best accuracy (largest model)
python -m spacy download en_core_web_lg

# For domain-specific needs
python -m spacy download en_core_web_trf  # Transformer-based
```

Update the model reference in your code accordingly.

### Adjusting Confidence Thresholds

The system uses confidence scores to determine when to auto-reply. You can adjust these thresholds in the code to make the agent more or less conservative.

### Knowledge Base Format

`context.txt` supports flexible formatting that `en_core_web_sm` can understand:
- Question-Answer pairs
- Natural language descriptions
- Bullet points
- Conversational text
- JSON or structured data

The NLP model will extract semantic meaning regardless of exact format.

## Security & Privacy

- **OAuth 2.0**: Secure authentication with Gmail
- **Token Storage**: API tokens stored locally on your machine
- **No Data Collection**: All processing happens on your infrastructure
- **API Permissions**: Only requests necessary Gmail permissions
- **Local Processing**: Your FAQ data never leaves your system

## Contributing

Contributions are welcome! Here are some ways to help:

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Disclaimer

This is an automated email agent. While Auto-FAQ aims to provide accurate responses, it should be monitored regularly to ensure quality and appropriateness of automated replies. Always review flagged messages that require human attention.
