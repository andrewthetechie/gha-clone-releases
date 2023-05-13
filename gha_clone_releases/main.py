import os
from typing import Any

from actions_toolkit import core as actions_toolkit
from github import Github
from github.GithubException import GithubException

from .utils.assets import download_asset
from .utils.releases import get_missing_releases

# This code is automatically generated by actions.yml and make generate-inputs
###START_INPUT_AUTOMATION###
INPUTS = {
    "token": {"description": "Github token", "required": True},
    "src_repo": {"description": "Source repo to clone from", "required": True},
    "dest_repo": {"description": "Destination repo to clone to, default is this repo", "required": False},
    "target": {
        "description": "Target for new tags/releases in this repo. If not set, will use the default branch",
        "default": "",
    },
    "skip_draft": {"description": "Skip draft releases", "default": False},
    "skip_prerelease": {"description": "Skip Prereleases", "default": False},
    "copy_assets": {
        "description": "If true, copy assets from source repo releases to the newly created releases",
        "default": False,
    },
    "limit": {
        "description": "A limit of how many releases to add on a single run. Good for not overwhelming CI systems",
        "default": 0,
    },
    "dry_run": {
        "description": "If true, just output what releases would have been made but do not make releases",
        "default": False,
    },
    "min_version": {
        "description": "If set, we will ignore any releases from the source repo that are less than min_version",
        "default": "",
    },
}
###END_INPUT_AUTOMATION###


def get_inputs() -> dict[str, Any]:
    """Get inputs from our workflow, valudate them, and return as a dict
    Reads inputs from actions.yaml. Non required inputs that are not set are returned as None
    Returns:
        Dict[str, Any]: [description]
    """
    parsed_inputs = dict()
    for input_name, input_config in INPUTS.items():
        this_input_value = actions_toolkit.get_input(
            input_name,
            required=input_config.get("required", input_config.get("default", None) is None),
        )
        parsed_inputs[input_name] = this_input_value if this_input_value != "" else None
        # set defaults from actions.yaml if not running in github, this is for local testing
        # https://docs.github.com/en/actions/learn-github-actions/environment-variables
        if (
            os.environ.get("CI", "false").lower() == "false"
            and os.environ.get("GITHUB_ACTIONS", "false").lower() == "false"
        ):
            if parsed_inputs[input_name] is None:
                parsed_inputs[input_name] = input_config.get("default", None)
    parsed_inputs["dry_run"] = (
        parsed_inputs["dry_run"].lower() == "true"
        if isinstance(parsed_inputs["dry_run"], str)
        else parsed_inputs["dry_run"]
    )
    parsed_inputs["limit"] = (
        int(parsed_inputs["limit"])
        if not isinstance(parsed_inputs["limit"], int)
        and parsed_inputs["limit"] != ""
        and parsed_inputs["limit"].isnumeric()
        else 0
    )
    parsed_inputs["skip_draft"] = (
        parsed_inputs["skip_draft"].lower() == "true"
        if isinstance(parsed_inputs["skip_draft"], str)
        else parsed_inputs["skip_draft"]
    )
    parsed_inputs["skip_prerelease"] = (
        parsed_inputs["skip_prerelease"].lower() == "true"
        if isinstance(parsed_inputs["skip_prerelease"], str)
        else parsed_inputs["skip_prerelease"]
    )
    parsed_inputs["copy_assets"] = (
        parsed_inputs["copy_assets"].lower() == "true"
        if isinstance(parsed_inputs["copy_assets"], str)
        else parsed_inputs["copy_assets"]
    )
    parsed_inputs["dest_repo"] = (
        os.environ.get("GITHUB_REPOSITORY") if parsed_inputs["dest_repo"] is None else parsed_inputs["dest_repo"]
    )
    if parsed_inputs["dest_repo"] is None:
        actions_toolkit.set_failed("Dest repo is none, set either INPUT_DEST_REPO or GITHUB_REPOSITORY")
    return parsed_inputs


def main():
    """Get all releases from a source repo and create them on
    the repo we are running this action in
    """
    inputs = get_inputs()

    g = Github(inputs["token"])
    src_releases = g.get_repo(inputs["src_repo"]).get_releases()

    this_repo = g.get_repo(inputs["dest_repo"])
    this_releases = this_repo.get_releases()
    added_releases = []
    actions_toolkit.debug(f"{inputs['src_repo']} has {src_releases.totalCount} releases")
    actions_toolkit.debug(f"{inputs['dest_repo']} has {this_releases.totalCount} releases")

    actions_toolkit.debug(f"Limit: {inputs['limit']}")

    skipped = 0
    for count, release in enumerate(get_missing_releases(src_releases, this_releases, inputs["min_version"])):
        if count >= (inputs["limit"] + skipped) and inputs["limit"] != 0:
            actions_toolkit.debug("Hit limit")
            break
        if inputs["skip_draft"] and release.draft:
            actions_toolkit.debug(f"Skipping {release.tag_name} due to skip_draft")
            skipped += 1
            continue
        if inputs["skip_prerelease"] and release.prerelease:
            actions_toolkit.debug(f"Skipping {release.tag_name} due to skip_prerelease")
            skipped += 1
            continue
        if inputs["dry_run"]:
            actions_toolkit.info(
                f"Would have added {release.tag_name} to {inputs['dest_repo']} with title {release.title}"
            )
            continue
        actions_toolkit.info(f"Adding {release.tag_name} to {inputs['dest_repo']}")
        target = this_repo.default_branch if inputs["target"] is None else inputs["target"]
        try:
            new_release = this_repo.create_git_release(
                tag=release.tag_name,
                name=release.title,
                message=release.body,
                draft=release.draft,
                prerelease=release.prerelease,
                target_commitish=target,
            )
            added_releases.append(release.tag_name)
        except GithubException as exc:
            actions_toolkit.error(f"Error while adding a release for {release.tag_name}. {exc}")
        if inputs["copy_assets"]:
            for asset in release.assets:
                try:
                    this_asset = download_asset(asset_name=asset.name, asset_url=asset.browser_download_url)
                    new_release.upload_asset(this_asset)
                except Exception as exc:
                    actions_toolkit.error(f"Error while copying asset {asset.name}. {exc}")
    actions_toolkit.set_output("addedReleases", ",".join(added_releases))
    actions_toolkit.set_output("skippedReleasesCount", skipped)
    actions_toolkit.set_output("addedReleasesCount", len(added_releases))


if __name__ == "__main__":
    main()
