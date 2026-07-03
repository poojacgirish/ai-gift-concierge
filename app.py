import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Gift Concierge",
    page_icon="🎁",
    layout="centered",
)

# -----------------------------
# Sidebar - API Key
# -----------------------------
st.sidebar.header("OpenAI Settings")
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Paste your OpenAI API key here. It is only used for this session.",
)

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
    if not api_key.strip():
        st.warning("Please enter your OpenAI API key in the sidebar before generating gift ideas.")
        st.stop()

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are an expert personal shopper. "
        f"The user is looking for a gift. Recipient age: {age}, "
        f"Relationship: {relationship}, "
        f"Budget: {budget}, "
        f"Interests: {interests}. "
        "Provide exactly 3 specific, highly searchable real-world gift recommendations. "
        "Format your response strictly with the Product Name (bolded), Estimated Price, "
        "and one sentence explaining why it is a perfect match based on their interests. "
        "Do not include introductory or concluding conversational filler."
    )

    try:
        with st.spinner("Finding the perfect gifts... 🎁"):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                ],
                temperature=0.8,
            )

        result = response.choices[0].message.content

        st.success("Here are your personalized gift recommendations!")
        st.markdown(result)

    except Exception as e:
        st.error(f"An error occurred: {e}")
