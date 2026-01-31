import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 1. Load Credentials
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="RAG Truthfulness Auditor", layout="wide")

# --- Logic: The Fact Checker ---
def analyze_truthfulness(source_text, ai_response, key):
    try:
        genai.configure(api_key=key)
        # We use 1.5 Flash because it is excellent at following JSON instructions
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are a Strict Fact-Checking Auditor.
        
        Task: Compare the 'AI Response' against the 'Source Text'.
        Determine if EVERY claim in the response is supported by the source text.
        
        Source Text:
        "{source_text}"
        
        AI Response:
        "{ai_response}"
        
        Output Requirements:
        Return a JSON List of objects. Do not write markdown.
        Format:
        [
            {{
                "sentence": "The exact sentence from the response.",
                "status": "Supported" or "Hallucinated" or "Contradicted",
                "reasoning": "A short explanation citing the source text."
            }}
        ]
        """
        
        # Force JSON mode for reliability
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
        
    except Exception as e:
        return f"Error: {e}"

# --- User Interface ---
st.title("🕵️‍♀️ RAG Hallucination Detector")
st.markdown("""
**Role:** AI Quality Assurance Specialist
**Goal:** Detect "Hallucinations" (information not present in the source) in AI outputs.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Source Truth (Context)")
    source_input = st.text_area("Paste Article / Manual / Wiki Text:", height=300, 
        value="SpaceX was founded in 2002 by Elon Musk. The company's goal is to reduce space transportation costs to enable the colonization of Mars. The Falcon 9 is a reusable rocket.")

with col2:
    st.subheader("2. AI Output (To Audit)")
    response_input = st.text_area("Paste the AI's Answer:", height=300,
        value="SpaceX was founded in 2005 by Elon Musk. It aims to colonize Mars using the Falcon 9, which is a fully reusable rocket. It was the first company to land on the Moon.")

# --- Audit Trigger ---
if st.button("🔍 Audit for Hallucinations"):
    if not api_key:
        st.error("Missing .env file.")
    else:
        with st.spinner("Cross-referencing claims against source..."):
            results = analyze_truthfulness(source_input, response_input, api_key)
            
            if isinstance(results, str):
                st.error(results)
            else:
                st.divider()
                
                # Metrics Dashboard
                hallucinations = sum(1 for item in results if item['status'] != "Supported")
                total = len(results)
                score = int(((total - hallucinations) / total) * 100)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Trust Score", f"{score}%", delta="-Low" if score < 100 else "+Perfect")
                m2.metric("Sentences Audited", total)
                m3.metric("Hallucinations", hallucinations, delta_color="inverse")
                
                st.subheader("📝 Sentence-by-Sentence Breakdown")
                
                for item in results:
                    # Visual styling for status
                    if item['status'] == "Supported":
                        icon = "✅"
                        color = "green"
                    elif item['status'] == "Contradicted":
                        icon = "❌"
                        color = "red"
                    else: # Hallucinated
                        icon = "⚠️"
                        color = "orange"
                    
                    with st.expander(f"{icon} {item['sentence']}"):
                        st.markdown(f"**Verdict:** :{color}[**{item['status']}**]")
                        st.write(f"**Reasoning:** {item['reasoning']}")