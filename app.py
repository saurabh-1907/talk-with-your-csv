import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Configure Gemini API
def configure_gemini(api_key):
    genai.configure(api_key=api_key)

# Function to get Gemini's response
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')  # Use the Gemini Pro model
    response = model.generate_content(prompt)
    return response.text

def main():
    # Set up the page
    st.set_page_config(
        page_title="Ask Your CSV 📊",
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for a catchy UI
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stFileUploader {
        background-color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("Ask Your CSV 📊")
    st.markdown("Upload a CSV file and ask questions about your data. Powered by **Google Gemini**! 🚀")

    # Load the Gemini API key from Streamlit's environment variables
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Gemini API key not found. Please set the `GEMINI_API_KEY` environment variable in Streamlit.")
        st.stop()
    else:
        configure_gemini(os.environ["GEMINI_API_KEY"])

    # Upload CSV file
    csv_file = st.file_uploader("Upload a CSV file", type="csv", help="Upload a CSV file to analyze.")
    if csv_file is not None:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Display the dataframe
        st.subheader("Data Preview")
        st.write(df.head())

        # Ask a question
        st.subheader("Ask a Question")
        user_question = st.text_input(
            "Enter your question about the CSV data:",
            placeholder="e.g., What is the average salary?",
            help="Ask any question about the data in your CSV file."
        )

        if user_question and user_question.strip() != "":
            with st.spinner("Generating response..."):
                # Create a prompt for Gemini
                prompt = f"""
                You are a data analyst. The user has uploaded a CSV file and asked the following question:
                {user_question}

                Here is a preview of the data:
                {df.head().to_string()}

                Please provide a detailed and accurate response to the user's question.
                """
                
                # Get Gemini's response
                try:
                    response = get_gemini_response(prompt)
                    st.subheader("Response")
                    st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()