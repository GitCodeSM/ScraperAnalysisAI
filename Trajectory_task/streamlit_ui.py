import streamlit as st
import pandas as pd
# import os

from scraper import main


st.set_page_config(page_title="Analyse companies website overview and opportunities.")
st.title("Analyse companies website overview and opportunities with AI.")

import streamlit as st

# Access API key
openai_api_key = st.secrets["api_keys"]["api_key"]

# Access database credentials
db_user = st.secrets["database"]["user"]
db_password = st.secrets["database"]["password"]
db_host = st.secrets["database"]["host"]
db_name = st.secrets["database"]["name"]
db_port = st.secrets["database"]["port"]

st.write("CSV and Excel File Processor")
uploaded_file = st.file_uploader("Upload your input file (Excel or CSV)", type=["csv", "xlsx"])
# save_path = st.text_input("Provide the directory path to save the processed file:")
output_file_path = st.text_input("Provide the file path to save the output CSV:")
process_button = st.button("Process File")

if uploaded_file and output_file_path and process_button:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    # if save_path:
    #     os.makedirs(save_path, exist_ok=True)
    #     file_path = os.path.join(save_path, "input_companies.csv")
    #     df.to_csv(file_path, index=False)
    #     st.success(f"File saved successfully at: {file_path}")

    st.write("Uploaded Data:")
    st.write(df)

    st.write("Processing your input data...")
    df_output = main(df=df, openai_api_key=openai_api_key, output_file_path=output_file_path, db_user=db_user, db_password=db_password, db_host=db_host, db_port=db_port, db_name=db_name)
    st.write("Processed Data:")

    # Save the processed file to the provided path
    if not df_output.empty:
        st.success(f"File saved successfully at: {output_file_path}.")
        st.write(df_output)
    else:
        st.write("Some error while saving the output! Please run again.")

    # Download link for the processed file
    st.write("Download the output file.")
    st.download_button(
        label="Download Processed File",
        data=df_output.to_csv(index=False).encode("utf-8"),
        file_name="processed_file.csv",
        mime="text/csv"
    )
    st.write("Downloaded output file successfully!")
