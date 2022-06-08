import os
from typing import List

from actions_toolkit import core as actions_toolkit
from github import Github
from github.GithubException import GithubException
from github.GitRelease import GitRelease


class ReleaseWrapper:
    def __init__(self, release: GitRelease):
        self.release = release

    def __eq__(self, other_release: GitRelease):
        return self.release.title == other_release.release.title

    def __hash__(self):
        return hash(self.release.title)


def get_missing_releases(source_releases, dest_releases) -> List[GitRelease]:
    """Compares two sets of releases and returns a list of releases in the source that are not in the destination"""

    def sort_key(release: GitRelease):
        return release.title

    source_releases = {ReleaseWrapper(release) for release in source_releases}
    dest_releases = {ReleaseWrapper(release) for release in dest_releases}
    releases = [release.release for release in list(source_releases - dest_releases)]
    releases.sort(key=lambda release: release.published_at, reverse=True)
    return releases


def main():
    """Get all releases from a source repo and create them on
    the repo we are running this action in
    """

    token = actions_toolkit.get_input("token", required=True)
    src_repo_str = actions_toolkit.get_input("repo", required=True)
    target = actions_toolkit.get_input("target", required=False)
    dry_run = actions_toolkit.get_input("dry_run", required=False).lower() == "true"
    limit_str = actions_toolkit.get_input("limit", required=False).lower()
    limit = int(limit_str) if limit_str != "" and limit_str.isnumeric() else 0
    skip_draft = actions_toolkit.get_input("skip_draft", required=False).lower() == "true"
    skip_prerelease = actions_toolkit.get_input("skip_prerelease", required=False).lower() == "true"
    this_repo_str = os.environ.get("GITHUB_REPOSITORY")

    g = Github(token)
    src_releases = g.get_repo(src_repo_str).get_releases()

    this_repo = g.get_repo(this_repo_str)
    this_releases = this_repo.get_releases()
    added_releases = []
    actions_toolkit.info(f"{src_repo_str} has {src_releases.totalCount} releases")
    actions_toolkit.info(f"{this_repo_str} has {this_releases.totalCount} releases")

    for count, release in enumerate(get_missing_releases(src_releases, this_releases)):
        if count >= limit and limit != 0:
            break
        if skip_draft and release.draft:
            actions_toolkit.info(f"Skipping {release.tag_name} due to skip_draft")
            continue
        if skip_prerelease and release.prerelease:
            actions_toolkit.info(f"Skipping {release.tag_name} due to skip_prerelease")
            continue
        if dry_run:
            actions_toolkit.info(f"Would have added {release.tag_name} to {this_repo_str} with title {release.title}")
            continue
        actions_toolkit.info(f"Adding {release.tag_name} to {this_repo_str}")
        try:
            this_repo.create_git_release(
                release.tag_name,
                release.title,
                release.body,
                release.prerelease,
                target_commitish=target,
            )
            added_releases.append(release.tag_name)
        except GithubException as exc:
            actions_toolkit.error(f"Error while adding a release for {release.tag_name}. {exc}")
    actions_toolkit.set_output("addedReleases", ",".join(added_releases))


if __name__ == "__main__":
    main()
