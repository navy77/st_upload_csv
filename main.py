import streamlit as st
import pandas as pd
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

mqtt_broker = '192.168.0.160'
mqtt_port = 1883
mqtt_topic = 'force/data'
number_rows = 2
mqtt_broker = os.



st.title("Upload CSV data")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def connect_broker():
    while True:
        try:
            client.connect(mqtt_broker, mqtt_port, 60)
            print("Connected to MQTT broker")
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Call the function to connect to the broker
connect_broker()

if uploaded_file is not None:
    # Read the file name
    file_name = uploaded_file.name
    st.write(f"Uploaded file name: {file_name}")

    if st.button("Submit"):
        df = pd.read_csv(uploaded_file)
        
        # Display the data
        st.write("Data inside the file:")
        st.dataframe(df)
