import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AI Gift Concierge",
    page_icon="🎁",
    layout="centered",
)

# Configure Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error(
        "GEMINI_API_KEY not found in Streamlit secrets. "
        "Please add it to your Streamlit secrets before running the app."
    )
    st.stop()

model = genai.GenerativeModel("gemini-1.5-flash-latest")

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
            response = model.generate_content(system_prompt)

        st.success("Here are your personalized gift recommendations!")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
