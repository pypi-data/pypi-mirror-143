import os

from utils import www


def _get_remote_file_path(file):
    return os.path.join(
        'https://raw.githubusercontent.com',
        'nuuuwan/gig-data/master',
        file,
    )


def _get_remote_tsv_data(file):
    return www.read_tsv(_get_remote_file_path(file))


def _get_remote_json_data(file):
    return www.read_json(_get_remote_file_path(file))
