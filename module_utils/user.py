# User module
import requests

def delete_user(api_key, team_id, user_id):
    """Delete user from team.

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key
    team_id: string
        Team ID
    user_id: string
        User ID

    Requests
    --------
        Calls DELETE /v2/teams/ID/team_members/ID

    Returns
    -------
        Request Response - dict
    """
    url = "https://app.honeybadger.io/v2/teams/{0}/team_members/{1}".format(team_id, user_id)
    response = requests.delete(url, auth=(api_key,''))
    response.close()
    return response

def get_user_info(team_info, user_email):
    """Get user info from team.

    Parameters
    ----------
    team_info: dict
        Dictionary containing team information
    user_email: string
        Email of the user to be found.

    Returns
    -------
        User info when user is found in team. Otherwise returns None.
    """
    for user_info in team_info['members']:
        if user_email in user_info['email']:
            return user_info
    return None

def invite_user(api_key, team_id, user_email, admin):
    """Sends email invitation to join a team.

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key
    team_id:
        Team ID
    is_admin: bool
        True when User is Admin
    user_email: string
        User email

    Requests
    --------
        Calls POST /v2/teams/ID/team_invitations

    Returns
    -------
        Request Response - dict
    """
    set_admin = "true" if admin is True else "false"
    url = "https://app.honeybadger.io/v2/teams/{0}/team_invitations".format(team_id)
    invitation = {
        "team_invitation": {
            "email": user_email,
            "admin": set_admin
        }
    }
    response = requests.post(url, json=invitation, auth=(api_key,''))
    response.close()
    return response

def update_user_role(api_key, team_id, user_id, admin):
    """Grant admin role to a user on a team

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key
    team_id: string
        Team ID
    user_id: string
        User ID

    Requests
    --------
        Calls PUT /v2/teams/ID/team_members/ID

    Returns
    -------
        Request Response - dict
    """
    url = "https://app.honeybadger.io/v2/teams/{0}/team_members/{1}".format(team_id, user_id)
    role = {
        "team_member": {
            "admin": admin
        }
    }
    response = requests.put(url, json=role, auth=(api_key,''))
    response.close()
    return response
