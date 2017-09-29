from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run 
import random

REPO_URL = 'http://github.com/BainesB/MyLittleList.git'


def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	# make a var site_folder = 
	#setting the dirrector to home/alex/sites/muddymarvellous.co.uk
	source_folder = site_folder + '/source'
	# this is where the source code is. 
	
	# note out functions bellow. 
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)	

def _create_directory_structure_if_necessary(site_folder):
	# this is working on the site folder. Muddymarvellous. 
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
	# it seem to be making these subfolders. 
		run(f'mkdir -p {site_folder}/{subfolder}')
		# this is where is is being called. 

def _get_latest_source(source_folder):
		# this one is working on /source 
		if exists(source_folder + '/.git'):
		# it is checking for the git log. 
			run(f'cd {source_folder} && git fetch')
			# change into the source folder and then do git fetch
		else:
			run(f'git clone {REPO_URL} {source_folder}') 
			# otherwise clone the repo. assume added it to the source/
			current_commit = local("git log -n 1 --format=%H", capture=True)
			#??? not to sure. 
			run(f'cd {source_folder} && git reset --hard {current_commit}')
			# cd into the source/ and git reset hard. 

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/megalists/settings.py'
	# this is getting the dirrectory path to settings.py
	sed(settings_path, "DEBUG = True", "DEBUG = False")
	# need to look at what sed is. this seems strieght switch
	sed(settings_path, 
		'ALLOWED_HOSTS =.+$',
		f'ALLOWED_HOSTS = ["{site_name}"]'
	)
	# looks like a swop out for the site name ie muddymarvellous. 	
	secret_key_file = source_folder + '/megalists/secret_key.py'
	# what is this secret_key.py bit. Ok the next bit it checks exists
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		#seems to be creating a massive password. 
		append(secret_key_file, f'SECRET_KEY = "{key}"')
		#....
	append(setting_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'):
		run(f'python3.6 -m venv {virtualenv_folder}')
	run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')
# this is installing the requirements file into virtualenv/

def _update_static_files(source_folder):
	run( 
		f'cd {source_folder}'
		' && ../virtualenv/bin/python manage.py collectstatic --noinput'
	)
# this is doing the collectstatic thing. 

def _update_database(source_folder):
	run(
		f'cd {source_folder}'
		'&& ../virtualenv/bin/python manage.py migrate --noinput'
	)

# this is migrating the db
