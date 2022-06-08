import os
from actions_toolkit import core as actions_toolkit
from github import Github
from github.Repository import Repository


def main():
    token = actions_toolkit.get_input("token", required=True)
    src_repo_str = actions_toolkit.get_input("repo", required=True)
    target = actions_toolkit.get_input("target", required=False)
    this_repo_str = os.environ.get("GITHUB_REPOSITORY")
    g = Github(token)
    src_repo = g.get_repo(src_repo_str)
    src_releases = src_repo.get_releases()
    this_repo = g.get_repo(this_repo_str)
    this_releases = this_repo.get_releases()
    added_releases = []
    for release in set(src_releases) - set(this_releases):
        actions_toolkit.info(f"Adding {release.tag_name} to {this_repo_str}")
        this_repo.create_git_release(
            release.tag_name,
            release.title,
            release.body,
            release.prerelease,
            target_commitish=target,
        )
        added_releases.append(release.tag_name)
    actions_toolkit.set_output("added_releases", ",".join(added_releases))


if __name__ == "__main__":
    main()
