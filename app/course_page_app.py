import base64
import json
import logging
import os
import pandas as pd
import requests
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from tools.TextTools import translateText

class CoursePage():

    def createAudioWithSarvaamBulbulV1(self, text, lang):
        print("Text input to Bulbul : "+text)
        url = "https://api.sarvam.ai/text-to-speech"

        if lang == 'kannada':
            lang = "kn-IN"
        if lang == 'hindi':
                lang = "hi-IN"
        if lang == 'english':
                lang = "en-IN"
        print(lang)
        payload = {
            "inputs": [f'{text}'],
            "target_language_code": f'{lang}',
            "speaker": "meera",
            "pitch": 0,
            "pace": 0.9,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        headers = {"Content-Type": "application/json", "api-subscription-key":"ec17625a-c39a-46da-a075-7dd41cd75052" }

        response = requests.request("POST", url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:

            audio_ascii = json.loads(response.text)["audios"][0]
            print("----+++------")
            print(type(audio_ascii))

            # audio_bytes = bytes(audio_ascii, 'utf-8') # didn't work

            # Decode the Base64 encoded audio
            audio_bytes = base64.b64decode(audio_ascii)
            print("----+++------")
            print(type(audio_bytes))

            # Define the directory and file path
            directory = "audio"
            audio_file = os.path.join(directory, "text.wav")
            
            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the decoded audio to a WAV file
            with open(audio_file, "wb") as f:
                f.write(audio_bytes)
                # playsound.playsound(audio_file)
            
            print(f"Audio saved as '{audio_file}'.")
            return audio_file
        else:
            print(f"Failed to get audio from API. Status code: {response.status_code}, Response: {response.text}")
            return None
        
    def tab_output(self,label, dfrow, language):
        #Set the display text        
        section_name = dfrow["Section Name"]
        if language != "English":
            section_name = translateText(section_name, None, language)

        st.header(section_name)
        side1, video_col, side2 = st.columns([0.001,0.998,0.001])
        with video_col:
            st.video(dfrow["Teacher Video"])
        # with side1:
        #     st.write(" ")
        # with side2:
        #     st.write(" ")

        text_col, audio_col = st.columns([0.9,0.1])
        with st.container():
            with text_col:
                st.write(dfrow["Details"])
            with audio_col:
                # audio_file = self.createAudioWithSarvaamBulbulV1(dfrow["Details"], "english")
                # st.audio(audio_file, format="wav")
                st.audio(dfrow["Teacher Audio"], format="wav")

    def app(self, data):
        print(f"Check Data : {data}")
        data = json.loads(data, strict=False)

        #Set the display text        
        language = data["input"]["language"]
        title = f""" Notes on {data["topic"]}"""
        header1 = "Lesson Summary"
        header2 = "Lesson Plan"
        if language != "English":
            title = translateText(title, None, language)+f""" ({title})"""
            header1 = translateText(header1, None, language)
            header2 = translateText(header2, None, language)

        st.title(title)
        
        ## Course Display
        st.subheader(header1)
        st.markdown(data["summary"])
        st.subheader(header2)
        st.markdown(data["course_plan"])

        # Specify the columns to check for null values
        # - section_name - Title
        # - summaryVideoURL, section_summary  - Teacher Video with Audio
        # - section_details, textContentAudioEnURL - Section details in text and audio format
        columns_subset = ['section_name', 'section_details', 'section_summary', 'summaryVideoURL', 'textContentAudioEnURL']
        custom_headers = ['Section Name', 'Details', 'Text for Audio Summary', 'Teacher Video', 'Teacher Audio']

        df = pd.DataFrame(data["sections"])
        sub_df = df[columns_subset]

        # Rename the columns using a dictionary
        sub_df.rename(columns=dict(zip(columns_subset, custom_headers)), inplace=True)

        ## Dynamically generate tabs
        # tab1, tab2, tab3, tab4, tab5 = st.tabs(sub_df['Section Name'])
        tab_labels = sub_df['Section Name'].unique().tolist()
        tabs = st.tabs(tab_labels)
        df_row = sub_df.iterrows()
        # for  row in zip(sub_df.iterrows()):
            #  print(row)
        for index, row_tab in enumerate(zip(sub_df.iterrows(),tab_labels, tabs)):
            row, label, tab = row_tab
            # print(f"{index}-{row}-{label}-{tab}")
            print(f"""----{row[1]}""")
            with tab:
                self.tab_output(label, row[1], language)



        # # Rename the columns using a dictionary
        # sub_df.rename(columns=dict(zip(columns_subset, custom_headers)), inplace=True)

        # gb = GridOptionsBuilder.from_dataframe(sub_df)
        # # gb.configure_grid_options(rowHeight=100)
        # gb.configure_default_column(
        # filterable=False,
        # # groupable=False,
        # editable=True,
        # wrapText=True,
        # flex=1,
        # maxWidth=700,
        # # autoWidth=False,
        # autoHeight=True
        # )
        # grid_options = gb.build()
        # sections = AgGrid(sub_df, gridOptions=grid_options)