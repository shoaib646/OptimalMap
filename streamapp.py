import streamlit as st
import datetime
import os
from TrafficData.TrafficFlowPredictor import *
import route_finding as router
import pdb
class Window:
    def __init__(self):
     
        self.windowTitle = st.set_page_config(page_title="Maple's Window")
        self.title = st.markdown("## Optimal Path Finder")
        self.developers = st.markdown("#### Developed by: [Shoaib Ahmed](https://www.cruzai.tech) Locations: [Scarborough](https://drive.google.com/file/d/1ctPug1ibuR2pj5CGuA9yGlynM1SUv3Y3/view?usp=sharing)")
        self.model = st.selectbox("Model:", [option.value for option in TrafficFlowModelsEnum])
        # st.markdown('<p style="color: red;">Source:</p>', unsafe_allow_html=True)
        self.src = st.text_input("Source:*", placeholder='e.g: 6145')     
        # pdb.set_trace()  
        self.dest = st.text_input("Destination:*", "", placeholder='e.g: 9732')
        self.date_string = st.text_input("Date | Time:", "")
     

        if st.button("Generate"):
            self.run()        
        if st.button("View on Map"):
            self.view_routes()

        self.pred = st.text_input("Predict route Traffic Flow:")
        if st.button("Predict"):
            self.predict_flow()

    def parse_date(self, date_string):
        try:
            date = datetime.datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            date = datetime.datetime.now()
        return date

    def run(self):
        st.text("Generating Routes...")
        src = self.src
        dest = self.dest
        if src == '' or dest == '':
            st.text("Please enter Route ID")
            return
        routes = router.runRouter(src, dest, self.parse_date(self.date_string), self.model)
        # print(pdb.set_trace())
        # pdb.set_trace()
        self.set_text_box(routes)

    def set_text_box(self, text):
        st.text(text)

    def view_routes(self):
        map_html = open("index.html", "r").read()
        st.components.v1.html(map_html, height=600)
        

    def predict_flow(self):
        st.text("Predicting...")
        point = str(self.pred)

        if point == '':
            st.text("Please enter Route ID")
            return

        predictor = TrafficFlowPredictor()
        date = self.parse_date(self.date_string)
        try:
            flow = predictor.predict_traffic_flow(point, date, 4, self.model)
        except:
            st.text("Invalid Route ID")
            return

        st.text(f"--Predicted Traffic Flow--\nRoute_ID:\t\t{point}\nTime:\t\t{date.strftime('%Y/%m/%d %I:%M:%S')}\nPrediction:\t\t{str(flow)}veh/hr")


if __name__ == "__main__":
    
    window = Window()
