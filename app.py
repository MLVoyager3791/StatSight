import streamlit as st
import pandas as pd
import warnings

# Ignore warnings to keep the output clean
warnings.filterwarnings("ignore")

# Define a class to hold settings for the application
class Settings:
    def __init__(self):
        self.app_name = "StatSight - An EDA Tool 📊"
        self.tagline = "See the Unseen...🧐🔍"

# Function to load settings from the Settings class
def load_settings():
    return Settings()

# Function to display the sidebar menu and return the user's choice
def display_sidebar():
    st.sidebar.title("Your EDA Tool")
    menu = ["Basic EDA"]
    choice = st.sidebar.selectbox("Select an option", menu)
    return choice

# Function to upload a file and return the loaded data
def upload_file():
    file = st.sidebar.file_uploader("Upload a file", type=["csv", "tsv", "xlsx", "xls"])
    if file is not None:
        try:
            if file.name.endswith(".csv"):
                data = pd.read_csv(file)
            elif file.name.endswith(".tsv"):
                data = pd.read_csv(file, sep='\t')
            elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
                data = pd.read_excel(file)
            st.subheader("Dataset")
            st.dataframe(data)
            return data
        except Exception as e:
            st.error(f"Error: {e}")
    return None

# Main function to run the application
def main():
    settings = load_settings()
    
    st.title(settings.app_name)
    st.subheader(settings.tagline)  
    
    choice = display_sidebar()
    data = upload_file()

# Run the main function
if __name__ == "__main__":
    main()
