# 🌍 Language Translator – Flask Project

## 📖 Description

A simple **Flask-based web application** for text translation.  
Users can enter text, select source and target languages, and get instant translations without reloading the page and have the prononciation of both source and translated text.

The project uses:  
- **Flask** → backend API (`/translate` route, JSON requests)  
- **HTML / CSS** → user interface  
- **JavaScript** → fetch translations dynamically  

---

## ✨ Features

- 📝 Text input for translation  
- 🌐 Select source and target languages  
- ⚡ Real-time translation (AJAX, no reload)  
- 📱 Simple & responsive UI  

---

## ⚙️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/Hamel82/CodeAlpha_LanguageTranslateTool.git

cd CodeAlpha_LanguageTranslateTool
```

2. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
project/
│── app.py                # Flask backend
│── templates/
│    └── index.html       # Main HTML page
│── static/
│    └── script.js        # JavaScript (translation logic)
└── README.md             # Documentation
```

---

## 🚀 Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open your browser:

👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. Enter text, choose languages, and click **Translate**.  
4. The translated text will appear instantly below the form.  

---

## 📌 Notes

- 🔧 Currently uses a **simulated backend** for translation.  
- 🌐 Can be connected to a real translation API (e.g. **LibreTranslate**, **Google Translate API**).  

---

## 👨‍💻 Author

Developed by **Hamel82** 🚀  

---
