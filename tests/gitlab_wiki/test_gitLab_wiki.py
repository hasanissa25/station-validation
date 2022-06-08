# flake8: noqa
from typing import List, Optional
import requests
import logging
from tests.gitlab_wiki.generate_markdown_template import generate_markdown_template
import json
import warnings
warnings.filterwarnings("ignore")

############################################################################################
# TODO:
# Add mypy
# Get the Specific directory, for one date for now. But make it scalable
############################################################################################


class GitLabWikis(dict):
    '''
    Gitlab handler

    Params:
        Title: Title of the wiki page: \
            Example: "QW.QCC01"
        gitlabUrl: URL to the gitlab website: \
            Example: "http://gitlab.seismo.nrcan.gc.ca"
        projectId: The project Id of the repository: \
            Example: 10
        token: The private token of the repository: \
            Example: "gJ-TxBSSMYBrsxhh9jze"
        webserver: The direct link to the web server that includes the attachments we are uploading to the wiki. \
            Example: "https://3.96.234.48:18010/json/QW/ONE01/2022-04-21-2022-05-01/"
    '''

    def __init__(
        self,
        title: str,
        gitlabUrl: str,
        projectId: int,
        token: str,
        webserver: str
    ):
        self.gitlabUrl = f"{gitlabUrl}/api/v4/projects/{projectId}/wikis"
        self.token = token
        self.webserver = webserver
        self.title = title

    def _post_wiki_api(self,
                       title: str,
                       content: Optional[str] = None,
                       ):
        request_url = f'{self.gitlabUrl}'
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
            self._put_wiki_api(title=title,
                               content=content)

    def _put_wiki_api(
        self,
        title: str,
        content: Optional[str] = None,
    ):
        request_url = f"{self.gitlabUrl}/{title}"
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

    def _get_api(self,
                 path_to_attachments: Optional[str] = None) -> requests.Response:
        request_url = self.webserver if path_to_attachments is None else f"{self.webserver}{path_to_attachments}"
        try:
            request_result = requests.get(
                request_url, verify=False
            )
            print(f"Getting file: {request_url}")
            request_result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err.response.content)
            raise err
        return request_result

    def _upload_attachments_wiki_api(self, attachments: List) -> List[dict]:
        request_url = f'{self.gitlabUrl}/attachments'
        headers = {'PRIVATE-TOKEN': self.token}
        list_of_attachment_references: List[dict] = []
        for attachment in attachments:
            print(f'Adding attachment {attachment["filename"]}')
            try:
                req = requests.post(
                    request_url,
                    headers=headers,
                    files={
                        'file': (
                            attachment["filename"],
                            attachment["content"]
                        )
                    })
                req.raise_for_status()
                request_as_json = json.loads(req.content.decode('utf-8'))
                list_of_attachment_references.append(request_as_json)
            except requests.exceptions.HTTPError as err:
                logging.error(err)
        return list_of_attachment_references

    def _download_documents(self, list_of_documents: List) -> List[dict]:
        # Download the documents from the webserver
        list_of_document_references = list(
            map(lambda attachment: {"filename": attachment, "content": self._get_api(attachment).content}, list_of_documents))
        # Upload documents to Git Lab as attachments
        list_of_attachment_references = self._upload_attachments_wiki_api(
            attachments=list_of_document_references)
        return list_of_attachment_references

    def _get_list_of_documents(
        self,
    ) -> List:
        # Getting the list of documents from the webserver provided
        request_result = self._get_api()
        array_of_documents = list(
            map(lambda document: document["name"], request_result.json()))
        filtered_array_of_documents = list(filter(lambda document_name: '.png' in document_name or '.json' in document_name or '.csv' in document_name,
                                                  array_of_documents))
        return filtered_array_of_documents

    def setup_wiki(self):
        list_of_documents = self._get_list_of_documents()
        list_of_attachment_references = self._download_documents(list_of_documents)
        # content = generate_markdown_template()
        # self._post_wiki_api(title=self.title,
        #                     content=content)
        print(json.dumps(list_of_attachment_references,
                      sort_keys=False, indent=4))


GitLabWikisObj = GitLabWikis(
    title="QW.QCC01",
    gitlabUrl="http://gitlab.seismo.nrcan.gc.ca",
    projectId=10,
    token="gJ-TxBSSMYBrsxhh9jze",
    webserver="https://3.96.234.48:18010/json/QW/ONE01/2022-04-21-2022-05-01/")

GitLabWikisObj.setup_wiki()


# content = generate_markdown_template()
# GitLabWikisObj._post_wiki_api(title="(Network.Station) (date) Test:2",
#                               content=content)
