# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 20:37:10 2022

@author: Ronald Nyasha Kanyepi
@email : kanyepironald@gmail.com
"""

import os
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
import folium
import requests
from requests.exceptions import ConnectionError


def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'logo.ico'))
    st.set_page_config(page_title='GEO LOCATION APP', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    st.balloons()
    # I want it to show balloon when it finished loading all the configs


def get_geolocation():
    key = "API_KEY"
    response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + key)
    return response.json()


def other_tab():
    st.header("Other TAB")


def home():
    try:
        with st.spinner("Please wait your request is being processed ......"):
            response = get_geolocation()
            st.header("IP Geolocation App 🕵️‍♂️")
            col1, col2 = st.columns([8, 4])

            with col1:
                m = folium.Map(location=[response["latitude"], response["longitude"]], zoom_start=16)
                tooltip = "The Approx Location"
                folium.Marker(
                    [response["latitude"], response["longitude"]],
                    popup="The Approx Location", tooltip=tooltip
                ).add_to(m)
                folium_static(m,width=500,height=400)



            with col2:
                st.markdown(f"""
                <table>
                <thead>
                   <th>Data</th>
                   <th>Value</td>
                </thead>
                
                <tr>
                   <td>Ip Address</td>
                   <td>{response["ip"]}</td>
                </tr>
                
                <tr>
                   <td>City</td>
                   <td>{response["city"]}</td>
                </tr>
                
                <tr>
                   <td>District</td>
                   <td>{response["district"]}</td>
                </tr>
                
                <tr>
                   <td>Province</td>
                   <td>{response["state_prov"]}</td>
                </tr>
                
                <tr>
                   <td>Calling Code</td>
                   <td>{response["calling_code"]}</td>
                </tr>
                <tr>
                   <td>Latitude</td>
                   <td>{response["latitude"]}</td>
                </tr>
                
                <tr>
                   <td>Longitude</td>
                   <td>{response["longitude"]}</td>
                </tr>
                           
                <tr>
                   <td>Country</td>
                   <td><img src="{response['country_flag']}" style="width:30%;max-width:40%"> {response["country_name"]}</td>
                </tr>
                

    
                </table>


""",unsafe_allow_html=True)

            with st.expander("More Information regarding this IP"):
                st.subheader("Currency")
                df = pd.DataFrame.from_dict(response["currency"], orient="index", dtype=str, columns=['Value'])
                st.write(df)
                st.subheader("ISP")
                st.write("isp",{response["isp"]})
                st.write("connection_type",{response["connection_type"]})
                st.write("organization", {response["organization"]})

                st.subheader("TimeZone")
                df_1 = pd.DataFrame.from_dict(response["time_zone"], orient="index", dtype=str, columns=['Value'])
                st.write(df_1)








    except ConnectionError as e:
        st.error("The APP has failed to connect please check your connection 😥")


def main():
    config()
    with st.sidebar:
        choice = option_menu("Main Menu", ["Home", 'Other Tab'], icons=['house', 'list-task'], menu_icon="cast",
                             default_index=0)

    home() if (choice == "Home") else other_tab()


if __name__ == '__main__':
    main()
