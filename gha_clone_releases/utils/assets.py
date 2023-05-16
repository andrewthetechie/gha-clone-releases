import os
import requests
import tempfile
from actions_toolkit import core as actions_toolkit


def download_asset(asset_name: str, asset_url: str, token: str) -> str:
    """Downloads an asset from a release and returns the path to the downloaded file"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/octet-stream",
    }
    response = requests.get(asset_url, stream=True, headers=headers, timeout=(60, 300))
    actions_toolkit.debug(f"{asset_url} Response status code: {response.status_code}")
    response.raise_for_status()  # Check for any errors during the request

    # Create a temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp()

    # Construct the full path to the downloaded file
    file_path = os.path.join(temp_dir, asset_name)

    # Write the response content to the file
    with open(file_path, "wb") as fh:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # Filter out any potential empty chunks
                fh.write(chunk)

    actions_toolkit.debug(f"{asset_url} downloaded to {file_path}")
    return file_path
