#README#
###Author: R.Nandhini
##TableofContents
#Background
#set up
#Tech stack
## Title of the project
Windstream special project

### Background
This project has the following requirements:

# Build a python script to read the resources list and create the excel tabs based on the API responses for each of the resources in the list
### The list of resources given
#'collections',
#'events',
#'workflows',
#'handlers',
#'roles',
#'role_permission_assignments',
#'analysis',
#'attribute_types',
#'workflow_status',
#'asset_types',
#'project_types',
#'custom_attributes',
#'workflow_status_events',
#'questionnaires',
#'tables',
#'asset_record_types'
#input:
API access credentials such as access token, Org_id, base url
API responses from org level resources and also from its nested resources
#output:
#Excel sheet which contain all the resources as tab names and its responses as fields names

The python script has been developed completely based on Highbond API documentation.The relationship between the resources are been cross checked with API documentation and created the treestructure based on the API documentation.
https://docs-apis.highbond-s1.com/public.html

Pros:

1.Resources dependencies can be Completely configurable by tree structure based on the use cases
2. Works well for the forst level requirements given to me
3. This is basic version can be improved as and when the requirements are changing 

Cons:
1. Testing has not been completed-In progress

Note: Edge cases has to be given as "special outliers  cases" as part of the requirements. 

#Time taken:
##4 working days
## Tech-stack
#Python
#windows
#excel reader
#API response
#excel writer
## setup
Run the requirenets.txt to set up the dependencies in your local machine

Summary: 
This version of code blocks works well with intial requirements given to me on June 29,2021. It takes 2 working days to fix the api call  bugs. After the intial first level meeting with John, few bugs were noted down. The next version fixes all bugs and cross checked with APi responses and captured those responses as rows and columns in excel sheet.






