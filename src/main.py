import pandas as pd
from scipy.io import arff
import streamlit as st
import io
import zipfile


if __name__ == "__main__":
    st.set_page_config(page_title='arff2csv', page_icon="./src/icon.png", 
                       layout="centered", initial_sidebar_state="auto", 
                       menu_items=None)

    st.header("Online converter :blue[.arff] to :green[.csv]", divider="gray")

    # Upload fules
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 1

    uploaded_files = st.file_uploader(
        "Choose a .arff file(s)", 
        accept_multiple_files=True,
        type='arff',
        key=st.session_state["uploader_key"]
    )

    # Result
    zip_buffer = io.BytesIO()
    conversion_complete = False

    # Convertion
    if uploaded_files:
        convert, clear = st.columns(2)

        # Convert button
        if convert.button("Convert", use_container_width=True):
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_archive:
                try:
                    for uploaded_file in uploaded_files:
                        # Read data and load as .arff
                        file_content = uploaded_file.read().decode('utf-8')
                        string_io = io.StringIO(file_content)
                        data, meta = arff.loadarff(string_io)

                        # Convert data to DataFrame
                        df = pd.DataFrame(data)

                        # Convert to .csv and update archive
                        csv = df.to_csv(index=False).encode('utf-8-sig')
                        csv_filename = f"{uploaded_file.name.split('.')[0]}.csv"
                        zip_archive.writestr(csv_filename, csv)
                    
                    conversion_complete = True
                except Exception as e:
                    st.error(f"Error with file {uploaded_file.name}: {e}")

        # Clear button
        if clear.button("Clear files", use_container_width=True):
            st.session_state["uploader_key"] += 1
            conversion_complete = False
            st.rerun()

        # Download results as archive
        zip_buffer.seek(0)
        st.download_button(
            label="Download data as CSV",
            use_container_width=True,
            data=zip_buffer,
            file_name="converted_files.zip",
            mime="application/zip",
            disabled=not(conversion_complete)
        )
        if conversion_complete:
            st.success('All files successfully converted')
