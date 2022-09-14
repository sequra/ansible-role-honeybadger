# Common Tools for honeybadger users management
import requests

def create_team(api_key, team_name):
    """Create team in HoneyBadger org.

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key
    team_name
        Team Name

    Requests
    --------
        Calls POST /v2/teams

    Returns
    -------
        Request Response - dict
    """
    url = "https://app.honeybadger.io/v2/teams"
    team = {
        "team": {
            "name": team_name
        }
    }
    response = requests.post(url, json=team, auth=(api_key,''))
    response.close()
    return response

def delete_team(api_key, team_id):
    """Delete user from team.

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key
    team_id: string
        Team ID

    Requests
    --------
        Calls DELETE /v2/teams/ID

    Returns
    -------
        Request Response - dict
    """
    url = "https://app.honeybadger.io/v2/teams/{0}".format(team_id)
    response = requests.delete(url, auth=(api_key,''))
    response.close()
    return response

def get_teams(api_key):
    """Get all teams from HoneyBadger org.

    Parameters
    ----------
    api_key: string
        HoneyBadger API Key

    Requests
    --------
        Calls GET /v2/teams

    Returns
    -------
        Array of dictionaries containing teams info
    """
    url = "https://app.honeybadger.io/v2/teams"
    response = requests.get(url, auth=(api_key,''))
    response.close()
    return response

def get_team_info(teams, team_name):
    """Returns team info when team is found in the list of teams.

    Parameters
    ----------
    teams: list
        List of dictionaries containing teams info
    team_name: string
        Name of the team to be found.

    Returns
    -------
        Team info when team is found. Otherwise returns None.
    """
    for team_dict in teams:
        if team_name in team_dict['name']:
            return team_dict
    return None
