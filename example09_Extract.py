#import the libraries
import pandas as pd
import requests
import os
import json
import datetime

#org_id = input("Enter org id: ")
org_id =13549#30888#30852# 30850#10657#10637#1001101#
#token = input("Enter token: ")
token = "21e299e3ec2057b5c6b653a774f517c84a21629c8bc6932801ed2d8a6e9ab3d0"#"c259e0648ff961cf604d5125d63adccd69ca19b8f36fd954a8705f3f8e29e483" #"134032dd8518112aaa4193f15a1cea6370c3ddd1f3f62d6bcd988e2f8164c3c5"# "e898c0f331c065595c5c8e1a890864bec93d7e99b3f20e66b7d26708854ed27e"#          
#set API URL
basepath = 'https://apis.highbond.com/v1/'#'https://apis.highbond-s2.com/v1/'#'https://apis.highbond-s1.com/v1/'#'https://apis.highbond-s2.com/v1/'#

# List of resources to make an API GET request for
# resources = ['asset_types', 'attribute_types', 'collections', 'events', 'workflows', 'handlers', 'project_types', 'frameworks', 'entities', 'roles', 'system_users','template_toolkits']
resource_names = ['collections',
                  'events',
                  'workflows',
                  'handlers',
                  'roles',
                  #'role_permission_assignments',
                  #'analysis',
                  'attribute_types',
                  'workflow_status',
                  'asset_types',
                  #'project_types',
                  #'custom_attributes',
                  #'workflow_status_events',
                  #'questionnaires',
                  #'tables',
                  #'asset_record_types',
                  ]

root_path = 'terraform_results'
excel_path = root_path+'/excel_resources'
os.makedirs(root_path, exist_ok=True)
os.makedirs(excel_path, exist_ok=True)

# Filename of the Excel file to create. 
excel_filename = 'excel_resources_post_itrm_fail.xlsx'
excel_file = os.path.join(excel_path, excel_filename)
# Create an pandas excel writer based on xlsxwriter.
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

