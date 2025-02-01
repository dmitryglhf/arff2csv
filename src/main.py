import pandas as pd
from scipy.io.arff import loadarff 
import streamlit as st


@st.cache_data
def convert_df_to_csv(df: pd.DataFrame, file_name: str):
    return df.to_csv(f"{file_name}.csv", index=False).encode("utf-8")


def clear_upload_file_list():
    st.session_state['uploaded_files'] = None


if __name__ == "__main__":
    st.set_page_config(page_title='arff2csv', page_icon="./src/icon.png", 
                       layout="centered", initial_sidebar_state="auto", 
                       menu_items=None)

    st.header("Online converter :blue[.arff] to :green[.csv]", divider="gray")

    # Upload fules
    uploaded_files = st.file_uploader(
        "Choose a .arff file(s)", 
        accept_multiple_files=True,
        type='arff',
        key='uploaded_files'
    )

    output = []
    if uploaded_files:
        convert, clear = st.columns(2)
        if convert.button("Convert", use_container_width=True):
            try:
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete, file in enumerate(uploaded_files):
                    my_bar.progress(percent_complete + 1, text=progress_text)
                    # arff_file = loadarff(file.getvalue())
                    # df = pd.DataFrame(arff_file[0])
                    # csv_file = convert_df_to_csv(df, file.name)
                    # output.append(csv_file)
                my_bar.empty()


                text_contents = '''This is some text'''
                st.download_button(
                    "Download", 
                    text_contents, 
                    use_container_width=True
                )
                st.write(":green[Succes]")
            except:
                my_bar.empty()
                st.write(":red[Failed]")
        if clear.button("Clear files", use_container_width=True):
            st.rerun()
