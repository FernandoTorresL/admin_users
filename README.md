# Admin Scrapper (admin_users)

## Create a scrapper and ETL process using Python, Selenium

<a href="https://github.com/FernandoTorresL/admin_users/commits/main" target="_blank">![GitHub last commit](https://img.shields.io/github/last-commit/FernandoTorresL/admin_users)</a>

<a href="https://github.com/FernandoTorresL/admin_users" target="_blank">![GitHub repo size](https://img.shields.io/github/repo-size/FernandoTorresL/admin_users)</a>

## Project for IMSS, México. (Proyecto personal para IMSS, México)

## Introduction

There´s a system that it's operated by workers of the _Coordinación de Afiliación - División de Soporte a los Procesos de Afiliación_, an office on Instituto Mexicano del Seguro Social (IMSS, DIR, CA, DSPA).

This code must login, navigate, and scrap pages from this site to create a CSV file.

From this website that use JavaScript, we also create and test some instructions on a Jupyter Notebook to test a scrapper to get all the general data from that site by page.

## Technology used

This project was build with the use of: 

- Python v3.11.4
- Selenium
- Jupyter notebooks (for test and debug)

## Important

The website and the data are confidential because are from an intranet site.
So, the real url is on a secret **config.yaml** production file.
This file defines what are the urls, the XPath strings, titles and body from that site.

In GitHub there is only a **config.example.yaml** with dummy data.
Check first the configuration on this example file.

Example *config.example.yaml*:
```sh
website_data:
  url: http://1.2.3.4:1234/site/
  user: user
  password: password
  labels:
    page01:
      alt_bntAceptarLogin: "alt_name"
    page02:
    ...
```
## Installation

### Clone this repo

```sh
git clone git@github.com:FernandoTorresL/admin_users.git
```
> Optional: You can use and change *<my_folder>* on this instruction to create a new folder instead of the default *admin_users*

```sh
git clone git@github.com:FernandoTorresL/admin_users.git <my_folder>
```

### Create/Copy initial files (only placeholder_file.txt on GitHub)

You must create o paste some files on place:

- A .yaml file on scraper_ETL/extract folder, based on config.example.yaml

### Change to working directory and create a Python virtual environment

OS X & Linux:

```sh
$ cd admin_users
$ python -m venv ./venv
$ source ./venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip3 install -r requirements.txt
(venv) $
```

Windows:
```sh
$ cd admin_users
$ python -m venv venv
$ .\venv\Scripts\activate
(venv) $ pip install --upgrade pip
(venv) $ pip3 install -r requirements.txt
(venv) $
```

Windows 10 with Git bash terminal:
```sh
$ cd admin_users
$ python -m venv venv
$ source ./venv/Scripts/activate
(venv) $ pip install --upgrade pip
(venv) $ pip3 install -r requirements.txt
(venv) $
```

Windows 10 with powershell terminal:
```sh
PS> cd admin_users
PS> python -m venv venv
PS> .\.venv\Scripts\Activate.ps1
(.venv) PS> pip install --upgrade pip
(.venv) PS> pip3 install -r requirements.txt
(.venv) PS>
```

Windows 10 with WSL shell:
```sh
user@pc_name: cd admin_users
user@pc_name: python3 -m venv venv
user@pc_name: source venv/bin/activate
(venv) user@pc_name: pip install --upgrade pip
(venv) user@pc_name: pip3 install -r requirements.txt
(venv) user@pc_name:
```

> This prompt may vary if you use another shell configuration, like pk10 or git bash

Later, to deactivate the virtual environment
OS X & Linux & Windows:

```sh
(venv) $ deactivate
$
```

### View help and arguments

```sh
(venv) $ cd scraper_ETL/extract
(venv) $ python3 main.py --help
```
#### Output
```sh
usage: main.py [-h] {admin_users}

positional arguments:
  {admin_users}  Argument: The website that you want to scrape

options:
  -h, --help     show this help message and exit
```
> If using another Python version try: python main.py --help


## Run the project

Before run this project, create and edit the following file:

* scraper_ETL/extract/config.yaml

Then, you can execute the program.

### Example

```sh
(venv) python main.py admin_users
```

## Output file

* ./csv/admin_users_<datetime_stamp>_records.csv, CSV file with the data extracted from the site

## Contributing to this repo

1. Fork it (<https://github.com/FernandoTorresL/admin_users/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

---

<div align="center">
    <a href="https://fertorresmx.dev/">
      <img height="150em" src="https://raw.githubusercontent.com/FernandoTorresL/FernandoTorresL/main/media/FerTorres-dev1.png">
  </a>
</div>



## Follow me
[fertorresmx.dev](https://fertorresmx.dev/)

#### :globe_with_meridians: [Twitter](https://twitter.com/FerTorresMx), [Instagram](https://www.instagram.com/fertorresmx/): @fertorresmx
