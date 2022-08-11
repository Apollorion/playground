import requests
import os
import base64
import json

GITHUB_OWNER = os.environ['GITHUB_OWNER']
GITHUB_REPO = os.environ['GITHUB_REPO']


def get_changed_files():
    # Add anything into git that is new or changed
    os.popen('git add .')

    # Get the list of files that have changed or added since last commit
    changed_files = os.popen('git diff --name-only HEAD').read().splitlines()
    return changed_files


def make_github_request(method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {'Authorization': 'token {}'.format(os.environ['GITHUB_TOKEN'])}
    return requests.request(method, url, headers=headers, data=json.dumps(data)).json()


def get_file_sha(file_path):
    req = make_github_request("GET", f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file_path}")
    if "sha" in req:
        return req["sha"]
    else:
        return False


def get_file_content_base64(file_path):
    file = open(file_path, 'rb')
    return base64.b64encode(file.read()).decode('utf-8')


def main():
    # Get a list of files that have changed or added since last commit
    changed_files = get_changed_files()

    for file in changed_files:
        file_sha = get_file_sha(file)
        new_file_content = get_file_content_base64(file)

        sha = {}
        if file_sha:
            sha["sha"] = file_sha

        data = {
            **sha,
            "message": f"feat($file): update file contents",
            "content": new_file_content,
            "committer": {
                "name": "github-file-updater",
                "email": "no-reply@github.com"
            }
        }

        update = make_github_request("PUT", f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file}", data=data)
        if "content" in update:
            print(f"{file} updated")
        else:
            print(update, data)
            raise Exception(f"Error updating {file}")


if __name__ == "__main__":
    main()
