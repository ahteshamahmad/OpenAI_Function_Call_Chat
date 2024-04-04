import argparse
from jira import JIRA
import base64
import os
import requests
import time
import json
import xml.etree.ElementTree as ET
import shutil

# Jira API details
JIRA_URL = "https://md-ahtesham-ahmad.atlassian.net"
JIRA_USERNAME = "ahtesham.ahmad2018@gmail.com"
JIRA_API_TOKEN = os.getenv("Jira_API_Token")
JENKINS_URL = 'http://localhost:8080'
JENKINS_USERNAME = 'ahtesham'
JENKINS_PASSWORD = os.getenv('MyJenkins_API_Tokens')
TEAMCITY_URL = 'https://ahtesham.teamcity.com'
TEAMCITY_USERNAME = 'ahtesham'
TEAMCITY_PASSWORD = os.getenv('Teamcity_API_Token')


# Encode credentials to use in the Authorization header
credentials = f"{JIRA_USERNAME}:{JIRA_API_TOKEN}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
auth = (JIRA_USERNAME, JIRA_API_TOKEN)

# Create Jira connection
jira = JIRA(server=JIRA_URL, basic_auth=auth)


def list_all_functions():
    jira_functions = [
        "search_jira_issues",
        "create_jira_issue",
        "update_jira_issue",
        "check_jira_issue_status",
        "create_jira_project",
        "fetch_jira_project",
        "update_jira_project",
        "add_comment_to_issue",
        "change_assignee"
    ]
    Jenkins_functions = [
        "create_jenkins_job",
        "retrieve_jenkins_job_configuration",
        "delete_jenkins_job",
        "retrieve_jenkins_job_information",
        "disable_jenkins_job",
        "enable_jenkins_job",
        "trigger_jenkins_build",
        "retrieve_jenkins_build_information",
        "retrieve_jenkins_console_output",
        "stop_jenkins_build",
        "retrieve_jenkins_queue_information",
        "retrieve_jenkins_queue_item_information",
        "list_jenkins_projects",
        "count_jenkins_jobs"
    ]
    Teamcity_functions = [
        "create_teamcity_project",
        "list_teamcity_projects",
        "list_teamcity_build_configurations",
        "get_teamcity_build_status",
        "get_teamcity_build_details",
        "cancel_teamcity_build",
        "get_teamcity_agent_details",
        "get_teamcity_agent_pools",
        "get_teamcity_build_artifacts",
        "list_teamcity_agents",
        "trigger_build"
    ]
    all_functions = jira_functions + Jenkins_functions + Teamcity_functions
    return all_functions

def create_jira_project():
    try:
        project_name = "OPEN_AI_APP_NSEIT"
        project_key = "NOAAP"
        
        existing_projects = jira.projects()
        for project in existing_projects:
            if project.name == project_name:
                return f"Project '{project_name}' already exists."

        project_dict = {
            "key": project_key,
            "name": project_name,
        }
        
        new_project = jira.create_project(**project_dict)
        return f"Project created successfully! Key: {new_project.key}"
    except Exception as e:
        if "Changing permission schemes is not allowed" in str(e):
            return "Project created successfully, but some configurations may be restricted by the current Jira plan."
        else:
            return f"Error creating project: {str(e)}"

def fetch_jira_project():
    try:
        project_key = "HACKPROJ"
        project = jira.project(project_key)
        return f"Project Details - Key: {project.key}, Name: {project.name}"
    except Exception as e:
        return f"Error fetching project: {str(e)}"

def update_jira_project():
    try:
        project_key = "HACKPROJ"
        new_name = "OpenAI_Project"
        
        project = jira.project(project_key)
        project.update(name=new_name)
        
        return f"Project updated successfully! New Name: {project.name}"
    except Exception as e:
        return f"Error updating project: {str(e)}"

def create_jira_issue():
    try:
        project_key = "ONP"
        issue_type = "Task"
        summary = "OpenAI_Project for NSEIT"
        description = "This is Open AI Project"

        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        new_issue = jira.create_issue(fields=issue_dict)
        return f"Issue created successfully! Key: {new_issue.key}"
    except Exception as e:
        return f"Error creating issue: {str(e)}"

