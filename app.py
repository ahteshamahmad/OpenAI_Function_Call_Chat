# app.py
import os
from flask import Flask, render_template, request, jsonify
from all_job_functions import search_jira_issues, add_comment_to_issue, change_assignee, update_jira_issue, create_jira_issue, check_jira_issue_status, create_jira_project, fetch_jira_project, update_jira_project, create_jenkins_job, retrieve_jenkins_job_configuration, list_all_functions, delete_jenkins_job, retrieve_jenkins_job_information, disable_jenkins_job, enable_jenkins_job, trigger_jenkins_build, retrieve_jenkins_build_information, retrieve_jenkins_console_output, stop_jenkins_build,  retrieve_jenkins_queue_information, retrieve_jenkins_queue_item_information, list_jenkins_projects, count_jenkins_jobs, create_teamcity_project, list_teamcity_projects, list_teamcity_build_configurations, get_teamcity_build_status, get_teamcity_build_details, cancel_teamcity_build, get_teamcity_agent_details, get_teamcity_agent_pools, get_teamcity_build_artifacts, list_teamcity_agents, trigger_build
import openai



# Load your OpenAI API key from a secure location
openai.api_key = os.getenv("OpenAI_API_Token")

app = Flask(__name__)

# Define your Jira functions and process_question as before

# Updated process_command function
def process_command(command):
    predefined_commands = {
        'search_jira_issues': search_jira_issues,
        'create_jira_issue': create_jira_issue,
        'update_jira_issue': update_jira_issue,
        'check_jira_issue_status': check_jira_issue_status,
        'create_jira_project': create_jira_project,
        'fetch_jira_project': fetch_jira_project,
        'update_jira_project': update_jira_project,
        'list_all_functions': list_all_functions,
        'create_jenkins_job': create_jenkins_job,
        'retrieve_jenkins_job_configuration': retrieve_jenkins_job_configuration,
        'delete_jenkins_job': delete_jenkins_job,
        'retrieve_jenkins_job_information': retrieve_jenkins_job_information,
        'disable_jenkins_job': disable_jenkins_job,
        'enable_jenkins_job': enable_jenkins_job,
        'trigger_jenkins_build': trigger_jenkins_build,
        'retrieve_jenkins_build_information': retrieve_jenkins_build_information,
        'retrieve_jenkins_console_output': retrieve_jenkins_console_output,
        'stop_jenkins_build': stop_jenkins_build,
        'retrieve_jenkins_queue_information': retrieve_jenkins_queue_information,
        'retrieve_jenkins_queue_item_information': retrieve_jenkins_queue_item_information,
        'list_jenkins_projects': list_jenkins_projects,
        'count_jenkins_jobs': count_jobs,
        'create_teamcity_project': create_teamcity_project,
        'list_teamcity_projects': list_teamcity_projects,
        'list_teamcity_build_configurations': list_teamcity_build_configurations,
        'get_teamcity_build_status': get_teamcity_build_status,
        'get_teamcity_build_details': get_teamcity_build_details,
        'cancel_teamcity_build': cancel_teamcity_build,
        'get_teamcity_agent_details': get_teamcity_agent_details,
        'get_teamcity_agent_pools': get_teamcity_agent_pools,
        'get_teamcity_build_artifacts': get_teamcity_build_artifacts,
        'list_teamcity_agents': list_teamcity_agents,
        'trigger_build': trigger_build,
        'add_comment_to_issue': add_comment_to_issue,
        'change_assignee': change_assignee
    }

#    if command.startswith('/'):
    if command in predefined_commands:
        command = command[1:]
        if command in predefined_commands:
            return predefined_commands[command]()
        else:
            return "Command not recognized."
    else:
        return process_question(command)

