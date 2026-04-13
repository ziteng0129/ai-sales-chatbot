import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# SETUP
# =========================

st.title("Confirm.AI Sales Assistant")

product_info = """
Product: iPhone 17
Price: RM4500
Warranty: 1 year
Delivery: 5-7 working days
Colour: Orange 
Stock count: 3
"""

# =========================
# CHAT MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================

if prompt := st.chat_input("Ask about the product..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # =========================
    # SALES LOGIC (IMPORTANT)
    # =========================

    if "interested" in prompt.lower() or "buy" in prompt.lower():
        reply = """Great! To proceed, please provide:
- Your name
- Phone number
- Preferred delivery date
"""

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    elif "," in prompt:
        reply = """Thank you! ✅

Your request has been recorded.

Our sales team will contact you within 24 hours via WhatsApp."""

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    # =========================
    # AI RESPONSE (FALLBACK)
    # =========================
    else:
        with st.chat_message("assistant"):
            with st.spinner("AI is typing..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
You are a professional sales assistant.

Product information:
{product_info}

Rules:
- Answer clearly and briefly
- Be friendly and professional
- Only answer product-related questions
- If not available, say politely
"""
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
