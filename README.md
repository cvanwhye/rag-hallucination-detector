# 🕵️‍♀️ RAG Hallucination Detector

A powerful AI auditing tool designed to detect hallucinations in RAG (Retrieval-Augmented Generation) applications. It uses **Gemini 1.5 Flash** to cross-reference AI-generated responses against a source truth, providing a detailed truthfulness report.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Features

- **Fact-Checking Engine**: Uses Gemini 1.5 Flash to compare claims against source text.
- **Trust Score**: Calculates a percentage score based on supported vs. unsupported sentences.
- **Detailed Audit**: Breaks down the response sentence-by-sentence.
    - ✅ **Supported**: Information is present in the source.
    - ❌ **Contradicted**: Information directly contradicts the source.
    - ⚠️ **Hallucinated**: Information is missing from the source.
- **JSON Output**: Robust backend using JSON mode for reliable parsing.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zebra-coder/rag-hallucination-detector.git
   cd rag-hallucination-detector
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up credentials:**
   - Create a `.env` file in the root directory.
   - Add your Google Gemini API key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

##  ▶️ Usage

Run the Streamlit app:
```bash
streamlit run auditor.py
```

1. Paste your **Source Text** (the ground truth context) into the left column.
2. Paste the **AI Response** you want to check into the right column.
3. Click **🔍 Audit for Hallucinations**.
4. Review the **Trust Score** and inspected sentences.
