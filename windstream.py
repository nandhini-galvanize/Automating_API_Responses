from pandas import json_normalize
from anytree import Node, RenderTree
import pandas as pd
import requests
import os
import json
org_id=0
token=''
url=''
#print("Enter the org-id", org_id)
#print("Enter your access token",token)
#org_id=int(input("Enter the org-id"))
#token=input("Enter the token")


list_of_resources=['collections','project_types']



def parent_resource_access_credentials():
    #org_id=orgid
    #access_token=token
    org_id=31996
    token="416397dec3833402268b291098de2972bba1c481914d95981428e90ac1c56d6a"
    basepath='https://apis.highbond.com/v1/'
    #url = """{}+{}+{}""".format(org_id, token)
    url=basepath+'orgs/'+str(org_id)
    print(url)
    return url
url_returned=url


def extract_resources_from_api(lst,url_returned):
    list_of_df=[]
    for i in lst:
        api_endpoint= url_returned+'/'+ i
        print(api_endpoint)
        resp = requests.get(api_endpoint, headers = {'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
        print(resp)
        #json_data = resp.json()if resp and resp.status_code == 200 else None
        # resp=json.loads(resp)
        # for item in resp['data']:
        #     ID = item.get("id")
        # print(ID)
        #print(resp.__getattribute__(id))
        #print(resp.getattribute(id)
        # data=resp.text
        
        # parsed = json.loads(data)

        # print(json.dumps(parsed, indent=4))

        # ID = parsed["id"]
        # print(ID)
        
        response_dict = resp.json()
        df_result = pd.json_normalize(response_dict['data'])
        #df_result_id=df_result.loc['id']
        #print(df_result_id)
        print(df_result) 
        list_of_df.append(df_result)
        
        #if the list[i]==collections call build child url("/id/analyses")
        # for i, val in enumerate(lst):
        #     if lst[val]='collections':
        build_child_url(base_url,lst,df_result)
        #call_child_api_endpoint

        #append the df to the list_of_df

        #ifelse the list[i]==analyses call builr child url("/id/table")

        #call_child_api_endpoint

        #append the df to the list_of_df

    return list_of_df

def build_child_url(base_url,lst,df_parent):
   for index, row in df_parent.iterrows(): 
       print(row['id'])
       #{{ _.org_id }}/collections/146418/analyses
    # child_url=base_url+'/'+id+"/analyses"
    # return None




base_url=parent_resource_access_credentials()
list_of_df=extract_resources_from_api(list_of_resources,base_url)

def export_to_excel(lst,list_of_df):
    root_path = 'API_extraction'
    excel_path = root_path+'/excel_resources'
    os.makedirs(root_path, exist_ok=True)
    os.makedirs(excel_path, exist_ok=True)
    excel_filename = 'Extracted_resources_31966.xlsx'
    excel_file = os.path.join(excel_path, excel_filename)
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_list_counter=0
    for i in lst:
      list_of_df[df_list_counter].to_excel(writer, sheet_name= i, index=False)
      df_list_counter+=1
  
    writer.save()



export_to_excel(list_of_resources,list_of_df) 



