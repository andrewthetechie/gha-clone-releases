# gha-clone-releases
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/andrewthetechie/gha-clone-releases)
[![Actions Status](https://github.com/andrewthetechie/gha-clone-releases/workflows/Lint/badge.svg)](https://github.com/andrewthetechie/gha-clone-releases/actions)
[![Actions Status](https://github.com/andrewthetechie/gha-clone-releases/workflows/Integration%20Test/badge.svg)](https://github.com/andrewthetechie/gha-clone-releases/actions)

<!-- action-docs-description -->
## Description

Clone the releases in one repo to this one


<!-- action-docs-description -->

This github action can clone releases from a source repo to your repo. This is useful if you are using a repo to build container
images for an upstream container. You can run this action on a cron schedule to pick up new releases and build new containers.

## Usage

On each run, it will find all releases in `src_repo` and the `dest_repo`, find any releases that exist in `src_repo` and not in your `dest_repo`, and then will create those releases in `dest_repo`.

If you don't define a `dest_repo`, it will use the repo the action is running on as a destination.

### Private Repos

To use this repo with a private repo, you must use a Personal Access Token with access to both the `src_repo` and `dest_repo` as your `token`.

### Github Enterprise

Currently, this action does not support Github Enterprise. If you would like to see support for Github Enterprise, [please vote on this issue](https://github.com/andrewthetechie/gha-clone-releases/issues/32).

### Example workflow

Here is an example usage of this workflow. If you set this up, every time it runs it would create releases in your repo that mirror the releases in andrewthetechie/testrepo.

```yaml
name: Clone
on:
  # kick off the job on demand
  workflow_dispatch:
  # and run on a schedule every 12 hours
  schedule:
    - cron: "* */12 * * *"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run action
        uses: andrewthetechie/gha-clone-releases@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          src_repo: andrewthetechie/test-repo
```

<!-- action-docs-inputs -->
## Inputs

| parameter | description | required | default |
| - | - | - | - |
| token | Github token | `true` |  |
| src_repo | Source repo to clone from | `true` |  |
| src_repo_github_api_url | API repo for the src_repo. Defaults to Github. Set this if using GHE | `false` | https://api.github.com |
| dest_repo | Destination repo to clone to, default is this repo | `false` |  |
| dest_repo_github_api_url | API repo for the dest_repo. Defaults to Github. Set this if using GHE | `false` | https://api.github.com |
| target | Target for new tags/releases in this repo. If not set, will use the default branch | `false` |  |
| skip_draft | Skip draft releases | `false` | false |
| skip_prerelease | Skip Prereleases | `false` | false |
| copy_assets | If true, copy assets from source repo releases to the newly created releases | `false` | false |
| limit | A limit of how many releases to add on a single run. Good for not overwhelming CI systems | `false` | 0 |
| dry_run | If true, just output what releases would have been made but do not make releases | `false` | false |
| min_version | If set, we will ignore any releases from the source repo that are less than min_version | `false` |  |



<!-- action-docs-inputs -->

<!-- action-docs-outputs -->
## Outputs

| parameter | description |
| - | - |
| addedReleases | Comma separated list of all the releases created |
| addedReleasesCount | Count of releases added |
| skippedReleasesCount | Count of releases skipped |



<!-- action-docs-outputs -->

<!-- action-docs-runs -->
## Runs

This action is a `docker` action.


<!-- action-docs-runs -->

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/andrewthetechie"><img src="https://avatars.githubusercontent.com/u/1377314?v=4?s=100" width="100px;" alt="Andrew"/><br /><sub><b>Andrew</b></sub></a><br /><a href="https://github.com/andrewthetechie/gha-clone-releases/commits?author=andrewthetechie" title="Code">💻</a> <a href="https://github.com/andrewthetechie/gha-clone-releases/commits?author=andrewthetechie" title="Documentation">📖</a> <a href="#ideas-andrewthetechie" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/andrewthetechie/gha-clone-releases/commits?author=andrewthetechie" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jrbe228"><img src="https://avatars.githubusercontent.com/u/88258057?v=4?s=100" width="100px;" alt="jrbe228"/><br /><sub><b>jrbe228</b></sub></a><br /><a href="https://github.com/andrewthetechie/gha-clone-releases/issues?q=author%3Ajrbe228" title="Bug reports">🐛</a> <a href="#ideas-jrbe228" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
