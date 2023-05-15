from github.GitRelease import GitRelease
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version
from actions_toolkit import core as actions_toolkit


class ReleaseWrapper:
    def __init__(self, release: GitRelease):
        self.release = release

    def __eq__(self, other_release: GitRelease):
        return self.release.title == other_release.release.title

    def __hash__(self):
        return hash(self.release.title)

    def __str__(self):
        return f"{self.release.title} - {self.release.published_at} - {self.release.tag_name}"


def exceeds_min_version(release_version: str, min_version: str):
    """Checks if a version exceeds a minimum version using packaging.version.parse"""
    if min_version is not None:
        try:
            result = parse_version(release_version) > parse_version(min_version)
        except InvalidVersion as exc:
            actions_toolkit.error(f"{release_version} Is an invalid version {exc}")
            return False
        actions_toolkit.debug(f"{release_version} exceeds_min_version result {result}")
        return result
    return True


def get_missing_releases(source_releases, dest_releases, min_version) -> list[GitRelease]:
    """Compares two sets of releases and returns a list of releases in the source that are not in the destination"""

    def sort_key(release: GitRelease):
        return release.title

    actions_toolkit.debug(f"Source releases: {source_releases}")
    actions_toolkit.debug(f"Dest releases: {dest_releases}")

    wrapped_sources = set()
    for release in source_releases:
        if exceeds_min_version(release.title, min_version):
            actions_toolkit.debug(
                f"Source release: {release.title} is greater than {min_version}, will copy to destination"
            )
            wrapped_sources.add(ReleaseWrapper(release))
        else:
            actions_toolkit.debug(
                f"Source release: {release.title} is less than {min_version}, will not copy to destination"
            )

    wrapped_dest_releases = set()
    for release in dest_releases:
        actions_toolkit.debug(f"Dest release: {release.title}")
        wrapped_dest_releases.add(ReleaseWrapper(release))

    releases = [release.release for release in list(wrapped_sources - wrapped_dest_releases)]
    releases.sort(key=lambda release: release.published_at, reverse=True)
    actions_toolkit.debug(f"Releases to add: {releases}")
    return releases