def search_jira_issues():
    try:
        jql_query = "project = HACKPROJ AND issuetype = task"
        max_results = "10"
        issues = jira.search_issues(jql_query, maxResults=max_results)
        for issue in issues:
            return f"Key: {issue.key}, Summary: {issue.fields.summary}, Type: {issue.fields.issuetype.name}"
    except Exception as e:
        return f"Error searching issues: {str(e)}"
        
def update_jira_issue():
    try:
        issue_key = "ONP-2"
        new_summary = "OpenAI-Hackathon-Project"
        new_description = "This issue is for testing"
        new_workflow_status = "In Review"  # New workflow status
        
        issue = jira.issue(issue_key)
        
        # Get transition ID for the desired status
        transition_id = None
        transitions = jira.transitions(issue)
        for transition in transitions:
            if transition['to']['name'] == new_workflow_status:
                transition_id = transition['id']
                break
        
        if transition_id:
            # Perform the transition and update fields
            jira.transition_issue(issue, transition_id)
            issue.update(
                summary=new_summary,
                description=new_description,
            )
            return f"Issue updated successfully! New Summary: {issue.fields.summary}, New Description: {issue.fields.description}, New Workflow Status: {new_workflow_status}"
        else:
            return f"Could not find transition for the status: {new_workflow_status}"
    except jira.JIRAError as e:
        return f"Error updating issue: {e.text}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def add_comment_to_issue():
    issue_key="HACKPROJ-1"
    comment_body = "This is a test comment."
    response = {
        "success": False,
        "message": ""
    }
    try:
        issue = jira.issue(issue_key)
        jira.add_comment(issue, comment_body)
        response["success"] = True
        response["message"] = "Comment added successfully!"
    except Exception as e:
        response["message"] = f"Unexpected error: {str(e)}"
    
    return json.dumps(response)

def change_assignee():
    new_assignee="ahtesham.ahmad2018@gmail.com"
    issue_key = "ONP-2"

    try:
        # Initialize JIRA client
        jira = JIRA(
            server=JIRA_URL,
            basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN)
        )

        # Get the issue
        issue = jira.issue(issue_key)

        # Update the assignee
        if new_assignee.lower() == "unassigned":
            issue.update(assignee=None)
            print(f"Assignee for issue {issue_key} set to unassigned successfully.")
            return True
        else:
            # Search for user by email
            user = jira.search_users(query=new_assignee)
            if user:
                assignee_account_id = user[0].accountId
                issue.update(assignee={"accountId": assignee_account_id})
                print(f"Assignee for issue {issue_key} updated to {new_assignee} successfully.")
                return True
            else:
                print(f"User with email {new_assignee} not found.")
                return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def check_jira_issue_status():
    try:
        issue_key = "HACKPROJ-1"
        issue = jira.issue(issue_key)
        status = issue.fields.status.name
        return f"Status for issue {issue_key}: {status}"
    except Exception as e:
        return f"Error checking issue status: {str(e)}"

