import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import pickle
import os
from PIL import Image
from sklearn.preprocessing import StandardScaler
import io
import plotly.express as px
import plotly.graph_objs as go

# loading the trained model
#with open(r'C:\Users\Catherine\Credit\classifier.pkl', 'rb') 
current_path = os.getcwd()
credit_path = os.path.join(current_path, 'classifier.pkl')
with open(credit_path, 'rb') as handle:
    model = pickle.load(handle)

########################################################
# Loading images to the website
########################################################
image = Image.open("images/credit.jpg")

def prediction(X):
    prediction = model.predict(X)
    return prediction 

def main_page():
    st.markdown("# Main page 🎈")
    st.title('Bienvenue sur Octroi de crédit !')
    
    def chargement_data(path):
        dataframe = pd.read_csv(path)
        liste_id = dataframe['SK_ID_CURR'].tolist()
        return dataframe, liste_id
      
    st.sidebar.markdown("# Main page 🎈")
    
    st.subheader("Prédictions de scoring client et positionnement dans l'ensemble des clients")

    examples_file = 'df1.csv'
    dataframe, liste_id = chargement_data(examples_file)

    st.sidebar.image(image)
    st.sidebar.markdown("🛰️ **Navigation**")

    id_input = st.sidebar.selectbox(
        'Choisissez le client que vous souhaitez visualiser',
        liste_id)

    client_infos = dataframe[dataframe['SK_ID_CURR'] == id_input].drop(
        ['SK_ID_CURR'], axis=1)
    #client_infos = client_infos.to_dict('record')[0]
    client_infos.to_dict(orient = 'records')
    
    result =""
    
    #if st.sidebar.button("Predict"):
    X1 = dataframe[dataframe['SK_ID_CURR'] == id_input]    
    X = X1[['CODE_GENDER', 
        'AGE',
        'CNT_CHILDREN', 
        'DEF_30_CNT_SOCIAL_CIRCLE',
         'NAME_EDUCATION_TYPE_High education',  
         'NAME_EDUCATION_TYPE_Low education',  
         'NAME_EDUCATION_TYPE_Medium education',  
         'ORGANIZATION_TYPE_Construction',  
         'ORGANIZATION_TYPE_Electricity',  
         'ORGANIZATION_TYPE_Government/Industry',  
         'ORGANIZATION_TYPE_Medicine',  
         'ORGANIZATION_TYPE_Other/Construction/Agriculture',  
         'ORGANIZATION_TYPE_School',  
         'ORGANIZATION_TYPE_Services',  
         'ORGANIZATION_TYPE_Trade/Business', 
         'OCCUPATION_TYPE_Accountants/HR staff/Managers', 
         'OCCUPATION_TYPE_Core/Sales staff',  
         'OCCUPATION_TYPE_Laborers',  
         'OCCUPATION_TYPE_Medicine staff',  
         'OCCUPATION_TYPE_Private service staff' , 
         'OCCUPATION_TYPE_Tech Staff',
         'NAME_FAMILY_STATUS',
          'AMT_INCOME_TOTAL',
          'INCOME_CREDIT_PERC',
          'DAYS_EMPLOYED_PERC',
          'EXT_SOURCE_1',
          'EXT_SOURCE_2',    
          'EXT_SOURCE_3']]
        
    result = prediction(X)
        
    if result == 1:
        if int(X1['TARGET']) == 1: 
             pred = 'Rejected (True Negative)'
        else:
             pred = 'Approved (False Negative)'
    else:
        if int(X1['TARGET']) == 1:
             pred = 'Rejected (False Positive)'
        else:
             pred = 'Approved (True Positive)'              
                   
    st.success('Your loan is {}'.format(pred))

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

my_dict = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

keys = list(my_dict.keys())

selected_page = st.sidebar.selectbox("Select a page", keys)
my_dict[selected_page]()