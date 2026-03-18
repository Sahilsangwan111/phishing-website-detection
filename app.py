import streamlit as st
import pandas as pd
import pickle
import re
from urllib.parse import urlparse

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Phishing Detection", layout="centered")

# -------------------- BACKGROUND + UI STYLE --------------------
st.markdown("""
    <style>
    .stApp {
        background-image: url("assests/Projectphoto.webp");
        background-size: cover;
        background-position: center;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 25px;
        border-radius: 15px;
    }

    .stTextInput>div>div>input {
        background-color: #0f172a;
        color: white;
        border: 1px solid #00ff9f;
    }

    .stButton>button {
        background-color: #00ff9f;
        color: black;
        font-size: 18px;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }

    h1, h2, h3 {
        color: #00ff9f;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- LOAD MODEL --------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------- FEATURE NAMES --------------------
feature_names = [
    'having_IP_Address','URL_Length','Shortining_Service','having_At_Symbol',
    'double_slash_redirecting','Prefix_Suffix','having_Sub_Domain','SSLfinal_State',
    'Domain_registeration_length','Favicon','port','HTTPS_token','Request_URL',
    'URL_of_Anchor','Links_in_tags','SFH','Submitting_to_email','Abnormal_URL',
    'Redirect','on_mouseover','RightClick','popUpWidnow','Iframe',
    'age_of_domain','DNSRecord','web_traffic','Page_Rank','Google_Index',
    'Links_pointing_to_page','Statistical_report'
]

# -------------------- FEATURE EXTRACTION --------------------
def extract_features(url):
    features = []

    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else -1)
    features.append(1 if len(url) < 54 else 0 if len(url) <= 75 else -1)
    features.append(-1 if any(x in url for x in ["bit.ly", "tinyurl", "goo.gl"]) else 1)
    features.append(-1 if "@" in url else 1)
    features.append(-1 if url.count("//") > 1 else 1)

    domain = urlparse(url).netloc
    features.append(-1 if "-" in domain else 1)
    features.append(-1 if domain.count('.') > 1 else 1)
    features.append(1 if url.startswith("https") else -1)

    # IMPORTANT FIX (phishing detect better)
    while len(features) < 30:
        features.append(-1)

    return features

# -------------------- UI --------------------
st.markdown("<h1>🔐 Phishing Detection System</h1>", unsafe_allow_html=True)

st.write("Enter a website URL to check whether it is safe or phishing")

url = st.text_input("🔗 Enter Website URL")

if st.button("🚀 Check Website"):
    if url:
        features = extract_features(url)
        input_df = pd.DataFrame([features], columns=feature_names)

        prediction = model.predict(input_df)

        if prediction[0] == 1:
            st.success("✅ This Website is SAFE (Legitimate)")
        else:
            st.error("⚠️ This Website is PHISHING!")
    else:
        st.warning("⚠️ Please enter a URL first")

st.markdown("---")
st.caption("Developed by Sahil 🚀 | Model Accuracy: 96.6%")