def create_jenkins_job():
    job_name="OpenAI_Job"
    job_config = """
        <project>
            <builders>
                <hudson.tasks.batch>
                    <command>echo 'Hello, Jenkins!'</command>
                </hudson.tasks.batch>
            </builders>
        </project>
    """
    url = f'{JENKINS_URL}/createItem?name={job_name}'
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(url, data=job_config, headers=headers, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
        response.raise_for_status()  # Raise an error for non-200 status codes
        time.sleep(5)  # Optional: Add a delay if necessary
        return f"Job '{job_name}' created successfully."
    except requests.exceptions.RequestException as e:
        return f"Failed to create job '{job_name}': {e}"

def count_jenkins_jobs():
    try:
        url = f'{JENKINS_URL}/api/json'
        response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
        if response.status_code == 200:
            data = response.json()
            num_jobs = len(data['jobs'])
            return f"Total number of jobs in Jenkins: {num_jobs}"
        else:
            return f"Failed to retrieve Jenkins projects. Status code: {response.status_code}"
    except Exception as e:
        return f"Error retrieving Jenkins projects: {str(e)}"

def list_jenkins_projects():
    try:
        url = f'{JENKINS_URL}/api/json'
        response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
        if response.status_code == 200:
            data = response.json()
            project_names = [job['name'] for job in data['jobs']]
            return project_names
        else:
            return f"Failed to retrieve Jenkins projects. Status code: {response.status_code}"
    except Exception as e:
        return f"Error retrieving Jenkins projects: {str(e)}"

def retrieve_jenkins_job_configuration():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/config.xml'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve configuration for job '{job_name}'. Status code: {response.status_code}"

def delete_jenkins_job():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/doDelete'
    response = requests.post(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return f"Job '{job_name}' deleted successfully."
    else:
        return f"Failed to delete job '{job_name}'. Status code: {response.status_code}"

def retrieve_jenkins_job_information():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/api/json'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return json.dumps(response.json())  # Convert JSON object to string
    else:
        return f"Failed to retrieve information for job '{job_name}'. Status code: {response.status_code}"

def disable_jenkins_job():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/disable'
    response = requests.post(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return f"Job '{job_name}' disabled successfully."
    else:
        return f"Failed to disable job '{job_name}'. Status code: {response.status_code}"

def enable_jenkins_job():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/enable'
    response = requests.post(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return f"Job '{job_name}' enabled successfully."
    else:
        return f"Failed to enable job '{job_name}'. Status code: {response.status_code}"
    
def trigger_jenkins_build():
    job_name="my_new_job"
    url = f'{JENKINS_URL}/job/{job_name}/build'
    response = requests.post(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 201:
        return f"Build triggered successfully for job '{job_name}'"
    else:
        return f"Failed to trigger build for job '{job_name}'. Status code: {response.status_code}"

def retrieve_jenkins_build_information():
    job_name="my_new_job"
    build_number="1"
    url = f'{JENKINS_URL}/job/{job_name}/{build_number}/api/json'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return f"Failed to retrieve build information for job '{job_name}', build number '{build_number}'. Status code: {response.status_code}"

def retrieve_jenkins_console_output():
    job_name="my_new_job"
    build_number="1"
    url = f'{JENKINS_URL}/job/{job_name}/{build_number}/consoleText'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve console output for job '{job_name}', build number '{build_number}'. Status code: {response.status_code}"

def stop_jenkins_build():
    job_name="my_new_job"
    build_number="1"
    url = f'{JENKINS_URL}/job/{job_name}/{build_number}/stop'
    response = requests.post(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return f"Build '{build_number}' stopped successfully for job '{job_name}'."
    else:
        return f"Failed to stop build '{build_number}' for job '{job_name}'. Status code: {response.status_code}"

def retrieve_jenkins_queue_information():
    url = f'{JENKINS_URL}/queue/api/json'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return f"Failed to retrieve queue information. Status code: {response.status_code}"

def retrieve_jenkins_queue_item_information():
    queue_item_id="4"
    url = f'{JENKINS_URL}/queue/item/{queue_item_id}/api/json'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return f"Failed to retrieve queue item information for id '{queue_item_id}'. Status code: {response.status_code}"

def create_teamcity_project():
    project_name = "Aht_Project"
    parent_project_id = None
    
    try:
        response = requests.post(
            f"{TEAMCITY_URL}/httpAuth/app/rest/projects",
            auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD),
            headers={"Content-Type": "application/json"},
            json={"name": project_name, "description": "New Open AI project created via API"}
        )

        if response.status_code == 200:
            return f"Project '{project_name}' created successfully!"
        else:
            return f"Error creating project: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {e}"



def list_teamcity_projects():
    try:
        response = requests.get(f"{TEAMCITY_URL}/httpAuth/app/rest/projects", auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  

        # Parse XML response
        root = ET.fromstring(response.content)
        projects = root.findall('project')
        project_names = [project.attrib['name'] for project in projects]
        return json.dumps(project_names)
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None

#Function to list build configurations for a project
def list_teamcity_build_configurations():
    url = f"{TEAMCITY_URL}/httpAuth/app/rest/buildTypes"
    response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
    
    if response.status_code == 200:
        if response.headers.get('Content-Type') == 'application/xml':
            root = ET.fromstring(response.content)
            build_types = root.findall('buildType')
            configurations = []
            for build_type in build_types:
                name_element = build_type.find('name')
                if name_element is not None:
                    name = name_element.text
                    id = build_type.attrib.get('id')
                    configurations.append((name, id))
                else:
                    id = build_type.attrib.get('id')
                    configurations.append((f"Unnamed Build Type (ID: {id})", id))
            return configurations
        elif response.headers.get('Content-Type') == 'application/json':
            build_types = response.json().get('buildType', [])
            return [(build_type.get('name', f"Unnamed Build Type (ID: {build_type['id']})"), build_type['id']) for build_type in build_types]
        else:
            return None
    else:
        return None

# # Function to get build status
def get_teamcity_build_status():
    build_id=16
    url = f"{TEAMCITY_URL}/httpAuth/app/rest/builds/id:{build_id}"
    try:
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        root = ET.fromstring(response.content)
        status = root.attrib.get('status')
        if status:
            return status
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# # Function to get build details
def get_teamcity_build_details():
    build_id=16
    url = f"{TEAMCITY_URL}/app/rest/builds/id:{build_id}"
    try:
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        root = ET.fromstring(response.content)
        agent_id_element = root.find(".//agent")
        agent_id = agent_id_element.attrib.get("id") if agent_id_element is not None else "Unknown"
        build_details = {
            "id": root.attrib.get("id"),
            "buildTypeId": root.attrib.get("buildTypeId"),
            "number": root.attrib.get("number"),
            "status": root.attrib.get("status"),
            "state": root.attrib.get("state"),
            "branchName": root.attrib.get("branchName"),
            "defaultBranch": root.attrib.get("defaultBranch"),
            "webUrl": root.attrib.get("webUrl"),
            "statusText": root.find("statusText").text,
            "queuedDate": root.find("queuedDate").text,
            "startDate": root.find("startDate").text,
            "finishDate": root.find("finishDate").text,
            "agentId": agent_id,
            # Add other fields as needed
        }
        return json.dumps(build_details)
    except requests.exceptions.RequestException as e:
        return None

def cancel_teamcity_build():
    build_id=16
    try:
        url = f"{TEAMCITY_URL}/app/rest/builds/{build_id}"
        response = requests.delete(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        
        if response.status_code == 200 or response.status_code == 204:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

# Function to get agent details
def get_teamcity_agent_details():
    agent_name = "Ahtesham_windows_agent"
    url = f"https://ahtesham.teamcity.com/app/rest/agents/name:{agent_name}"
    
    try:
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    except requests.RequestException as e:
        return None
    
    if response.status_code != 200:
        return None
    
    try:
        agent_info = response.content.decode("utf-8")
        root = ET.fromstring(agent_info)
    except ET.ParseError as e:
        return None
    
    agent_details = {
        "Agent ID": root.attrib.get("id", ""),
        "Agent Name": root.attrib.get("name", ""),
        "Connected": root.attrib.get("connected", ""),
        "Enabled": root.attrib.get("enabled", ""),
        "Authorized": root.attrib.get("authorized", ""),
        "Last Communication IP": root.attrib.get("ip", "")
    }
    
    return json.dumps(agent_details)

# Function to get agent pools
def get_teamcity_agent_pools():
    url = f"{TEAMCITY_URL}/app/rest/agentPools"
    try:
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        root = ET.fromstring(response.content)
        agent_pools = [pool.attrib['name'] for pool in root.findall('agentPool')]
        return json.dumps(agent_pools)
    except requests.exceptions.RequestException as e:
        return None
    
def get_teamcity_build_artifacts():
    build_id=9
    try:
        url = f"{TEAMCITY_URL}/app/rest/builds/{build_id}/artifacts/"
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception if response status code is not 2xx

        artifact_paths = []

        # Parse XML response
        root = ET.fromstring(response.content)
        for file_elem in root.findall('.//file'):
            artifact_paths.append(file_elem.attrib['name'])
        return artifact_paths
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching build artifacts: {e}")


# # Function to get the list of all agents
def list_teamcity_agents():
    url = f"{TEAMCITY_URL}/app/rest/agents"
    try:
        response = requests.get(url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        root = ET.fromstring(response.content)
        agents = [agent.attrib['name'] for agent in root.findall('agent')]
        return json.dumps(agents)
    except requests.exceptions.RequestException as e:
        return None

def trigger_build():
    build_type_id="OpenAIProject_Build"
    try:
        response = requests.post(
            f"{TEAMCITY_URL}/app/rest/buildQueue",
            auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD),
            headers={"Content-Type": "application/xml"},
            data=f'<build><buildType id="{build_type_id}"/></build>'
        )

        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions for Jira operations.")
    parser.add_argument(
        "operation",
        choices=["create_jenkins_job","retrieve_jenkins_job_configuration","delete_jenkins_job","retrieve_jenkins_job_information","disable_jenkins_job","enable_jenkins_job","trigger_jenkins_build","retrieve_jenkins_build_information","retrieve_jenkins_console_output","stop_jenkins_build","retrieve_jenkins_queue_information","retrieve_jenkins_queue_item_information","list_all_functions","search_jira_issues", "create_jira_issue", "update_jira_issue", "jira_issue_status", "create_jira_project", "fetch_jira_project", "update_jira_project", "create_teamcity_project", "list_teamcity_projects", "list_teamcity_build_configurations", "get_teamcity_build_status", "get_teamcity_build_details", "cancel_teamcity_build", "get_teamcity_agent_details", "get_teamcity_agent_pools", "get_teamcity_build_artifacts", "list_teamcity_agents"],
        help="Specify operation to perform (Get/Post/Put/Delete)",
    )

    args = parser.parse_args()

    if args.operation == "search_jira_issues":
        search_jira_issues()
    elif args.operation == "create_jira_issue":
        create_jira_issue()
    elif args.operation == "update_jira_issue":
        update_jira_issue()
    elif args.operation == "issue_jira_status":
        check_jira_issue_status()
    elif args.operation == "create_jira_project":
        create_jira_project()
    elif args.operation == "fetch_jira_project":
        fetch_jira_project()
    elif args.operation == "update_jira_project":
        update_jira_project()
    elif args.operation == "list_all_functions":
        list_all_functions()
    elif args.operation == "create_jenkins_job":
        create_jenkins_job()
    elif args.operation == "retrieve_jenkins_job_configuration":
        retrieve_jenkins_job_configuration()
    elif args.operation == "delete_jenkins_job":
        delete_jenkins_job()
    elif args.operation == "retrieve_jenkins_job_information":
        retrieve_jenkins_job_information()
    elif args.operation == "disable_jenkins_job":
        disable_jenkins_job()
    elif args.operation == "enable_jenkins_job":
        enable_jenkins_job()
    elif args.operation == "trigger_jenkins_build":
        trigger_jenkins_build()
    elif args.operation == "retrieve_jenkins_build_information":
        retrieve_jenkins_build_information()
    elif args.operation == "retrieve_jenkins_console_output":
        retrieve_jenkins_console_output()
    elif args.operation == "stop_jenkins_build":
        stop_jenkins_build()
    elif args.operation == "retrieve_jenkins_queue_information":
        retrieve_jenkins_queue_information()
    elif args.operation == "retrieve_jenkins_queue_item_information":
        retrieve_jenkins_queue_item_information()
    elif args.operation == "list_jenkins_projects":
        list_jenkins_projects()
    elif args.operation == "count_jenkins_jobs":
        count_jenkins_jobs()
    elif args.operation == "create_teamcity_project":
        create_teamcity_project()
    elif args.operation == "list_teamcity_projects":
        list_teamcity_projects()
    elif args.operation == "list_teamcity_build_configurations":
        list_teamcity_build_configurations()
    elif args.operation == "get_teamcity_build_status":
        get_teamcity_build_status()
    elif args.operation == "get_teamcity_build_details":
        get_teamcity_build_details()
    elif args.operation == "cancel_teamcity_build":
        cancel_teamcity_build()
    elif args.operation == "get_teamcity_agent_details":
        get_teamcity_agent_details()
    elif args.operation == "get_teamcity_agent_pools":
        get_teamcity_agent_pools()
    elif args.operation == "get_teamcity_build_artifacts":
        get_teamcity_build_artifacts()
    elif args.operation == "list_teamcity_agents":
        list_teamcity_agents()
    elif args.operation == "trigger_build":
        trigger_build()
    elif args.operation == "add_comment_to_issue":
        add_comment_to_issue()
    elif args.operation == "change_assignee":
        change_assignee()

    else:
        print("Invalid operation. Choose a valid operation.")
