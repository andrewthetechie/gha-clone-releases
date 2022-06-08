# gha-clone-releases

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/andrewthetechie/gha-clone-releases)
[![Actions Status](https://github.com/andrewthetechie/gha-clone-releases/workflows/Lint/badge.svg)](https://github.com/andrewthetechie/gha-clone-releases/actions)
[![Actions Status](https://github.com/andrewthetechie/gha-clone-releases/workflows/Integration%20Test/badge.svg)](https://github.com/andrewthetechie/gha-clone-releases/actions)

This github action can clone releases from a source repo to your repo. This is useful if you are using a repo to build container
images for an upstream container. You can run this action on a cron schedule to pick up new releases and build new containers.

## Usage

On each run, it will find all releases in `repo` and the repo you are running your action on, find any releases that exist in `repo` and not in your repo, and then will create those releases in your repo.

### Example workflow

```yaml
name: Clone
on:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run action
        # Put your action repo here
        uses: andrewthetechie/gha-clone-releases@v1
        # Put an example of your mandatory inputs here
        with:
          token: ${{ secrets.GithubToken }}
          repo: andrewthetechie/andrewthetechie
```

### Inputs

| Input                 | Description                                                                      |
| --------------------- | -------------------------------------------------------------------------------- |
| `token`               | A github token that can publish releases to this repo                            |
| `repo`                | The repository to clone releases from.                                           |
| `target` _(optional)_ | Optional, a target for your releases, default will be your default branch's HEAD |

### Outputs

| Output          | Description                                           |
| --------------- | ----------------------------------------------------- |
| `addedReleases` | A comma separated list of all the releases we created |
