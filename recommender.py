import os
import streamlit as st
from icecream import ic
import pandas as pd

DATABASE_ID = "bfad3d3f2560497e9e2c60d4790ad2f7"
NOTION_URL = 'https://api.notion.com/v1/databases/'

import requests

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token= st.secrets["notion_token"]):

        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": f"Bearer {integration_token}", "Notion-Version": "2022-06-28"})
        if response.status_code != 200:
            # raise ApiError(f'Response Status: {response.status_code}')
            print(f'### Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        return list(data_json["results"][0]["properties"].keys())

    def get_projects_data(self,data_json,projects):
        res = {}
        projects_data = {}
        for p in projects:
            if p == 'Name':
                projects_data['Name'] = [data_json["results"][i]["properties"]['Name']['title']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'URL':
                projects_data['URL'] = [data_json["results"][i]["properties"]['URL']['url']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Status':
                projects_data['Status'] = [data_json["results"][i]["properties"]['Status']['status']['name']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Area':
                projects_data['Area'] = [data_json["results"][i]["properties"]['Area']['multi_select']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Notes':
                # ic(data_json["results"][0]["properties"]['Notes'])
                projects_data['Notes'] = [data_json["results"][i]["properties"]['Notes']['rich_text']
                                    for i in range(len(data_json["results"]))]
                
        res['Name'] = [projects_data['Name'][j][0]['plain_text'] for j in range(len(projects_data['Name']))]

        temp = []
        for j in range(len(projects_data['Area'])):
            temp.append([projects_data['Area'][j][k]['name'] for k in range(len(projects_data['Area'][j]))])
        res['Area'] = [','.join(temp[j]) for j in range(len(temp))]

        res['URL'] = [projects_data['URL'][j] for j in range(len(projects_data['URL']))]

        temp = []
        for j in range(len(projects_data['Notes'])):
            temp.append([projects_data['Notes'][j][k]['text']['content'] for k in range(len(projects_data['Notes'][j]))])
        ic(temp)
        res['Notes'] = [','.join(temp[j]) for j in range(len(temp))]

        res['Status'] = [projects_data['Status'][j] for j in range(len(projects_data['Status']))]
        
        
        
        return pd.DataFrame(res).drop(columns='Status')
    
def get_sample(df, n=5):
    return df.sample(min(n, len(df)))

def get_recommendation(n=5):
    nsync = NotionSync()
    data = nsync.query_databases()
    projects = nsync.get_projects_titles(data)
    print(projects)
    df = nsync.get_projects_data(data,projects)
    return get_sample(df, n=n)

# ic(get_recommendation(30))