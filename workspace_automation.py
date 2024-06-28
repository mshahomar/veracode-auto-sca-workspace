import requests
import os
from typing import Any
from auth import generate_header
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

headers={ 
    'accept-encoding': 'gzip', 
    'user-agent': 'AbahKo Co',
    'Content-Type': 'application/json' 
    }


def create_workspace(repo_name, api_base_url):
    path = '/srcclr/v3/workspaces'
    data = f'{{"name":"{repo_name}"}}'
    create_workspace = requests.post(
        f'https://{api_base_url}{path}',
        auth=RequestsAuthPluginVeracodeHMAC(),
        data=data,
        headers=headers,
        verify=False
    )

    create_workspace.raise_for_status()
    print(f"create_workspace Status Code: {create_workspace.status_code}")
    print(f"type: create_workspace Status Code: {type(create_workspace.status_code)}")

    # Get workspace ID
    workspace_id = get_workspace(repo_name, api_base_url)
    return workspace_id


def get_workspace(repo_name, api_base_url):
    path = f'/srcclr/v3/workspaces?filter%5Bworkspace%5D={requests.utils.quote(repo_name)}'
    check_workspace = requests.get(
        f'https://{api_base_url}{path}',
        auth=RequestsAuthPluginVeracodeHMAC(),
        headers=headers,
        verify=False
    )

    check_workspace.raise_for_status()
    print(f"check_workspace Status Code: {check_workspace.status_code}")
    workspace_results = check_workspace.json()
    workspace_length = workspace_results['page']['total_elements']
    print(f"There are {workspace_length} workspaces")

    workspace_id = ''

    if workspace_length == 0:
        print("Workspace doesn't exist and needs to be created")
        create_workspace_response = input("Do you want to create the workspace? (y/n): ").lower().strip()
        if create_workspace_response == 'y':
            create_workspace(repo_name, api_base_url)
            return workspace_id
        else:
            print("No Workspace will be created")
            return None
    else:
        print(f"workspace_results: {workspace_results['_embedded']}")

        workspace_id = workspace_results['_embedded']['workspaces'][0]['id']
        # projects_count = workspace_results['workspaces'][0]['projects_count']
        print(f'Workspace ID: {workspace_id}')
        print(f'type Workspace ID: {type(workspace_id)}')
        # print(f"Number of Projects: {projects_count}")
        return workspace_id


def get_agent(workspace_id, api_base_url):
    path = f'/srcclr/v3/workspaces/{workspace_id}/agents'
    check_agents = requests.get(
        f'https://{api_base_url}{path}',
        auth=RequestsAuthPluginVeracodeHMAC(),
        headers=headers,
        verify=False
    )
    check_agents.raise_for_status()
    print(f"check_agents Status Code: {check_agents.status_code}")
    workspaces_agents_results = check_agents.json()
    print(f"Agents: {workspaces_agents_results}")

    if '_embedded' in workspaces_agents_results:
        print('There are agents, check if the correct agent exists')
        for agent in workspaces_agents_results['_embedded']['agents']:
            print(f"Agent Name: {agent['name']}")
            print(f"Agent ID: {agent['id']}")
            if agent['name'] == 'Jenkins':
                agent_id = agent['id']
            else:
                agent_id = None

        # Found agent with name "Jenkins"
        if agent_id is not None:
            print('Agent ID: ' + agent_id + ' - for agent with name "Jenkins" already exists')

            # Prompt user if they want to regenerate a new token
            regenerate_token = input('Do you want to regenerate the token for the agent? (y/n): ').lower()
            if regenerate_token == 'y':
                print('Agent ID: ' + agent_id + ' - for agent with name "Jenkins" - regenerating token')
                regenerate_agent_token(workspace_id, agent_id, api_base_url)
            elif regenerate_token == 'n':
                print('Agent ID: ' + agent_id + ' - for agent with name "Jenkins" - token not regenerated')
            else:
                print('Invalid input')
                srcclr_api_token = agent['token']['access_token']
    else:
        print('No agents found, creating one...')
        create_agent_token(workspace_id, api_base_url)


def create_agent_token(workspace_id, api_base_url):
    print("Agent for \"Jenkins\" doesn't exist and needs to be created")
    path = f'/srcclr/v3/workspaces/{workspace_id}/agents'
    data = '{"agent_type": "JENKINS", "name": "Jenkins"}'
    create_agent = requests.post(
        f'https://{api_base_url}{path}',
        auth=RequestsAuthPluginVeracodeHMAC(),
        headers=headers,
        data=data,
        verify=False
    )

    create_agent.raise_for_status()
    print('Agent created')
    srcclr_api_token = create_agent.json()['token']['access_token']
    print(f"srcclr_api_token: {srcclr_api_token}")
    return srcclr_api_token


def regenerate_agent_token(workspace_id, agent_id, api_base_url):
    path = f'/srcclr/v3/workspaces/{workspace_id}/agents/{agent_id}/token:regenerate'
    regenerate_token = requests.post(
        f'https://{api_base_url}{path}',
        auth=RequestsAuthPluginVeracodeHMAC(),
        headers=headers,
        verify=False
    )
    regenerate_token.raise_for_status()
    print(f"regenerate_token Status Code: {regenerate_token.status_code}")

    print('Agent token regenerated')
    srcclr_api_token = regenerate_token.json()['access_token']
    print(f"srcclr_api_token 1: {srcclr_api_token}")
    return srcclr_api_token


def workspace_automation(options: Any) -> str:
    """
    Automates the workspace creation and agent setup for the Veracode Software Composition Analysis (SCA) tool.

    Args:
        options (Any): A dictionary containing the following keys:
            VID (str): Veracode ID
            VKEY (str): Veracode Key
            GITHUB_REPOSITORY (str, optional): The name of the GitHub repository

    Returns:
        str: The SCA API token for the created/existing agent.
    """
    # Set the platform region and base API URL
    # cleaned_id = options.get('VID', '').replace('vera01ei-', '')
    # cleaned_key = options.get('VKEY', '').replace('vera01es-', '')
    # repo_name = os.environ.get('GITHUB_REPOSITORY', '')
    repo_name = options

    # if options.get('VID', '').startswith('vera01ei-'):
    #     print('Platform is ER')
    api_base_url = 'api.veracode.eu'
    # else:
    #     print('Platform is US')
    # api_base_url = 'api.veracode.com'

    workspace_id = get_workspace(repo_name, api_base_url)

    if workspace_id is None:
        print("No Workspace ID. Exiting...")
        return workspace_id

    # Get Agents 
    get_agent(workspace_id, api_base_url)


workspace_name = input("Please provide the workspace name: ")
clean_workspace_name = workspace_name.strip()
print(f"You have provided this workspace name: {clean_workspace_name}")
workspace_automation(clean_workspace_name)
