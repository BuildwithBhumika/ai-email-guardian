# 🛡️ AI Email Guardian

### Intelligent Email Threat Detection using Machine Learning & NLP

**AI Email Guardian** is a machine-learning-based email security application that analyzes email content, detects potential phishing and spam threats, and provides an interpretable risk assessment through an interactive web interface.

---

## ✨ Features

* 🎯 Email classification
* ⚠️ Risk score and priority assessment
* 📊 Prediction confidence and category probabilities
* 🔎 Suspicious keyword detection
* 🔗 URL detection
* 📈 Session statistics
* 🧠 NLP-based text processing
* 🌐 Flask-powered web application

---

## 🏗️ How It Works

```text
Email Input
     ↓
Text Preprocessing
     ↓
TF-IDF Vectorization
     ↓
Multinomial Naive Bayes
     ↓
Threat Analysis
     ↓
Risk Score + Classification
     ↓
Interactive Dashboard
```

The system combines **machine-learning predictions with rule-based security indicators** to provide a more informative threat assessment.

---

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **Scikit-learn**
* **Pandas**
* **NumPy**
* **TF-IDF**
* **Multinomial Naive Bayes**
* **HTML / CSS / JavaScript**

---

## 📂 Project Structure

```text
ai-email-guardian/
│
├── app.py              # Flask application & API
├── model.py            # ML model training & prediction
├── preprocessing.py    # Text preprocessing
├── utils.py            # Threat detection & risk scoring
├── dataset.csv         # Training dataset
├── model.pkl           # Trained ML model
├── vectorizer.pkl      # TF-IDF vectorizer
├── docs/
│   └── screenshots/
│       ├── application.png
│       └── analysis-result.png
│
└── README.md
```

---

## 📸 Application

### Email Input

Users can enter email content or use the built-in sample emails for phishing, spam, promotion, and safe-email testing.

![AI Email Guardian Interface](docs/screenshots/application.png)

### Threat Analysis Dashboard

The dashboard displays the classification result, confidence, risk score, priority, category probabilities, suspicious keywords, detected URLs, and session statistics.

![AI Email Guardian Analysis](docs/screenshots/analysis-result.png)

---

# 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/BuildwithBhumika/ai-email-guardian.git
```

### 2. Open the project

```bash
cd ai-email-guardian
```

Make sure `app.py` is present in the current directory.

### 3. Install dependencies

```bash
pip install flask flask-cors scikit-learn pandas numpy
```

### 4. Start the application

```bash
python app.py
```

You should see:

```text
Running on http://127.0.0.1:5000
```

### 5. Open in your browser

Go to:

**http://localhost:5000/**

---

## 🔌 API Endpoints

| Method | Endpoint   | Purpose                     |
| ------ | ---------- | --------------------------- |
| `GET`  | `/`        | Main application            |
| `POST` | `/analyze` | Analyze email content       |
| `GET`  | `/stats`   | Retrieve session statistics |

### Example `/analyze` Request

```json
{
  "text": "URGENT! Your account has been suspended. Verify your password immediately."
}
```

The application returns information such as:

* Classification
* Confidence
* Risk score
* Priority
* Category probabilities
* Suspicious keywords
* Detected URLs

---

## 🧠 Machine Learning

The project uses:

**TF-IDF → Multinomial Naive Bayes → Email Classification**

Additional rule-based signals are used for suspicious keywords, URLs, and other threat indicators to improve the final risk assessment.

---

## 🔐 Security Note

This project is intended for educational and development purposes.

Do not submit real passwords, API keys, confidential emails, authentication codes, or other sensitive information while testing.

---

## 🚧 Future Improvements

* Real-time email integration
* Browser extension
* Larger and more diverse datasets
* Advanced phishing detection
* Deep-learning models
* Production deployment

---

## 👩‍💻 Author

**Bhumika Chauhan**

GitHub: https://github.com/BuildwithBhumika

---

⭐ **AI Email Guardian — Machine Learning powered email threat detection with an interactive security dashboard.**




