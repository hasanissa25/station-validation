# flake8: noqa
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
import requests
import logging
import json
import io
from tests.gitlab_wiki.generate_markdown_template import generate_markdown_template
from pprint import pprint


class GitLabWikis(dict):
    '''
    Gitlab handler

    :param str url: url of gitlab
    :param str token: api token
    '''

    def __init__(
        self,
        url: str,
        projectId: int,
        token: str,
        webserver: str
    ):
        self.url = f"{url}/api/v4/projects/{projectId}/wikis"
        self.token = token
        self.webserver = webserver

    def post_wiki(self,
                  title: str,
                  content: str,
                  ):
        request_url = f'{self.url}'
        headers = {'PRIVATE-TOKEN': self.token}
        data = {"title": title,
                "content": content}
        try:
            req = requests.post(
                request_url,
                headers=headers,
                data=data,
            )
            req.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.put_wiki(title=title,
                          content=content)

    def put_wiki(
        self,
        title: str,
        content: str,
    ):
        request_url = f"{self.url}/{title}"
        headers = {'PRIVATE-TOKEN': self.token}
        data = {"title": title,
                "content": content}
        try:
            req = requests.put(
                request_url,
                headers=headers,
                data=data,
            )
            req.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err.response.content)
            raise err

    def download_attachments(
        self,
        link
    ):
        response = requests.get(link)
        file = open(f"results/{link.split('/')[-1]}", "wb")
        file.write(response.content)
        file.close()


GitLabWikisObj = GitLabWikis(url="http://gitlab.seismo.nrcan.gc.ca",
                             projectId=10,
                             token="WJgJ8NZDP2ei_KpiF8s8",
                             webserver="http://3.96.234.48:18010")


# 1 - Download the files we need
def get_all_files_from_url(url):
    url = url.replace(" ", "%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    links = (soup.find_all('a'))
    for i in links:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ", "%20")
        if(file_name[-1] == '/' and file_name[0] != '.'):
            get_all_files_from_url(url_new)
        if "png" in url_new or "csv" in url_new or "json" in url_new:
            GitLabWikisObj.download_attachments(link=url_new)


get_all_files_from_url("http://3.96.234.48:18010/")


# 2 - Upload the files to WIKI


# 3 - Create the wiki page
# content = generate_markdown_template()
# GitLabWikisObj.post_wiki(title="(Network.Station) (date)",
#                          content=content)
