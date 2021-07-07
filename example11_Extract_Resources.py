#import the libraries
import pandas as pd
import requests
import os
import json
import datetime

#org_id = input("Enter org id: ")
org_id =31996    #13450#30852# 30850#10657#10637#1001101#
#token = input("Enter token: ")
# nandhini's token
token = "416397dec3833402268b291098de2972bba1c481914d95981428e90ac1c56d6a"#"c259e0648ff961cf604d5125d63adccd69ca19b8f36fd954a8705f3f8e29e483" #"134032dd8518112aaa4193f15a1cea6370c3ddd1f3f62d6bcd988e2f8164c3c5"# "e898c0f331c065595c5c8e1a890864bec93d7e99b3f20e66b7d26708854ed27e"#          
#set API URL
basepath = 'https://apis.highbond.com/v1/'#'https://apis.highbond-s2.com/v1/'#'https://apis.highbond-s1.com/v1/'#'https://apis.highbond-s2.com/v1/'#

# List of resources to make an API GET request for
# resources = ['asset_types', 'attribute_types', 'collections', 'events', 'workflows', 'handlers', 'project_types', 'frameworks', 'entities', 'roles', 'system_users','template_toolkits']
resource_names =  ['collections',
                  'events',
                  'workflows',
                  'handlers',
                  'roles',
                  #'role_permission_assignments',
                  #'analyses',
                  'asset_types',
                  'attribute_types',
                  #'workflow_status',
                  'project_types',
                  'entities',
                  'record_types',
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
excel_filename = 'excel_resources_13549.xlsx'
excel_file = os.path.join(excel_path, excel_filename)
# Create an pandas excel writer based on xlsxwriter.
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

# Function to iterate through list of resources to make an API call for their data.
def export_resources(resource):
    for i in resource:
        endpoint = basepath + '/orgs/'+str(org_id) + '/{0}'.format(i)    # Create URL iterating through list of resources.
        print(endpoint)
        resp = requests.get(endpoint, headers = { 'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
        print(resp)
          # Prepare the URL and make the GET API call.
        if resp == None or resp =='':
            print('It is None')
        else:
            #json1 = resp.json() # Convert to json response.
            #response_dict = json1   # Convert response to a dictionary.
            response_dict = resp.json()
            
            analyses_df = pd.json_normalize(response_dict['data'])   # Normalize the json dict using "data" as the key.
            #analyses_df['test_col'] = (basepath+'orgs/'+str(org_id)+'/'+analyses_df['type']+'/'+analyses_df['id'])
            analyses_df.to_excel(writer, sheet_name= i, index=False) # Write dataframe to Excel.
            #print(analyses_df)

# calls export_resources function.
export_resources(resource_names)

writer.save()
