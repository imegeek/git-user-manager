import re
import os
import sys
import json
import argparse
import subprocess
from InquirerPy import inquirer

config_path = os.path.join(os.path.expanduser("~"), ".config", "git-user-manager")
credential_path = os.path.join(config_path, "credentials.json")

if not os.path.isdir(config_path):
	os.makedirs(config_path)

def validate_email(email):
    if email:
        # Define the regular expression pattern for a valid email address
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        
        # Use the re.match() function to check if the email matches the pattern
        match = re.match(pattern, email)
        
        # If a match is found, the email is valid; otherwise, it is invalid
        return bool(match)

parser = argparse.ArgumentParser(prog="git-user-manager")
parser.add_argument(
    "--add",
    action='store_true',
    help="use this argument to set credentials",
)

parser.add_argument(
    "--remove",
    action='store_true',
    help="use this argument to remove credentials.",
)

parser.add_argument(
    "--list",
	action='store_true',
    help="use this argument to list saved user credentials.",
)

parser.add_argument(
    "--set",
	metavar="user",
    help="use this argument to set git user.",
)

parser.add_argument(
    "--user", "-u",
    metavar='user',
    help="specify your username",
)

parser.add_argument(
    "--name", "-n",
    metavar="name",
    help="specify your full name",
)

parser.add_argument(
    "--email", "-e",
    metavar="email",
    help="specify your git email",
)

args = parser.parse_args()
getadd = args.add
getset = args.set
getlist = args.list
getremove = args.remove
getuser = args.user
getname = args.name
getemail = args.email

git = subprocess.run("git", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if not git.stdout:
	print("'git' command not found.\ninstall 'git' to continue.")
	sys.exit(1)

if getlist:
	with open(credential_path) as f:
		f = json.loads(f.read())
		users = [user for index, user in enumerate(f)]
		print(f"{len(users)}", "users" if len(users) > 1 else "user", "found.", f"\n\n{"\n".join(users)}")
		sys.exit(0)

if getuser:
    if getname is None or getemail is None:
        parser.error("--user requires two additional arguments: --name and --email")

def main():
	global getadd, getset, getlist, getremove, getuser, getname, getemail

	credentials = {}
	found_credentials = False

	try:
		if getadd:
			getuser = inquirer.text(
				message="Enter your username:",
				validate=lambda text : text,
				invalid_message="Input required"
				).execute()
			getname = inquirer.text(
				message="Enter your name:",
				validate=lambda text : text,
				invalid_message="Input required"
				).execute()
			getemail = inquirer.text(
				message="Enter your email:",
				validate=lambda text : validate_email(text),
				invalid_message="Email is not valid."
				).execute()

		if getuser and getname and getemail:
			validate = validate_email(getemail)
			if not validate:
				print(f"'{getemail}' is not a valid email address.")
				sys.exit(1)
		
			found_credentials = True

		if os.path.isfile(credential_path):
			with open(credential_path) as f:
				file = f.read().strip()
				if file:
					credentials = json.loads(file)
				if (file == "{}") and (not found_credentials):
					print("no credentials found, use --add argument to add.")
					sys.exit(1)
		else:
			if not found_credentials:
				print("no credentials found, use --add argument to add.")
				sys.exit(1)

		if found_credentials:
			credentials[getuser] = {
				"name":getname,
				"email":getemail
			}

			json.dump(credentials, open(credential_path, "w"), indent=2)
			print(json.dumps(credentials[getuser], indent=2))
			print("Credentials saved.")
			sys.exit(0)

		if credentials and file:
			users = [user for user in credentials]

			if getremove:
				users = inquirer.checkbox(
					message="Select one or more user [Use tab button to select]:",
					choices=users
				).execute()
				for user in users:
					credentials.pop(user)
				
				if users:
					json.dump(credentials, open(credential_path, "w"))
					selected_users = ', '.join(users)
					if len(users) > 1:
						print(f"Users: {selected_users} has been removed.")
					else:
						print(f"User: {selected_users} has been removed.")
					sys.exit(0)
				else:
					print("No user selected.")
					sys.exit(0)

			if getset:
				user = getset
			else:
				user = inquirer.rawlist(
					message = "Select an user account:",
					choices = users
				).execute()

			try:
				name, email =  [credentials[user][detail] for detail in credentials[user]]
			except Exception:
				print(f"User: '\33[91m{user}\33[0m' not found in credentials.")
				sys.exit(1)

			set_name = subprocess.run(f"git config --global user.name \"{name}\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode
			set_email = subprocess.run(f"git config --global user.email {email}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode

			if set_name == 0 and set_email == 0:
				print(f"User '\33[92m{user}\33[0m' has been selected for git.")
	except (KeyboardInterrupt, EOFError):
		print("Program Interrupted.")
		sys.exit(1)

if __name__ == "__main__":
	main()