# Updated process_question function
def process_question(user_input):
    try:
        if user_input == "search_jira_issues":
            search_jira_issues()
            return search_jira_issues()
        if user_input == "create_jira_issue":
            create_jira_issue()
            return create_jira_issue()
        if user_input == "add_comment_to_issue":
            add_comment_to_issue()
            return add_comment_to_issue()
        if user_input == "change_assignee":
            change_assignee()
            return change_assignee()
        if user_input == "update_jira_issue":
            update_jira_issue()
            return update_jira_issue()
        if user_input == "check_jira_issue_status":
            check_jira_issue_status()
            return check_jira_issue_status()
        if user_input == "create_jira_project":
            create_jira_project()
            return create_jira_project()
        if user_input == "update_jira_project":
            update_jira_project()
            return update_jira_project()
        if user_input == "fetch_jira_project":
            fetch_jira_project()
            return fetch_jira_project()
        if user_input == "list_all_functions":
            list_all_functions()
            return list_jira_functions()
        if user_input == "create_jenkins_job":
            create_jenkins_job()
            return create_jenkins_job()
        if user_input == "retrieve_jenkins_job_configuration":
            retrieve_jenkins_job_configuration()
            return retrieve_jenkins_job_configuration()
        if user_input == "delete_jenkins_job":
            delete_jenkins_job()
            return delete_jenkins_job()
        if user_input == "retrieve_jenkins_job_information":
            retrieve_jenkins_job_information()
            return retrieve_jenkins_job_information()
        if user_input == "disable_jenkins_job":
            disable_jenkins_job()
            return disable_jenkins_job()
        if user_input == "enable_jenkins_job":
            enable_jenkins_job()
            return enable_jenkins_job()
        if user_input == "trigger_jenkins_build":
            trigger_jenkins_build()
            return trigger_jenkins_build()
        if user_input == "retrieve_jenkins_build_information":
            retrieve_jenkins_build_information()
            return retrieve_jenkins_build_information()
        if user_input == "retrieve_jenkins_console_output":
            retrieve_jenkins_console_output()
            return retrieve_jenkins_console_output()
        if user_input == "stop_jenkins_build":
            stop_jenkins_build()
            return stop_jenkins_build()
        if user_input == "retrieve_jenkins_queue_information":
            retrieve_jenkins_queue_information()
            return retrieve_jenkins_queue_information()
        if user_input == "retrieve_jenkins_queue_item_information":
            retrieve_jenkins_queue_item_information()
            return retrieve_jenkins_queue_item_information()
        if user_input == "list_jenkins_projects":
            list_jenkins_projects()
            return list_jenkins_projects()
        if user_input == "count_jenkins_jobs":
            count_jenkins_jobs()
            return count_jenkins_jobs()
        if user_input == "create_teamcity_project":
            create_teamcity_project()
            return create_teamcity_project()
        if user_input == "list_teamcity_projects":
            list_teamcity_projects()
            return list_teamcity_projects()
        if user_input == "list_teamcity_build_configurations":
            list_teamcity_build_configurations()
            return list_teamcity_build_configurations()
        if user_input == "get_teamcity_build_status":
            get_teamcity_build_status()
            return get_teamcity_build_status()
        if user_input == "get_teamcity_build_details":
            get_teamcity_build_details()
            return get_teamcity_build_details()
        if user_input == "cancel_teamcity_build":
            cancel_teamcity_build()
            return cancel_teamcity_build()
        if user_input == "get_teamcity_agent_details":
            get_teamcity_agent_details()
            return get_teamcity_agent_details()
        if user_input == "get_teamcity_agent_pools":
            get_teamcity_agent_pools()
            return get_teamcity_agent_pools()
        if user_input == "get_teamcity_build_artifacts":
            get_teamcity_build_artifacts()
            return get_teamcity_build_artifacts()
        if user_input == "list_teamcity_agents":
            list_teamcity_agents()
            return list_teamcity_agents()
        if user_input == "trigger_build":
            trigger_build()
            return trigger_build()

        # Make the OpenAI API call for other user inputs
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )

        # Extract the assistant's reply from the response
        answer = response['choices'][0]['message']['content'].strip()

        # Process specific commands or responses as needed

        return answer

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"An error occurred: {str(e)}"

    except Exception as e:
        # Handle other unexpected errors
        return f"An unexpected error occurred: {str(e)}"
