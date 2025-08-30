import streamlit as st
import pandas as pd

# -----------------------------
# Streamlit App: Expense Categorizer (Stable, Generator Only)
# -----------------------------

st.set_page_config(page_title="Expense Categorizer", page_icon="💸", layout="centered")

st.title("💸 Expense Categorizer")
st.write("Upload a CSV file with your expenses and categorize them automatically using keyword rules.")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload your expenses CSV", type=["csv"])

if uploaded_file:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Uploaded Data Preview")
        st.dataframe(df.head())

        # -----------------------------
        # Rules for Categorization
        # -----------------------------
        rules = {
            "Food & Dining": ["restaurant", "cafe", "kfc", "mcdonald", "food", "takeaway", "dine"],
            "Transport": ["uber", "taxi", "bus", "fuel", "petrol", "diesel", "train"],
            "Groceries": ["shoprite", "woolworths", "spar", "pick n pay", "grocery", "supermarket"],
            "Utilities": ["electricity", "water", "internet", "wifi", "telkom", "dstv"],
            "Entertainment": ["netflix", "spotify", "movie", "cinema", "showmax", "theatre"],
            "Health": ["pharmacy", "clinic", "doctor", "hospital", "medication"],
            "Shopping": ["clothes", "mall", "checkers", "edgars", "mr price", "woolworths clothing"],
            "Other": []  # default fallback
        }

        def categorize(description):
            desc = str(description).lower()
            for category, keywords in rules.items():
                if any(word in desc for word in keywords):
                    return category
            return "Other"

        # -----------------------------
        # Apply Categorization
        # -----------------------------
        if "Description" in df.columns:
            df["Category"] = df["Description"].apply(categorize)

            st.subheader("✅ Categorized Expenses")
            st.dataframe(df)

            # -----------------------------
            # Export Downloads
            # -----------------------------
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Categorized CSV",
                data=csv,
                file_name="categorized_expenses.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ CSV must contain a **'Description'** column for categorization.")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")

else:
    st.info("📂 Please upload a CSV file to begin.")