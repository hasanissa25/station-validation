import argparse
from stationverification.config import get_default_parameters


class UserInput(dict):
    @property
    def gitlabUrl(self) -> bool:
        return self["gitlabUrl"]


def upload_report_fetch_arguments() -> UserInput:
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-u",
        "--gitlabUrl",
        help='URL of GitLab project. Ex: "http://gitlab.seismo.nrcan.gc.ca"',
        type=str,
    )
    argsparser.add_argument(
        "-i",
        "--projectId",
        help="Project ID of GitLab project. Ex: 10",
        type=int,
    )
    argsparser.add_argument(
        "-t",
        "--projectToken",
        help="Project token. Ex: WJgJ8NZDP2ei_KpiF8s8",
        type=str,
    )
    argsparser.add_argument(
        "-w",
        "--web server",
        help='Path to the validation result files. \
Ex: "http://3.96.234.48:18010/QW/ONE01/2022-04-21-2022-05-01/"',
        type=str,
    )
    args = argsparser.parse_args()
    default_parameters = get_default_parameters()

    gitlabUrl = args.gitlabUrl if args.gitlabUrl is not None\
        else default_parameters.GITLAB_URL
    projectId = args.projectId if args.projectId is not None\
        else default_parameters.PROJECT_ID
    projectToken = args.projectToken if args.projectToken is not None\
        else default_parameters.PROJECT_TOKEN
    webserver = args.webserver if args.webserver is not None\
        else default_parameters.WEB_SERVER

    return UserInput(gitlabUrl=gitlabUrl,
                     projectId=projectId,
                     projectToken=projectToken,
                     webserver=webserver
                     )
