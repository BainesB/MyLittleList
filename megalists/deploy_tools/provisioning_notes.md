Provisioning an new site

+++++++++++++++++++++++++++++

## Required packages:


* nginx 
* Python  3.6
* virtualenv + pip 
* Git  

eg, on Ubuntu: 

sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-venv

## Nginx virtual Host config 

* see nignx.template.conf 
* replace SITENAME wit, eg, staging.my-domain.com 

## Systemd service

* see gunicorn-systemd.template.service 
* replace SITENAME wit, e.g., staging.my-domain.com

## Folder structure: 
Assume we have a user account at /home/username

/home.username
|__sites 
	|___SITENAME
		|____database
		|____source 
		|____static 
		|____virtualenv