# Routes
@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.form['user_input']

    # Check for specific commands and call corresponding functions
    if user_input == 'search_jira_issues':
        return jsonify({'answer': search_jira_issues()})
    if user_input == 'create_jira_issue':
        return jsonify({'answer': create_jira_issue()})
    if user_input == 'add_comment_to_issue':
        return jsonify({'answer': add_comment_to_issue()})
    if user_input == 'change_assignee':
        return jsonify({'answer': change_assignee()})
    if user_input == 'update_jira_issue':
        return jsonify({'answer': update_jira_issue()})
    if user_input == 'check_jira_issue_status':
        return jsonify({'answer': check_jira_issue_status()})
    if user_input == 'create_jira_project':
        return jsonify({'answer': create_jira_project()})
    if user_input == 'update_jira_project':
        return jsonify({'answer': update_jira_project()})
    if user_input == 'fetch_jira_project':
        return jsonify({'answer': fetch_jira_project()})
    if user_input == 'list_all_functions':
        return jsonify({'answer': list_all_functions()})
    if user_input == 'create_jenkins_job':
        return jsonify({'answer': create_jenkins_job()})
    if user_input == 'retrieve_jenkins_job_configuration':
        return jsonify({'answer': retrieve_jenkins_job_configuration()})
    if user_input == 'delete_jenkins_job':
        return jsonify({'answer': delete_jenkins_job()})
    if user_input == 'retrieve_jenkins_job_information':
        return jsonify({'answer': retrieve_jenkins_job_information()})
    if user_input == 'disable_jenkins_job':
        return jsonify({'answer': disable_jenkins_job()})
    if user_input == 'enable_jenkins_job':
        return jsonify({'answer': enable_jenkins_job()})
    if user_input == 'trigger_jenkins_build':
        return jsonify({'answer': trigger_jenkins_build()})
    if user_input == 'retrieve_jenkins_build_information':
        return jsonify({'answer': retrieve_jenkins_build_information()})
    if user_input == 'retrieve_jenkins_console_output':
        return jsonify({'answer': retrieve_jenkins_console_output()})
    if user_input == 'stop_jenkins_build':
        return jsonify({'answer': stop_jenkins_build()})
    if user_input == 'retrieve_jenkins_queue_information':
        return jsonify({'answer': retrieve_jenkins_queue_information()})
    if user_input == 'retrieve_jenkins_queue_item_information':
        return jsonify({'answer': retrieve_jenkins_queue_item_information()})
    if user_input == 'list_jenkins_projects':
        return jsonify({'answer': list_jenkins_projects()})
    if user_input == 'count_jenkins_jobs':
        return jsonify({'answer': count_jenkins_jobs()})
    if user_input == 'create_teamcity_project':
        return jsonify({'answer': create_teamcity_project()})
    if user_input == 'list_teamcity_projects':
        return jsonify({'answer': list_teamcity_projects()})
    if user_input == 'list_teamcity_build_configurations':
        return jsonify({'answer': list_teamcity_build_configurations()})
    if user_input == 'get_teamcity_build_status':
        return jsonify({'answer': get_teamcity_build_status()})
    if user_input == 'get_teamcity_build_details':
        return jsonify({'answer': get_teamcity_build_details()})
    if user_input == 'cancel_teamcity_build':
        return jsonify({'answer': cancel_teamcity_build()})
    if user_input == 'get_teamcity_agent_details':
        return jsonify({'answer': get_teamcity_agent_details()})
    if user_input == 'get_teamcity_agent_pools':
        return jsonify({'answer': get_teamcity_agent_pools()})
    if user_input == 'get_teamcity_build_artifacts':
        return jsonify({'answer': get_teamcity_build_artifacts()})
    if user_input == 'list_teamcity_agents':
        return jsonify({'answer': list_teamcity_agents()})
    if user_input == 'trigger_build':
        return jsonify({'answer': trigger_build()})
    else:
        # If it's not a specific command, process the question with OpenAI or handle other cases
        answer = process_question(user_input)
        return jsonify({'answer': answer})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)