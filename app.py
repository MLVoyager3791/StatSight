import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# Function to perform basic exploratory data analysis
def basic_eda(data):
    display_basic_info(data)
    visualize_missing_values(data)
    display_correlation_matrix(data)

# Function to display basic information about the dataset
def display_basic_info(data):
    col1, col2, col3, col4 = st.columns([0.23, 0.23, 0.27, 0.27]) # spec entered for maintaining the width - relative width
    with col1:
        st.header("Shape of Dataset")
        st.write(data.shape)
    with col2:
        st.header("Total Null Values")
        st.write(data.isna().sum().sum())
    with col3:
        st.header("Duplicated Records")
        st.write(data.duplicated().sum())
    with col4:
        st.header("No. of Features")
        st.write(len(data.columns))

    st.header("Unique Columns in Dataset")
    st.write(pd.DataFrame(data.columns.to_list(), columns=["Column Names"]))

    st.header("Data Types of Columns")
    st.write(pd.DataFrame(data.dtypes, columns=["Data Type"]))

    st.header("Statistical Description of the Dataset")
    st.write(data.describe())

# Function to visualize missing values in the dataset
def visualize_missing_values(data):
    st.header("Visualizing Missing Values")
    
    # Creating tabs for different visualizations
    tab1, tab2 = st.tabs(["Bar Plot", "Heatmap"])

    with tab1:
        st.subheader("Bar Plot")
        # Calculating number of missing values in each column
        missing_values = data.isnull().sum()
        missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

        if not missing_values.empty:
            with plt.style.context('dark_background'):
                plt.figure(figsize=(10, 6))
                ax = sns.barplot(x=missing_values.index, y=missing_values.values, palette="viridis")
                ax.set_facecolor('#000000')  # Setting face color of the axes to black, trying to give some nice look.
                plt.xlabel("Columns", color='white')
                plt.ylabel("Number of Missing Values", color='white')
                plt.title("Missing Values Count", color='white')
                plt.xticks(rotation=45, ha='right', color='white')
                plt.yticks(color='white')
                st.pyplot()
        else:
            st.write("No missing values in the dataset.")
    
    with tab2:
        st.subheader("Heatmap")
        plt.style.use('dark_background')  # Setting dark background style
        plt.figure(figsize=(10, 6))
        colours = ['#000000', 'seagreen']
        sns.heatmap(data.isnull(), cmap=sns.color_palette(colours), cbar=False, annot=False)
        st.pyplot()
        plt.style.use('default')  # Resetting to default style

# Function to display the correlation matrix
def display_correlation_matrix(data):
    numeric_data = data.select_dtypes(include=[float, int])
    st.header("Correlation Matrix")
    st.write(numeric_data.corr())
    
    st.header("Correlation Heatmap")
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="viridis")
    st.pyplot()

# Main function to run the application
def main():
    settings = load_settings()
    
    st.title(settings.app_name)
    st.subheader(settings.tagline)  
    
    choice = display_sidebar()
    data = upload_file()

    if data is not None:
        if choice == "Basic EDA":
            basic_eda(data)

# Run the main function
if __name__ == "__main__":
    main()
