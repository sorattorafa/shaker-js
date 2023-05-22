# shaker-standalone

Shaker is a script that detects flakiness in codebases by introducing noise and load to the execution environment. It currently supports pytest and Maven. For each stress run, it will run the tests once for each one of the 4 stress configurations.

## Usage

```
usage: ./shaker-js/shaker/shaker.py jest "jests-tests-example" -tc "yarn test" -o "jests-tests-example/output" -sr 1 -nsr 1

positional arguments:
  {pytest,maven}        specify testing tool
  directory             specify directory

optional arguments:
  -h, --help            show this help message and exit
  -e EXTRA_ARGUMENTS, --extra-arguments EXTRA_ARGUMENTS
                        specify extra arguments
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        specify output folder
  -sr STRESS_RUNS, --stress-runs STRESS_RUNS
                        specify number of stress runs
  -nsr NO_STRESS_RUNS, --no-stress-runs NO_STRESS_RUNS
                        specify number of no-stress runs
  -tc TESTS_COMMAND, --tests-command TESTS_COMMAND
                        specify the path of the test(s) Shaker will execute
```

## Examples

## Jest example 

- ./shaker-js/shaker/shaker.py jest "jests-tests-example" -tc "yarn test" -o "jests-tests-example/output" -sr 1 -nsr 1

## Karma example

- ./shaker-js/shaker/shaker.py karma "react-helmet-tree-a2323ad" -tc "yarn test" -o "react-helmet-tree-a2323ad/output" -sr 1 -nsr 1