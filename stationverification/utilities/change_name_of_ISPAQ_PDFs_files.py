# flake8:noqa
import subprocess
import logging

from pathlib import Path


def change_name_of_ISPAQ_PDFs_files(network: str,
                                    station: str):
    files: list = []
    path = f"ispaq_outputs/PDFs/{network}/{station}/*.png"
    cmd = f'ls {path}'
    output = subprocess.getoutput(
        cmd
    ).split('\n')
    if not output == ['']:
        files.extend(output)
    for file in files:
        path_to_file = Path(file)
        new_file_name = file.replace(
            ".D.", ".").replace("_PDF", ".pdf")
        if path_to_file.exists():
            subprocess.getoutput(
                f"mv {file} {new_file_name}")