# Function to iterate through list of resources to make an API call for their data.
def export_resources(resource):
    for i in resource:
        endpoint = basepath + '/orgs/'+str(org_id) + '/{0}'.format(i)    # Create URL iterating through list of resources.
        resp = requests.get(endpoint, headers = { 'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })  # Prepare the URL and make the GET API call.
        if resp == None or resp =='':
            print('It is None')
        else:
            #json1 = resp.json() # Convert to json response.
            #response_dict = json1   # Convert response to a dictionary.
            response_dict = resp.json()
            collection_analyses_df = pd.json_normalize(response_dict['data'])   # Normalize the json dict using "data" as the key.
            collection_analyses_df['test_col'] = (basepath+'orgs/'+str(org_id)+'/'+collection_analyses_df['type']+'/'+collection_analyses_df['id'])
            collection_analyses_df.to_excel(writer, sheet_name= i, index=False) # Write dataframe to Excel.
            #print(collection_analyses_df)

# Function to create collection_id list. Used in for i in collection_ids.
endpoint = basepath + "/orgs/"+str(org_id) + "/attribute_types/"
resp = requests.get(endpoint, headers = { 'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
json1 = resp.json() #last step converts to json.
json_response_dict = json1  # Convert response to a dictionary.
# print(json_response_dict.keys())  # this print will tell you what branches in your json are available.
attribute_types_df = pd.json_normalize(json_response_dict["data"])  # this normalizes the dict into a dataframe.
attribute_type_ids = attribute_types_df['id'].to_list() # select a column as series and then convert it into a column.
print('Attribute_Type IDs: ', attribute_type_ids)


# Function to create collection_id list. Used in for i in collection_ids.
endpoint = basepath + "/orgs/"+str(org_id) + "/asset_types/"
resp = requests.get(endpoint, headers = { 'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
json1 = resp.json() #last step converts to json.
json_response_dict = json1  # Convert response to a dictionary.
# print(json_response_dict.keys())  # this print will tell you what branches in your json are available.
asset_types_df = pd.json_normalize(json_response_dict["data"])  # this normalizes the dict into a dataframe.
asset_type_ids = asset_types_df['id'].to_list() # select a column as series and then convert it into a column.
print('Asset IDs: ', asset_type_ids)

#for i in asset_type_ids:
#        for x in attribute_type_ids:
#            pair = basepath + "/orgs/"+str(org_id) + "/asset_types/"+i+"/attribute_types/"+x
#            print(pair)
        
# Initialize a blank list for holding the list of dataframes
asset_type_attribute_type_df_list = []

# Loop through the analyses lists and gets the table IDs into their own dataframes.
for i in asset_type_ids:
    endpoint1 = basepath + "orgs/" + str(org_id) + "/asset_types/{0}/attribute_types/".format(i)
    resp = requests.get(endpoint1, headers = { 'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
    json1 = resp.json()
    response_dict = json1
    asset_type_attribute_type_df = pd.json_normalize(response_dict["data"])
    asset_type_attribute_type_df['asset_type_id'] = i
    asset_type_attribute_type_df['delete_url'] = (basepath+'orgs/'+str(org_id)+ "/asset_types/{0}/attribute_types".format(i)+'/'+asset_type_attribute_type_df['id'])
    asset_type_attribute_type_df_list.append(asset_type_attribute_type_df)    

# Concatenate (append) all the dataframes in the list
all_tables_df = pd.concat(asset_type_attribute_type_df_list, ignore_index=True)
all_tables_df.to_excel(writer, sheet_name= 'Asset_Attribute', index=False)   # Write dataframe to Excel
#print(all_tables_df['delete_url'])

headers = {
    "cookie": "visitor_id=e5fd6287c2f9a6811036366e2e567ebe; _skynet_server_session=SUwQ8bLMJkrGm82a366xTvmK5xupeptui6XYc2FwEXGdNZJ17lau7kxdNylCwXod9kwHhh8BeILO82%252FMkH5sgouF95UYU%252Bc06GOLgqo0zUNzB35jk6eNSKEqj9k0qWby4jM%252F3sp21g%253D%253D--wUxLTIAI%252Fgyly55z--ptoAtJn2jDsEjYiBr3psjg%253D%253D; XSRF-TOKEN=I3RnjoOwEirO6U8nIV6HpA4mcf6FmRziFRw7yALJKAC5%252Fgua%252FFiet%252F3jDb8Y3TBe1GAQkvrQCoIBsDeme4S6HQ%253D%253D; _results_session=ZEZibkhPd29RRE1nMk9iQjdLOER3K1ZZeDVRcWRjWjhjaU1ySXIzTzFKTmZsaFB5SjBwUkRyYVgzTUFncGNiUWtFR2J1QWU5ZnZKVVp6L050VGhxTERycVdqMEMwRk1CNzhKaXdwRjk1bGRTWTdBYTJhTEpPaE9seTFxK0E0VmRZVTRKTFhaUndZMGdXeFhFKzRza1RTL29vQ2dxSVFzTnRMbVV4Uk9IUC9xTTRKYms5bXlMam5sQk9TSnJRYTI4SlR2VFZkNlBSQWJHVDVHVEdkZDJyQT09LS1oOG51SDE5bjhUTzc5dUtVT0gvaTdBPT0%253D--ba64c1b5d24d3ce2795aaf39e89db41356aa8689",
    "Content-Type": "application/vnd.api+json",
    "Authorization": "Bearer 21e299e3ec2057b5c6b653a774f517c84a21629c8bc6932801ed2d8a6e9ab3d0"
}

#for i in all_tables_df['delete_url']:
#    response = requests.request("DELETE", i, headers=headers)

# calls export_resources function.
export_resources(resource_names)

writer.save()
