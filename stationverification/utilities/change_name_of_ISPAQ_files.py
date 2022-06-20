# flake8:noqa
import subprocess
import logging

from pathlib import Path


def change_name_of_ISPAQ_files(network: str,
                               station: str):
    proccess_PDF_directory(network=network,
                           station=station)
    proccess_PSD_directory(network=network,
                           station=station)


def proccess_PDF_directory(network: str,
                           station: str):
    files: list = []
    path_to_pngs = f"ispaq_outputs/PDFs/{network}/{station}/*.png"
    cmd = f'ls {path_to_pngs}'
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
    path_to_csvs = f"ispaq_outputs/PDFs/{network}/{station}/*.csv"
    cmd = f'ls {path_to_csvs}'
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


def proccess_PSD_directory(network: str,
                           station: str):
    files: list = []
    path_to_pngs = f"ispaq_outputs/PSDs/{network}/{station}/*.csv"
    cmd = f'ls {path_to_pngs}'
    output = subprocess.getoutput(
        cmd
    ).split('\n')
    if not output == ['']:
        files.extend(output)
    for file in files:
        path_to_file = Path(file)
        new_file_name = file.replace(
            ".D_", ".").replace("_PSDCorrected", ".psdcorrected")
        if path_to_file.exists():
            subprocess.getoutput(
                f"mv {file} {new_file_name}")
