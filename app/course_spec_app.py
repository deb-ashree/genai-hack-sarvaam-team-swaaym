import json
import sys
import time
import streamlit as st

## Function Def
class Home():

    def __init__(self) -> None:
        self.grade = ""
        self.subject = ""
        self.topic = ""
        self.language = ""
        self.instructions = ""
        
    def prepareDict(self):
        input = {}
        input["grade"] = self.grade
        input["subject"] = self.subject
        input["topic"] = self.topic
        input["language"] = self.language
        input["instructions"] = self.instructions
        input["review_status"] = "Pending"

        print(input)
        return input

    def app(self):
        st.title("Course Creator")

        # Collate the data for the course
        self.grade = st.selectbox("Select Grade", ["Grade 3","Grade 4", "Grade 5", "Grade 6"])
        self.subject = st.selectbox("Select Subject", ["Hindi","Kannada", "Science", "Social"])
        self.topic = st.text_input(label="Add a topic of interest")

        if self.subject in ["Science", "Social"]:
            self.language = st.selectbox("Select Language", ["English","Hindi","Kannada", "Marathi"])
        else:
            self.language = self.subject

        self.instructions = st.text_area(label="Share your thoughts around how the course should be formatted or feel free to add any thing specific ")

        # Format the query for course
        ## inputs = {"grade" : self.grade, "subject" : self.subject, "topic" : self.topic,  "language" : self.language, "instructions": self.instructions}

        # Steps to run (on separate windows)
        # -----------------------------------
        # python server.py
        # streamlit run calculator_app.py

