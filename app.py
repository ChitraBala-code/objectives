# app.py
import streamlit as st
import random

st.set_page_config(page_title="Objective Question Generator")
st.markdown("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8523970821848927"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

st.title("📝 Objective Question Generator")
st.write("Enter a paragraph and generate objective questions")

text = st.text_area("Enter your text here", height=200)

if st.button("Generate Questions"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 5]

        if not sentences:
            st.error("Not enough content to generate questions.")
        else:
            for i, sent in enumerate(sentences, 1):
                words = sent.split()
                if len(words) < 5:
                    continue

                answer = random.choice(words)
                question = sent.replace(answer, "______", 1)

                st.subheader(f"Q{i}. {question}")
                st.write("A)", answer)
                st.write("B)", random.choice(words))
                st.write("C)", random.choice(words))
                st.write("D)", random.choice(words))
                st.success(f"Answer: {answer}")
                st.divider()

