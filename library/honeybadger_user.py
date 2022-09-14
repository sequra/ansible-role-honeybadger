#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.user import get_user_info, invite_user, delete_user, update_user_role
from ansible.module_utils.team import get_teams, get_team_info


DOCUMENTATION = '''
---
module: honeybadger_user
short_description: Module for provisioning users in HoneyBadger
description:
    - This module provides the ability to provision users on HoneyBadger.
version_added: "0.1"
author: "Luis Fernández @treezio"
requirements:
    - HoneyBadger API key
options:
    admin:
        description:
            - 'true' admin user
            - 'false' non-admin user
        required: true
        default: False
        choices: [False, True]
    email:
        description:
            - email of the user to be invited to a given team.
        required: true
    honeybadger_active_teams:
        description:
            - emails to be present in honeybadger org.
        required: true
        type: list
    honeybadger_api_key:
        description:
            - Personal API Key from HoneyBadger.
        required: true
    state:
        description:
            - 'present' will invite the user to the team if the user is not already invited.
            - 'absent' removes the user from the team.
        required: false
        default: present
        choices: [present, absent]
    team:
        description:
            - team where the user belongs to.
        required: true
'''

EXAMPLES = '''
    - name: create honeybadger user
      honeybadger_user:
        honeybadger_api_key: my_api_key
        user: some-email@corporation.org
        team: some-team
        admin: False
        state: present
        honeybadger_active_teams: ['some-team','another-team']
'''

CHANGES = False
ERROR_MSG = ''

def main():
    """Load the option and route the methods to call"""
    module = AnsibleModule(
            argument_spec=dict(
                admin=dict(default=False, choices=[True, False]),
                email=dict(required=True, type='str', no_log=False),
                honeybadger_api_key=dict(required=True, type='str'),
                honeybadger_active_teams=dict(required=True, type='list', no_log=False),
                state=dict(default='present', choices=['absent', 'present']),
                team=dict(required=True, type='str', no_log=False),
                ),
            supports_check_mode=False
            )
    # api auth vars
    honeybadger_api_key = module.params['honeybadger_api_key']
    # user input vars
    user_admin_status = module.params['admin']
    user_desired_state = module.params['state']
    user_email = module.params['email']
    # team input vars
    user_desired_team = module.params['team']
    honeybadger_active_teams = module.params['honeybadger_active_teams']

    # Get all teams from honeybadger org
    response = get_teams(honeybadger_api_key)
    if response.status_code == 200:
        teams = response.json()['results']
    else:
        raise Exception("Unable to request teams info - " + str(response))

    # Get team status and info in honeybadger
    team_info = get_team_info(teams, user_desired_team)

    # Check Team Exists and should exist
    if team_info is None:
        module.fail_json(msg=str("Team {0} not found, team must exist before users creation. Make sure Team creation task runs properly.".format(user_desired_team)))
        return

    # Get user information from the current team in loop
    user_info = get_user_info(team_info, user_email)

    # The user does not exist so we want to invite it
    if user_desired_state == 'present' and user_info is None:
        response = invite_user(honeybadger_api_key, team_info['id'], user_email, user_admin_status)
        # user invitation sent
        if response.status_code == 201:
            module.exit_json(changed=True, user=user_email, msg="User {0} invited to team {1}".format(user_email, user_desired_team))
        # user already invited
        elif response.status_code == 422:
            module.exit_json(changed=False, user=user_email, msg="User {0} already invited to team {1}".format(user_email, user_desired_team))
        else:
            module.fail_json(msg="Failed to invite to user: {0}\n".format(user_email) + str(response))
        return

    # The user exists but needs to be granted Admin Role
    if user_info is not None and user_info['admin'] is not True and user_admin_status is True:
        response = update_user_role(honeybadger_api_key, team_info['id'], user_info['id'], user_admin_status)
        if response.status_code == 204:
            module.exit_json(changed=True, user=user_email, msg="User {0} upgraded to Admin in Team {1}".format(user_email, user_desired_team))
        else:
            module.fail_json(msg="Failed to grant Admin role to user: {0}\n".format(user_email) + str(response))
        return

    # The user exists but needs to be downgraded from Admin to Team member
    if user_info is not None and user_info['admin'] is True and user_admin_status is not True:
        response = update_user_role(honeybadger_api_key, team_info['id'], user_info['id'], user_admin_status)
        if response.status_code == 204:
            module.exit_json(changed=True, user=user_email, msg="User {0} downgraded to team member in Team {1}".format(user_email, user_desired_team))
        else:
            module.fail_json(msg="Failed to downgrade to Team Member role to user: {0}\n".format(user_email) + str(response))
        return

    # The user exists and we want to delete it.
    if user_desired_state == 'absent' and user_info is not None:
        response = delete_user(honeybadger_api_key, team_info['id'], user_info['id'])
        if response.status_code == 204:
            module.exit_json(changed=True, user=user_email, msg="User {0} deleted from team {1}".format(user_email, user_desired_team))
        else:
            module.fail_json(msg="Failed to delete user: {}\n".format(user_email) + str(response))
        return

    # The user is there and we want it there. Nothing to do here
    if user_desired_state == 'present' and user_info is not None:
        module.exit_json(changed=False, user=user_email, msg="User {0} already member of team {1}".format(user_email, user_desired_team))
        return

    # The user is not there and we don't want it there. Nothing to do here
    if user_desired_state == 'absent' and user_info is None:
        module.exit_json(changed=False, user=user_email, msg="User {0} already absent from team {1}".format(user_email, user_desired_team))
        return


if __name__ == '__main__':
    main()
