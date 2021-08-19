# Part one >>> cloning lots of python related repositories from **GITHUB**
# and put them into repos directory.

import os
import subprocess

import wget
from colorama import Fore
from github import Github
from requests.exceptions import HTTPError

""" There are two ways to do so: 1. Clone lots of repositories and then walk through the directories and delete every
single file except python files, 2. Get a specific content file which is the chosen way here """

""" There are many ways to download the files: 1. Using wget, 2. Implementing your own dl.py file in order to
download files using requests library or even making a function named download """

# replace with your desired directory
repos_path = ''

try:
    access_token = open('', 'r').read()
    github = Github(access_token)

    query = 'language:python'
    res = github.search_repositories(query)

    # print(res.totalCount)
    # print(dir(res))

    for repo in res:
        contents = repo.get_contents('')
        while contents:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
            else:
                # print(f'{Fore.GREEN} + URL: {file_content.download_url}')
                if file_content.path.endswith('.py'):
                    contents_url = file_content.download_url

                    if not os.path.isfile(f'{repos_path}/{file_content.name}'):
                        try:
                            wget.download(
                                contents_url, out=repos_path, bar=None)
                        except HTTPError as http_err:
                            print(
                                f'{Fore.YELLOW} -  "Error occurred": {http_err}')
                            continue
                        except Exception as err:
                            print(f'{Fore.YELLOW} -  "Error occurred": {err}')
                            continue
                        else:
                            print(
                                f'{Fore.GREEN} + {Fore.WHITE} "{file_content.name}" {Fore.GREEN} Downloaded')
                    else:
                        print(
                            f'{Fore.RED} - {Fore.WHITE} "{file_content.name}" {Fore.RED} Exists')


except Exception as e:

    command = 'du -sh repos/'

    filenames_len = 0
    for dirpath, dirnames, filenames in os.walk(repos_path):
        filenames_len = len(filenames)

    print(f'\n{e}')
    print(f'{Fore.WHITE}There are {filenames_len} Python files under "repos" directory')
    subprocess.call(command)
