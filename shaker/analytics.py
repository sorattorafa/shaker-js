import json
import time
from argparse import ArgumentParser
from requests import post
from pathlib import Path
import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def get_args():
    parser = ArgumentParser()
    parser.add_argument("output_folder", help="output folder")
    parser.add_argument("repo", help="repository")
    parser.add_argument("ref", help="repository ref")
    parser.add_argument("numtests", type=int, help="number of tests")
    parser.add_argument("nsr", type=int, help="specify number of no-stress runs")
    parser.add_argument("sr", type=int, help="specify number of stress runs")
    args = parser.parse_args()
    return args

def openResultsJson(args):
    print(find_all("__results.json", '../'))
    print(find_all("__results.json", './'))
    f = None
    mode = "r"
    try:
      f = open((Path("./output/") / "__results.json"), mode)
    except IOError:
      pass
    
    if f == None:
            try:
                f = open(find("__results.json", '.'), mode)
            except IOError:
                pass
    if f == None:
            try:
                f = open(find("__results.json", '../'), mode)
            except IOError:
                pass
    return f

def save_flakies():
    args = get_args()
    f = openResultsJson(args)
    if f == None:
        raise Exception("Results file not found")
    else:
        total_runs = args.nsr + (args.sr * 4)

        repoInfo = {"name": args.repo, "ref": args.ref, "num_tests": args.numtests}
        failures = json.load(f)
        
        modules = []
        print(failures, f.read(), 'failures debug')
        for module in failures:
            saved_module = {
                'name': module,
                'test_cases': []
            }
            print(failures[module], 'failures module debug')
            for test_case in failures[module]:
                print(test_case, 'test_case module debug')
                testCaseName = test_case

                function_failures = failures[module][test_case]

                no_stress_failures = 0
                stress_failures = 0
                tests_run_configurations_type = 'plain'
                for failure in function_failures:
                    print(failure, 'test_case module debug')
                    if failure["config"] == "no-stress":
                        no_stress_failures += 1
                    else:
                        tests_run_configurations_type = 'stress'
                        stress_failures += 1
                        
                    saved_module['test_cases'].append({
                        'test_name': testCaseName,
                        'test_result': failure,
                        'test_run_configuration_id': tests_run_configurations_type
                    })
            modules.append(saved_module)

        testsReportObject = {
            "project_infos": {
                "name": repoInfo["name"],
                "commit": repoInfo["ref"]
            },
            "total_runs": total_runs,
            "tests_run_configurations": [
                {
                    "type": 'plain',
                    "id": "plain",
                    "running_times": args.nsr
                },
                {
                    "type": 'stress',
                    "id": "stress",
                    "running_times": args.sr * 4
                },                   
            ],
            "modulos": modules
        }
        post("https://flakybd-97b53-default-rtdb.firebaseio.com/.json", json=testsReportObject)

def save_simplified_flakies():
    
    with open(Path('./output/') / "__results.json") as f:
        args = get_args()
        total_runs = args.nsr + (args.sr * 4)
        repoInfo = {"name": args.repo, "ref": args.ref, "num_tests": args.numtests}
        failures = json.load(f)
        
        for module in failures:
            for test_case in failures[module]:
                testCaseName = test_case

                function_failures = failures[module][test_case]

                no_stress_failures = 0
                stress_failures = 0
                tests_run_configurations_type = 'plain'
                for failure in function_failures:
                    if failure["config"] == "no-stress":
                        no_stress_failures += 1
                    else:
                        tests_run_configurations_type = 'stress'
                        stress_failures += 1
                    flakyPostObject = {
                        "project_name": repoInfo["name"],
                        "project_commit": repoInfo["ref"],
                        "tests_run_configurations_type": tests_run_configurations_type,
                        "run_times": total_runs,
                        "module_name": module,
                        "test_case_name": testCaseName,
                        "created_at": int(time.time()),
                        "test_case_result": failure,
                    }
                    post("https://flakybd-97b53-default-rtdb.firebaseio.com/.json", json=flakyPostObject)

def default_post():
    repoUrl = "https://my-new-app-denini.herokuapp.com/repos"
    flakiesUrl = "https://my-new-app-denini.herokuapp.com/flakies"

    args = get_args()

    total_runs = args.nsr + (args.sr * 4)

    repoInfo = {"name": args.repo, "ref": args.ref, "num_tests": args.numtests}
    repoJson = json.loads(json.dumps(repoInfo))
    post(repoUrl, json=repoJson)

    with open(Path(args.output_folder) / "__results.json") as f:
        failures = json.load(f)

    for module in failures:
        moduleName = module

        for test_case in failures[module]:
            testCaseName = test_case

            function_failures = failures[module][test_case]

            no_stress_failures = 0
            stress_failures = 0

            for failure in function_failures:
                if failure["config"] == "no-stress":
                    no_stress_failures += 1
                else:
                    stress_failures += 1

            total_failures = no_stress_failures + stress_failures
            ratio = total_failures / total_runs

            flaky = {
                "repo": repoInfo["name"],
                "module": module,
                "function_name": testCaseName,
                "datetime_epoch": int(time.time()),
                "ratio": ratio,
            }
            flakyJson = json.loads(json.dumps(flaky))
            post(flakiesUrl, json=flakyJson)

#save_simplified_flakies()
save_flakies()
# / == %2F
