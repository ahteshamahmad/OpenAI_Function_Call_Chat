import argparse
from jira import JIRA
import base64
import os
import requests
import time
import json

# Jira API details
JIRA_URL = "https://md-ahtesham-ahmad.atlassian.net"
JIRA_USERNAME = "ahtesham.ahmad2018@gmail.com"
JIRA_API_TOKEN = os.getenv("Jira_API_Token")
JENKINS_URL = 'http://localhost:8080'
JENKINS_USERNAME = 'ahtesham'
JENKINS_PASSWORD = os.getenv('MyJenkins_API_Tokens')


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
        "update_jira_project"
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
    all_functions = jira_functions + Jenkins_functions
    return all_functions

def create_jira_project():
    try:
        project_name = input("Enter new project name: ")
        project_key = input("Enter new project key: ")
        
        project_dict = {
            "key": project_key,
            "name": project_name,
            "projectTypeKey": "business",
            "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-project-management",
            "description": "New project created via API",
        }
        
        new_project = jira.create_project(**project_dict)
        return f"Project created successfully! Key: {new_project.key}"
    except Exception as e:
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
        project_key = input("Enter project key to update: ")
        new_name = input("Enter new project name: ")
        
        project = jira.project(project_key)
        project.update(name=new_name)
        
        return f"Project updated successfully! New Name: {project.name}"
    except Exception as e:
        return f"Error updating project: {str(e)}"

def create_jira_issue():
    try:
        project_key = input("Enter project key: ")
        issue_type = input("Enter issue type: ")
        summary = input("Enter issue summary: ")
        description = input("Enter issue description (press Enter for none): ") or None

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
        issue_key = "HACKPROJ-1"
        new_summary = "OpenAI Hackathon Project"
        new_description = "This issue is for testing purpose"
        
        issue = jira.issue(issue_key)
        issue.update(summary=new_summary, description=new_description)
        
        return f"Issue updated successfully! New Summary: {issue.fields.summary}, New Description: {issue.fields.description}"
    except Exception as e:
        return f"Error updating issue: {str(e)}"
        
def check_jira_issue_status():
    try:
        issue_key = "HACKPROJ-1"
        issue = jira.issue(issue_key)
        status = issue.fields.status.name
        return f"Status for issue {issue_key}: {status}"
    except Exception as e:
        return f"Error checking issue status: {str(e)}"

def create_jenkins_job():
    job_name="Jen_Pro"
    job_config = """
        <project>
            <builders>
                <hudson.tasks.Shell>
                    <command>echo 'Hello, Jenkins!'</command>
                </hudson.tasks.Shell>
            </builders>
        </project>
    """
    url = f'{JENKINS_URL}/createItem?name={job_name}'
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=job_config, headers=headers, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    time.sleep(5)
    if response.status_code == 200:
        return f"Job '{job_name}' created successfully."
    else:
        return f"Failed to create job '{job_name}'. Status code: {response.status_code}"

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
    job_name="My_Jenkins_Job"
    url = f'{JENKINS_URL}/job/{job_name}/config.xml'
    response = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve configuration for job '{job_name}'. Status code: {response.status_code}"

def delete_jenkins_job():
    job_name="Jen_Pro"
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
    job_name="My_Jenkins_Job"
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
    job_name="My_Jenkins_Job"
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
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions for Jira operations.")
    parser.add_argument(
        "operation",
        choices=["create_job","retrieve_job_configuration","delete_job","retrieve_job_information","disable_job","enable_job","trigger_build","retrieve_build_information","retrieve_console_output","stop_build","retrieve_queue_information","retrieve_queue_item_information","list_jira_functions","search_issues", "create_issue", "update_issue", "issue_status", "create_project", "fetch_project", "update_project"],
        help="Specify operation to perform (search/create/create_project/fetch_project/update_project/update_issue)",
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
  
    else:
        print("Invalid operation. Choose a valid operation.")
