import json
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from tools.TextTools import translateText

class ReviewPage():

    def app(input):
        print(f"In Review page : {input}")
        print(type(input))
        # json_data = json.dumps(input, indent=4)
        # print(type(json_data))
        # json_data = json_data.replace("\'", "\"").replace('},{', '} {')
        if isinstance(input, dict) == False:
            data = json.loads(input, strict=False)
        else:
            data = input
        # data = json_data
        print(type(data))
        language = data["input"]["language"]
        topic = data["topic"]
        print(f"Today's Topic : {topic}")
        title = f"Course Review "
        header1 = "Lesson Plan"
        header2 = "Short Summary"
        if language != "English":
            title = f"""{translateText(title, None, language)} - {translateText(topic, None, language)} ({title} - {topic})"""
            header1 = translateText(header1, None, language)
            header2 = translateText(header2, None, language)

        st.header(title)
        # Custom CSS to modify the textarea width and height 
        # height: 250px !important;
        textarea_css = '''
        <style>
            textArea {
                background-color: #FFFFFF !important;
                border:1px solid #224f5f !important;
            }
        </style>
        '''
        st.markdown(textarea_css, unsafe_allow_html=True)

        st.subheader(header1)
        data["course_plan"] = st.text_area("", data["course_plan"], height=250)
        st.subheader(header2)
        data["summary"] = st.text_area("", data["summary"], height=150)
        df = pd.DataFrame(data["sections"])

        # Drop columns with all null values
        ## df_cleaned = df.dropna(axis=1, how='all')

        # Specify the columns to check for null values
        columns_subset = ['section_name', 'section_details', 'section_summary']
        custom_headers = ['Section Name', 'Details', 'Audio Summary']

        sub_df = df[columns_subset]

        # Rename the columns using a dictionary
        sub_df.rename(columns=dict(zip(columns_subset, custom_headers)), inplace=True)

        # Use custom CSS to set the width of the DataFrame
        # st.markdown(
        #     """
        #     <style>
        #     .streamlit-expanderHeader {
        #         font-size: 20px;
        #     }
        #     .dataframe {
        #         width: 80%;
        #         margin: 0 auto;
        #     }
        #     </style>
        #     """,
        #     unsafe_allow_html=True
        # )

        # col1, col2, col3 = st.columns([0.1, 0.5,0.4], gap="small")
        # for index, row in df.iterrows():
        #     with st.container():
        #             with col1:
        #                  st.text_input(label='',value=row["section_name"] )
        #             with col2:
        #                  st.text_area(label='',value=row["section_details"])
        #             with col3:
        #                  st.text_input(label='',value=row["section_summary"])
        aggrid_css = '''{
                “.ag-root.ag-unselectable.ag-layout-normal”: {"border":"1px solid #224f5f !important";}               
        }'''
        gb = GridOptionsBuilder.from_dataframe(sub_df)
        # gb.configure_grid_options(rowHeight=100)
        gb.configure_default_column(
        filterable=False,
        # groupable=False,
        editable=True,
        wrapText=True,
        flex=1,
        maxWidth=700,
        # autoWidth=False,
        autoHeight=True
        )
        grid_options = gb.build()
        sections = AgGrid(sub_df, gridOptions=grid_options, custom_css=aggrid_css)

        ## Create the json object for the next call
        df = pd.DataFrame(sections.data)
        print(sections.data)
        print("New Values")
        # data_dict = dict({"section_name":a,"section_details":b,"section_summary":c } for a,b,c in zip(df["Section Name"],df["Details"],df["Audio Summary"]))
        data_dict = []
        for a,b,c in zip(df["Section Name"],df["Details"],df["Audio Summary"]):
            data_dict.append({"section_name":a,"section_details":b,"section_summary":c, "section_review":"Done" })
            print({"section_name":a,"section_details":b,"section_summary":c })
        print(data_dict)
        data["sections"] = data_dict
        data["input"]["review_status"] = "Done"
        st.session_state["data"] = data
        print("New Data Values")
        print(type(st.session_state["data"]))
        return data

        ## Using st.data_editor
        # st.data_editor(sub_df,
        #                 hide_index = True,
        #                 column_config={
        #                 "Details": st.column_config.TextColumn(width="large"),
        #                 "Audio Summary": st.column_config.TextColumn(width="medium"),
        #                 },
        #                 use_container_width=True,
        #                 # row_height=100
        #                 )
        # st.dataframe(sub_df, use_container_width=True)
        # st.table("section data")
