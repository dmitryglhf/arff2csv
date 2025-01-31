import pandas as pd
from scipy.io.arff import loadarff 
import streamlit as st


@st.cache_data
def convert_df(df: pd.DataFrame, file_name: str):
    return df.to_csv(f"{file_name}.csv", index=False).encode("utf-8")


if __name__ == "__main__":
    st.set_page_config(page_title='arff2csv', page_icon='icon.png', 
                       layout="centered", initial_sidebar_state="auto", 
                       menu_items=None)

    st.header("Online converter :blue[.arff] to :green[.csv]", divider="gray")

    uploaded_files = st.file_uploader(
        "Choose a .arff file", 
        accept_multiple_files=True,
        type='arff'
    )

    files = []
    result = []

    if uploaded_files is not None:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        # files.append(uploaded_files)

        for percent_complete, file in enumerate(files):
            my_bar.progress(percent_complete + 1, text=progress_text)

            # Read .arff file
            arff_file = loadarff(file.read)

            # Convert to .csv
            df = pd.DataFrame(arff_file[0])
            csv_file = convert_df(df, file.name)
            result.append(csv_file)
        my_bar.empty()

    # Download .csv
    if result:
        st.download_button(
            label="Download data as CSV",
            data=result,
            file_name="large_df.csv",
            mime="text/csv",
        )
