import os
import streamlit as st
from icecream import ic
import pandas as pd

DATABASE_ID_1 = "bfad3d3f2560497e9e2c60d4790ad2f7" #Want to go
DATABASE_ID_2 = "9764a07b87724cd8958002017a93df88" #Diary
NOTION_URL = 'https://api.notion.com/v1/databases/'

import requests

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self, database_id = DATABASE_ID_1, integration_token= st.secrets["notion_token"]):
        database_url = NOTION_URL + database_id + "/query"
        response = requests.post(database_url, headers={"Authorization": f"Bearer {integration_token}", "Notion-Version": "2022-06-28"})
        if response.status_code != 200:
            print(f'### Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        return list(data_json["results"][0]["properties"].keys())

    def get_to_go_data(self, data_json, projects):
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
        res['Area'] = [', '.join(temp[j]) for j in range(len(temp))]

        res['URL'] = [projects_data['URL'][j] for j in range(len(projects_data['URL']))]

        temp = []
        for j in range(len(projects_data['Notes'])):
            temp.append([projects_data['Notes'][j][k]['text']['content'] for k in range(len(projects_data['Notes'][j]))])
        ic(temp)
        res['Notes'] = [', '.join(temp[j]) for j in range(len(temp))]
        res['Status'] = [projects_data['Status'][j] for j in range(len(projects_data['Status']))]
        
        return pd.DataFrame(res)
    
    def get_diary_data(self, data_json, projects):
        res = {}
        projects_data = {}
        for p in projects:
            if p == 'Name':
                projects_data['Name'] = [data_json["results"][i]["properties"]['Name']['title']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Date':
                # ic(data_json["results"][0]["properties"]['Notes'])
                projects_data['Date'] = [data_json["results"][i]["properties"]['Date']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Area':
                projects_data['Area'] = [data_json["results"][i]["properties"]['Area']['multi_select']
                                    for i in range(len(data_json["results"]))]
                
            if p == 'Notes':
                projects_data['Notes'] = [data_json["results"][i]["properties"]['Notes']['rich_text']
                                    for i in range(len(data_json["results"]))]
                
        ic(projects_data['Date'][0])
        res['Name'] = [projects_data['Name'][j][0]['plain_text'] for j in range(len(projects_data['Name']))]
        res['Date'] = [projects_data['Date'][j]['date']['start'] for j in range(len(projects_data['Date']))]
        temp = []
        for j in range(len(projects_data['Area'])):
            temp.append([projects_data['Area'][j][k]['name'] for k in range(len(projects_data['Area'][j]))])
        res['Area'] = [', '.join(temp[j]) for j in range(len(temp))]
        res['Notes'] = [', '.join(temp[j]) for j in range(len(temp))]

        return pd.DataFrame(res)
    
    

def get_sample(df, n=5):
    return df.sample(min(n, len(df)))

def get_recommendation(n=5, new_place = False):
    nsync = NotionSync()
    data = nsync.query_databases(database_id=DATABASE_ID_1)
    projects = nsync.get_projects_titles(data)
    df1 = nsync.get_to_go_data(data, projects)

    if not new_place:
        data = nsync.query_databases(database_id=DATABASE_ID_2)
        projects = nsync.get_projects_titles(data)
        df2 = nsync.get_diary_data(data, projects)
        df = df1.merge(df2, on='Name', how='outer')
    
        ic(list(df.columns))
        df['Area'] = df.apply(lambda x: x['Area_x'] if pd.notnull(x['Area_x']) else x['Area_y'], axis=1)
        df['Notes'] = df.apply(lambda x: x['Notes_x'] if pd.notnull(x['Notes_x']) else x['Notes_y'], axis=1)

        COLUMNS = list(df1.columns)
        ic(COLUMNS)
        COLUMNS.append('Date')
        df = df[COLUMNS].rename(columns={'Date': 'Last Visited'})

    else:
        df = df1[df1['Status']=='Backlog']

    return get_sample(df, n=n).drop(columns=['Status']), len(df)

# ic(get_recommendation(30))
# print(get_recommendation(new_place=True))