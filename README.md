# Git User Manager

`git-user-manager` is a Python CLI tool designed to help you manage multiple Git user profiles. This tool makes it easy to configure and switch between different Git user credentials, which is particularly useful if you work on multiple projects with different Git accounts.

## Features

- Add new Git user credentials interactively
- Remove existing Git user credentials
- List all saved Git user credentials
- Set active Git user credentials

## Installation

You can install `git-user-manager` from PyPI:

```sh
pip install git-user-manager
```

## Usage
The `git-user-manager` tool provides several command-line arguments to manage your Git user credentials.

```sh
usage: git-user-manager [-h] [--add] [--remove] [--list] [--set user] [--user user] [--name name] [--email email]
```

## Commands and Arguments
- -h, --help: Show the help message and exit.
- --add: Use this argument to set credentials.
- --remove: Use this argument to remove credentials.
- --list: Use this argument to list saved user credentials.
- --set user: Use this argument to set the active Git user.
- --user user, -u user: Specify your username.
- --name name, -n name: Specify your full name.
- --email email, -e email: Specify your Git email.

## Examples
- Add a New User
```sh
git-user-manager --add
```
This command will prompt you to enter your username, full name, and email interactively.

- Remove an Existing User
```sh
git-user-manager --remove
```
This command will prompt you to select one or more users to remove.

- List All Saved Users
```sh
git-user-manager --list
```
This command will list all saved user credentials.

- Set the Active User
```sh
git-user-manager --set username
```
This command will set the specified username as the active Git user.

## Configuration
The user credentials are stored in a JSON file located at ~/.config/git-user-manager/credentials.json.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/imegeek/git-user-manager/blob/master/LICENSE) file for details.
