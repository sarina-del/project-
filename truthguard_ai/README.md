# TruthGuard AI

A simple Learn AI competition prototype for **Ethical Technology and Misinformation Detection**.

## Features

- Misinformation / fake information detector
- Privacy policy summariser
- Flask backend API
- HTML, CSS, and JavaScript frontend
- Rule-based demo logic so it works without a paid AI API

## Folder Structure

```text
truthguard_ai/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## How to Run in VS Code

1. Open the `truthguard_ai` folder in VS Code.

2. Open the terminal in VS Code.

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate it.

For Windows PowerShell:

```bash
venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

5. Install requirements:

```bash
pip install -r requirements.txt
```

6. Run the app:

```bash
python app.py
```

7. Open this in your browser:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Check misinformation

```text
POST /api/check-misinformation
```

Request:

```json
{
  "text": "Paste article, claim, or social media post here"
}
```

### Summarise privacy policy

```text
POST /api/summarise-policy
```

Request:

```json
{
  "policy": "Paste privacy policy here"
}
```

## Demo Tip

For the misinformation checker, try text like:

```text
URGENT!!! This secret cure was hidden by doctors. Share this now before it gets deleted.
```

For the privacy policy summariser, try text like:

```text
We collect your name, email, location data, cookies and device information. We may share data with third-party partners for advertising. You may request deletion of your data and withdraw consent.
```
