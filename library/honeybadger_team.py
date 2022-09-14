#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.team import create_team, delete_team, get_teams, get_team_info

DOCUMENTATION = '''
---
module: honeybadger_team
short_description: Module for provisioning Teams in HoneyBadger
description:
    - This module provides the ability to provision Teams on HoneyBadger
version_added: "0.1"
author: "Luis Fernandez @treezio"
requirements:
    - HoneyBadger API key
options:
    honeybadger_api_key:
        description:
            - Personal API Key from HoneyBadger
        required: true
    team:
        description:
            - team where the user belongs to.
        required: true
    state:
        description:
            - "'present' will invite the user to the team if the user is not already invited."
            - "'absent' removes the user from the team"
        required: false
        default: present
        choices: [present, absent]
'''

EXAMPLES = '''
    - name: create honeybadger teams
      honeybadger_team:
        honeybadger_api_key: my_api_key
        team: cool-team
        state: present
'''

def main():
    """Load the option and route the methods to call"""
    module = AnsibleModule(
            argument_spec=dict(
                honeybadger_api_key=dict(required=True, type='str'),
                team=dict(required=True, type='str', no_log=False),
                state=dict(default='present', choices=['present', 'absent']),
                ),
            supports_check_mode=False
            )

    desired_state = module.params['state']
    honeybadger_api_key = module.params['honeybadger_api_key']
    team_name = module.params['team']

    # Get all teams from honeybadger org
    response = get_teams(honeybadger_api_key)
    if response.status_code == 200:
        teams = response.json()['results']
    else:
        raise Exception("Unable to request teams info - " + str(response))

    # Get team info
    team_info = get_team_info(teams, team_name)

    # The team does no exist and we want to create it
    if desired_state == 'present' and team_info is None:
        response = create_team(honeybadger_api_key, team_name)
        if response.status_code == 201:
            module.exit_json(changed=True, team=team_name, msg="team {0} created.".format(team_name))
        else:
            module.fail_json(msg="Failed to create team: {0}\n".format(team_name) + str(response))

    # The team exists and we want to delete it
    if desired_state == 'absent' and team_info is not None:
        response = delete_team(honeybadger_api_key, team_info['id'])
        if response.status_code == 204:
            module.exit_json(changed=True, team=team_name, msg="team {0} deleted.".format(team_name))
        else:
            module.fail_json(msg="Failed to delete team: {0}\n".format(team_name) + str(response))

    # The team_state and desired_state are equal
    if desired_state == 'present' and team_info is not None:
        module.exit_json(changed=False, team=team_name, msg="Team {0} already present in organization.".format(team_name))
        return

    if desired_state == 'absent' and team_info is None:
        module.exit_json(changed=False, team=team_name, msg="Team {0} already absent from organization.".format(team_name))
        return


if __name__ == '__main__':
    main()
