# sequra.honeybadger

## Description

This role manages teams and users on a [honeybadger.io](https://www.honeybadger.io/) organization.

This ansible role is intended to send requests to Honeybadger API locally.

## Requirements

Optional: It is recommended to create a python virtual environment to manage python packages by running:
- `python -mvenv venv` - to create the virtual environment
- `source venv/bin/activate` - to activate the virtual environment

Install the necessary Python Packages/Libraries in your ansible virtualenv by running:
`pip install -r requirements.txt`

## Configuration

Create `~/.honeybadger.json` file containing the Honeybadger API Key as follows:
```
{"api_key":"$YOUR_API_KEY"}
```

## Role Variables

### Common
* **honeybadger_api_key** - string - API Key from honeyBadger personal profile.

### Team
* **honeybadger_active_teams** - list - Teams to be **present** in honeybadger organization.
* **honeybadger_inactive_teams** - list - Teams to be **absent** from honeybadger organization.
### User
* **honeybadger_active_users** - list of dicts - Users to be **present** in a list of teams.
* **honeybadger_inactive_users** - list of dicts - Users to be **absent** from a list of teams.


### Vars File Example:

```
honeybadger_active_teams:
  - foo team
  - bar team

honeybadger_inactive_teams:
  - deleted team

honeybadger_api_key: "{{ lookup('file','~/.honeybadger.json') | from_json | json_query('api_key') }}"

honeybadger_active_users:
  # User is member of both foo and bar teams
  - email: foo.bar.member@mycompany.org
    teams:
      - name: foo team
      - name: bar team
  # User is admin of foo Team
  - email: foo.admin@mycompany.org
    teams:
      - name: foo team
        admin: True
  # User is admin of bar team and foo team
  - email: foo.bar.admin@mycompany.org
    teams:
      - name: foo team
        admin: True
      - name: bar team
        admin: True

honeybadger_inactive_users:
  # User should be deleted from foo and bar team
  - email: former.member@mycompany.org
    teams:
      - name: foo team
      - name: bar team
```

## Usage

Your `organization` represents a single `host`.

### Example Playbook

```
- hosts: my_organization
  roles:
    - role: sequra.honeybadger
  tags:
    - org
```

As the ansible connection must be local, add the following to your hosts file:

```
[honeybadger]
my_organization ansible_host=127.0.100.1 ansible_connection=local
```

### Keeping vars file clean

In case we want to delete a whole team, move team from `honeybadger_active_teams` to `honeybadger_inactive_teams` and delete all team references from users list of teams. Otherwise errors will be raised.

## License

MIT

## Author

[Luis Fernández](https://github.com/treezio)

## Reviewers

[Marcel Puchol](https://github.com/mpucholblasco)

[Miquel Barceló](https://github.com/miquelbar)
