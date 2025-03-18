# n8n Workflow: AI Agent for Financial Analysis

This workflow automates financial analysis tasks using AI, integrating with various services like Gmail, Google Sheets, and a financial data API.

## Overview

The n8n workflow is designed to:

1.  Receive user queries via a chat interface.
2.  Use AI to process the query and fetch relevant financial data.
3.  Optionally, send emails and store data in Google Sheets.

## n8n Installation

1.  **Install n8n:**

    - **Using npm:**
      ```bash
      npm install -g n8n
      ```
    - **Using Docker:**
      ```bash
      docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
      ```
    - Refer to the [official n8n documentation](https://docs.n8n.io/getting-started/) for more detailed installation instructions and options.

2.  **Start n8n:**

    - **Using npm:**
      ```bash
      n8n start
      ```
    - **Using Docker:** The container should already be running from the installation step.

3.  **Access n8n:**
    - Open your web browser and go to `http://localhost:5678` (or the appropriate address if you've configured a different port or are using a remote server).

## Importing the Workflow

1.  **Open n8n:**

    - Make sure your n8n instance is running and accessible in your web browser.

2.  **Navigate to Workflows:**

    - In the n8n interface, click on the "+" icon in the left sidebar to create a new workflow or select an existing one.

3.  **Import Workflow:**

    - Click the menu button (three dots) in the top right corner of the n8n interface.
    - Select "Import from file".

4.  **Select the JSON File:**

    - Choose the `AI_agent_workflow.json` file from your file system.

5.  **Workflow Imported:**

    - The workflow should now be imported into your n8n instance. You will see all the nodes and connections as described in the "Nodes" section.

6.  **Configure Credentials (Important):**

    - Follow the "Configure Credentials" section above to set up the necessary API keys and OAuth2 connections for Groq, Gmail, and Google Sheets. This step is crucial for the workflow to function correctly.

7.  **Enable the Workflow:**
    - Once you have configured the credentials, activate the workflow by clicking the "Active" toggle in the top right corner of the n8n interface.
## Nodes

### 1. Chat Interface

- **Type:** Chat Trigger
- **Purpose:** Provides a public webhook to receive chat messages.
- **Webhook ID:** `bitcoin-chat-webhook`
- **Configuration:**
  - `Public`: true
  - `Mode`: webhook

### 2. AI Agent1

- **Type:** Langchain Agent
- **Purpose:** Processes the chat input using an AI agent.
- **Configuration:**
  - `Prompt Type`: define
  - `Text`: `{{ $json.chatInput }}`
  - `Options`:
    - `System Message`: respond with simple message
    - `passthroughBinaryImages`: false

### 3. Groq Chat Model

- **Type:** LM Chat Groq
- **Purpose:** Uses the Groq language model to generate responses.
- **Configuration:**
  - `Model`: `qwen-2.5-32b`
- **Credentials:** Requires a Groq API key.

### 4. Gmail1

- **Type:** Gmail Tool
- **Purpose:** Sends emails.
- **Configuration:**
  - `Send To`: ` {{ $fromAI('To', ``, 'string') }} `
  - `Subject`: ` {{ $fromAI('Subject', ``, 'string') }} `
  - `Message`: ` {{ /*n8n-auto-generated-fromAI-override*/ $fromAI('Message', ``, 'string') }} `
- **Credentials:** Requires Gmail OAuth2 credentials.

### 5. HTTP Request (Bitcoin Price)

- **Type:** Tool HTTP Request
- **Purpose:** Fetches the current Bitcoin price from the CoinGecko API.
- **Configuration:**
  - `Tool Description`: you can find the bitcoin price here
  - `URL`: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`

### 6. read email here

- **Type:** Google Sheets Tool
- **Purpose:** Reads data from a Google Sheet.
- **Configuration:**
  - `Document ID`: `1BTOjppl-kBObtQEUkaTA3cX_t2LvIMhOZt_aV7Vhm4s`
  - `Sheet Name`: `gid=0`
- **Credentials:** Requires Google Sheets OAuth2 API credentials.

### 7. save email here

- **Type:** Google Sheets Tool
- **Purpose:** Appends data to a Google Sheet.
- **Configuration:**
  - `Operation`: append
  - `Document ID`: `1BTOjppl-kBObtQEUkaTA3cX_t2LvIMhOZt_aV7Vhm4s`
  - `Sheet Name`: `gid=0`
  - `Columns`:
    - `name`: `{{ $fromAI("name") }}`
    - `Email`: `{{$fromAI("email")}}`
- **Credentials:** Requires Google Sheets OAuth2 API credentials.

### 8. HTTP Request1 (Stock Analysis)

- **Type:** Tool HTTP Request
- **Purpose:** Retrieves stock analysis data from a financial data API.
- **Configuration:**
  - `Tool Description`: get the info about the data
  - `Method`: POST
  - `URL`: `https://data-analist-agent.onrender.com/api/stock/analysis`
  - `Send Body`: true
  - `Parameters Body`:
    - `symbol`
    - `period`
    - `interval`

## Setup Instructions

1.  **Import the Workflow:**

    - Import the `AI_agent_workflow.json` file into your n8n instance.

2.  **Configure Credentials:**

    - **Groq API:**
      - Create a [Groq account](https://console.groq.com/users/sign_up).
      - Obtain your API key from the Groq console.
      - In n8n, create a new credential of type "Groq API" and enter your API key.
    - **Gmail OAuth2:**
      - Create a [Google Cloud project](https://console.cloud.google.com/).
      - Enable the Gmail API for your project.
      - Create OAuth 2.0 credentials.
      - In n8n, create a new credential of type "Gmail OAuth2" and configure it with your Google Cloud project details.
    - **Google Sheets OAuth2 API:**
      - Create a [Google Cloud project](https://console.cloud.google.com/).
      - Enable the Google Sheets API for your project.
      - Create OAuth 2.0 credentials.
      - In n8n, create a new credential of type "Google Sheets OAuth2 API" and configure it with your Google Cloud project details.

3.  **Configure Google Sheets:**

    - Create a Google Sheet with the ID `1BTOjppl-kBObtQEUkaTA3cX_t2LvIMhOZt_aV7Vhm4s`.
    - Ensure the sheet named `Sheet1` exists.
    - The sheet should have columns for "name" and "Email".

4.  **Configure HTTP Request1 (Stock Analysis):**

    - Ensure that the `https://data-analist-agent.onrender.com/api/stock/analysis` endpoint is accessible.

5.  **Enable the Workflow:**
    - Activate the workflow in n8n.

## Usage

1.  **Trigger the Workflow:**

    - Send a chat message to the Chat Interface webhook URL.

2.  **AI Processing:**

    - The AI Agent will process the message, potentially using the Bitcoin price and stock analysis tools.

3.  **Email Sending (Optional):**

    - If the AI determines an email should be sent, it will use the Gmail node.

4.  **Data Storage (Optional):**
    - If the AI determines data should be stored, it will use the Google Sheets node.

## Notes

- Ensure all credentials are correctly configured for the workflow to function properly.
- The Gmail API must be enabled in your Google Cloud project for the Gmail node to work.
- The Google Sheets API must be enabled in your Google Cloud project for the Google Sheets node to work.
- Adjust the AI Agent prompt and tool descriptions to suit your specific needs.
- The workflow is currently configured to fetch Bitcoin prices and stock analysis data. Modify the HTTP Request nodes to fetch other data as needed.

