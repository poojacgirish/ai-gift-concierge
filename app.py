import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Gift Concierge",
    page_icon="🎁",
    layout="centered",
)

# Configure Gemini client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error(
        "GEMINI_API_KEY not found in Streamlit secrets. "
        "Please add it to your Streamlit secrets before running the app."
    )
    st.stop()

# -----------------------------
# Main UI
# -----------------------------
st.title("🎁 AI Gift Concierge")

st.write(
    "Generate thoughtful, personalized gift ideas in seconds based on the "
    "recipient's age, relationship, budget, and interests."
)

with st.form("gift_form"):
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=30,
        step=1,
    )

    relationship = st.selectbox(
        "Relationship",
        [
            "Parent",
            "Partner",
            "Friend",
            "Coworker",
            "Child",
            "Other",
        ],
    )

    budget = st.selectbox(
        "Budget",
        [
            "Under ₹500",
            "₹500 - ₹1000",
            "₹1000 - ₹3000",
            "₹3000+",
        ],
    )

    interests = st.text_area(
        "Interests / Vibe",
        placeholder="e.g., Loves hiking, drinks too much coffee",
        height=120,
    )

    submitted = st.form_submit_button("Find Perfect Gifts 🎁")

# -----------------------------
# Backend Logic
# -----------------------------
if submitted:
    prompt = f"""
You are an expert personal shopper.

The user is looking for a gift.

Recipient age: {age}
Relationship: {relationship}
Budget: {budget}
Interests: {interests}

Provide exactly 3 specific, highly searchable real-world gift recommendations.

For each recommendation, use this exact format:

**Product Name**
Estimated Price: <price>
Why it's a perfect match: <one sentence>

[Find it here](https://www.google.com/search?tbm=shop&q=Product+Name)

For each of the 3 products, you must include a clickable Markdown link that routes the user to Google Shopping. Format it exactly like this:

[Find it here](https://www.google.com/search?tbm=shop&q=Product+Name)

Ensure you replace spaces in the URL with +. Do not guess or invent store URLs. Only use the Google Shopping search URL format above.

Do not include introductory or concluding conversational filler.
"""

    try:
        with st.spinner("Finding the perfect gifts... 🎁"):
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )

        st.success("Here are your personalized gift recommendations!")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
