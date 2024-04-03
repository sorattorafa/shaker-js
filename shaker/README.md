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

em alguns casos de testes nodejs é necessário fazer o setup do nodejs com o comando:

sudo apt install node-gyp0

## Jest example 

- ./shaker-js/shaker/shaker.py jest "jests-tests-example" -tc "yarn test" -o "jests-tests-example/output" -sr 1 -nsr 1

## Karma example


### Add karma-junit-reporter-lib

- `npm i karma-junit-reporter` 
- Add reporter config:
``` 


const reporters = ['dots', 'progress', 'junit']

plugins.push('karma-junit-reporter')
config.frameworks = frameworks
config.plugins = plugins
config.reporters = reporters
config.junitReporter = {
  outputDir: 'output', // os resultados serão salvos como $outputDir/$browserName.xml
  outputFile: process.env.JEST_JUNIT_OUTPUT_NAME, // se incluído, os resultados serão salvos como $outputDir/$browserName/$outputFile
  useBrowserName: true, // adicione o nome do navegador ao relatório e aos nomes das classes
  suite: '', // suite will become the package name attribute in xml testsuite element
  useBrowserName: true, // add browser name to report and classes names
  nameFormatter: function (browser, result) {
    return result.description; // Use a descrição do teste como o nome
  },

  classNameFormatter: function (browser, result) {
    return result.suite.join('.'); // Use o caminho da suíte de teste como a classe
  }, // function (browser, result) to customize the classname attribute in xml testcase element
  properties: {}, // key value pair of properties to add to the <properties> section of the report
  xmlVersion: null // use '1' if reporting to be per SonarQube 6.2 XML format
}
``` 

- Run command: `./shaker-js/shaker/shaker.py karma "react-helmet-tree-a2323ad" -tc "yarn test" -o "react-helmet-tree-a2323ad/output" -sr 1 -nsr 1`


