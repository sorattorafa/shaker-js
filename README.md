[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5347973.svg)](https://doi.org/10.5281/zenodo.5347973)

# shaker

This action uses [shaker](shaker) in your GitHub workflow to detect flakiness. If the job ends in failure, flakes were detected and errors will be reported.

Shaker supports projects using `jest`, `maven` or `pytest`.

## Usage

Add the following code to your GitHub Actions workflow configuration

```yaml
name: Flaky Shaker # This is a basic workflow to help you get started with Actions 

# Controls when the action will run. 
on:
  # Triggers the workflow on push or pull request events but only for the main branch
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
# This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v3
      - name: Jest tests
        uses: sorattorafa/shaker-js@main
        with:
          tool: jest
          tests_command: yarn test:source
          runs: 1
          output_folder: project_name/output
```

## Inputs

| Input | Description |
| --- | --- |
| `tool` | Specifies the tool required to run the tests. Currently supported: `maven` and `pytest`. |
| `extra_arguments` | Optional. Passes extra arguments to the testing tool. For example, you can pass `-DModule.skip.tests=true` to tell Maven to skip a certain module. |
| `runs` | Optional, default: 3. Specifies how many times Shaker will run. |

# Examples


## Jest example 

- ./shaker-js/shaker/shaker.py jest "jests-tests-example" -tc "yarn test" -o "jests-tests-example/output" -sr 1 -nsr 1

## Karma example

- ./shaker-js/shaker/shaker.py karma "react-helmet-tree-a2323ad" -tc "yarn test" -o "react-helmet-tree-a2323ad/output" -sr 1 -nsr 1 

## Github actions example
1 -  Fork the repository (it can be any project of yours).
    - git clone your fork or your own project.
2- Into the project, create a folder called .github/workflows.
    - mkdir -p .github/workflows
3 - Create a file .yml, for example main.yml.
    - touch .github/workflows/main.yml


4 - Write the action that runs Shaker in the .yml file :

```yml
name: CI # This is a basic workflow to help you get started with Actions 

# Controls when the action will run. 
on:
  # Triggers the workflow on push or pull request events but only for the main branch
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2
      - name: Java tests
        uses: STAR-RG/shaker@main
        with:
          tool: maven
          runs: 3
```


and

```shell
git add .github
git commit -m "add shaker action"
git push


git commit --allow-empty -m "empty commit to trigger the action"
git push
```