import subprocess
import os

from datetime import date, timedelta


def cleanup_directory(
    network: str,
    station: str,
    startdate: date,
    enddate: date,
    outputdir: str,
):
    '''
    Function to clean up after the program runs.

    Parameters
    ----------
    network: string
        Network code used for naming the tarball of output files

    station: string
        The station code, used for naming the tarball of output files

    startdate: date
        The start date to use in the name of the tarball of output files

    enddate: date
        The end date to use in the name of the tarball output

    outputdir: string
        Path to the directory to deposit output tarball in. Default = None

    '''
    # Create the final directory that the data will be placed in
    if startdate == enddate - timedelta(days=1):
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}'
    else:
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}-{enddate}'
    # Create the directory if it doesn't already exist
    if not os.path.isdir(validation_output_directory):
        subprocess.getoutput(
            f"mkdir -p '{validation_output_directory}'")
    pdffiles = f'ispaq_outputs/PDFs/{network}/{station}/*.png'
    # Move current outputs to the directory specified
    subprocess.getoutput(
        f"mv {pdffiles} {validation_output_directory}/")
    subprocess.getoutput(
        f"mv ./stationvalidation_output/* {validation_output_directory}")  # noqa

    subprocess.getoutput(
        "rm -rf stationvalidation_output")

    subprocess.getoutput(
        f"mv ISPAQ_TRANSCRIPT.log {validation_output_directory}")

    subprocess.getoutput(
        "rm -rf ispaq_outputs")
