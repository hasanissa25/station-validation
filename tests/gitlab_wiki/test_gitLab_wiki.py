# flake8: noqa
from tests.gitlab_wiki.GitLabAttachments import GitLabAttachments
from tests.gitlab_wiki.GitLabWikis import GitLabWikis
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


GitLabWikisObj = GitLabWikis(
    title="QW.QCC01",
    gitlabUrl="http://gitlab.seismo.nrcan.gc.ca",
    projectId=10,
    token="gJ-TxBSSMYBrsxhh9jze",
    webserver="https://3.96.234.48:18010/json/QW/ONE01/2022-04-21-2022-05-01/")

GitLabWikisObj.setup_wiki()

GitLabAttachmentsObj = GitLabAttachments(
    list_of_attachments=GitLabWikisObj.list_of_attachment_references)
attachments = GitLabAttachmentsObj.get_attachments()

content = generate_markdown_template(attachments=attachments)
GitLabWikisObj._post_wiki_api(content=content)
