
import streamlit as st
import pandas as pd
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
# mqtt_broker = '192.168.0.160'
# mqtt_port = 1883
# mqtt_topic = 'force/data'
# number_rows = 2
mqtt_broker = os.getenv('mqtt_broker')
mqtt_port = 1883
mqtt_topic = os.getenv('mqtt_topic')
number_rows = int(os.getenv('number_rows'))

client = mqtt.Client()

st.title("Upload CSV data")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def connect_broker():
    while True:
        try:
            client.connect(mqtt_broker, mqtt_port, 60)
            print("Connected to MQTT broker")
            break
        except Exception as e:
            st.error('Error'+str(e), icon="❌")
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
# HAL Cover_15_50002902142_24X15C_DBW-AA4
    if uploaded_file is not None:
        file_name = str(uploaded_file.name)
        name_split = file_name.split("_")
        die = name_split[1]
        bash = name_split[2]
        lot = name_split[3]
        cav_full = name_split[4]
        cav_split = cav_full.split(".")
        cav = cav_split[0]

        st.write(f"Uploaded file name: {file_name}")
        if st.button("Submit"):
            try:
                connect_broker()
                data = pd.read_csv(uploaded_file, header=None, nrows=number_rows)
                df = pd.DataFrame(data)
                df_split = df[0].str.split("=", expand=True) 
                df_split[0] = df_split[0].str.strip()
                df_split[1] = df_split[1].str.strip()
                data_dict = dict(zip(df_split[0], df_split[1]))

                data_dict["die"] = str(die)
                data_dict["bash"] = str(bash)
                data_dict["lot"] = str(lot)
                data_dict["cav"] = str(cav)

                json_data = json.dumps(data_dict, indent=4)
                client.publish(mqtt_topic, json_data)
                st.success('Send data finished !', icon="✅")
            except Exception as e:
                st.error('Error'+str(e), icon="❌")

if __name__ == "__main__":
    main()
    connect_broker()
