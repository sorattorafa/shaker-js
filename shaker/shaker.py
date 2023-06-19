#!/usr/bin/env python3

import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from requests import post
import failure_parser
from print_failures import print_failures
# tools
from tool_maven import Maven
from tool_pytest import Pytest
from tool_jest import Jest
from tool_karma import Karma


def main(args):
    tools = {"pytest": Pytest, "maven": Maven , "jest": Jest, "karma": Karma }

    # Environment setup
    directory = Path(args.directory)
    extra_arguments = args.extra_arguments
    output_folder = Path(
        args.output_folder if args.output_folder else "./output")
    no_stress_runs = args.no_stress_runs
    stress_runs = args.stress_runs
    config_file = Path(__file__).parent / "stressConfigurations.json"
    tests_path = args.tests_path

    with open(config_file) as json_file:
        configs = json.load(json_file)

    # Construct tool object and set it up
    tool = tools[args.tool](directory, extra_arguments, configs, output_folder, tests_path)

    logging.basicConfig(level=logging.DEBUG)
    logging.info(
        f"Running {args.tool} with {no_stress_runs} no-stress runs and {stress_runs} stress runs..."
    )

    sleep(2)

    tests_command = args.tests_command

    # Run tests
    for i in range(0, no_stress_runs):
        tool.no_stress(i, tests_command)

    for i in range(0, stress_runs):
        tool.stress(i, tests_command)

    # Save results
    failures = failure_parser.parse(output_folder)
    with open(output_folder / "__results.json", "w") as f:
        json.dump(failures, f)

    # Show results
    if len(failures) != 0:
        post_failures(args, failures)
        print_failures(failures, no_stress_runs, stress_runs, 4)
        exit(1)
    else:
        exit(0)

def post_failures(args, failures):
    total_runs = args.no_stress_runs + (args.stress_runs * 4)

    repoInfo = { "name": args.directory }
        
    modules = []

    for module in failures:
        saved_module = {
            'name': module,
            'test_cases': []
        }
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
                        
                saved_module['test_cases'].append({
                    'test_name': testCaseName,
                    'test_result': failure,
                    'test_run_configuration_id': tests_run_configurations_type
                })
        modules.append(saved_module)

    testsReportObject = {
        "project_infos": {
            "name": repoInfo["name"],
            #"commit": repoInfo["ref"]
        },
        "total_runs": total_runs,
        "tests_run_configurations": [
            {
                "type": 'plain',
                "id": "plain",
                "running_times": args.no_stress_runs
            },
            {
                "type": 'stress',
                "id": "stress",
                "running_times": args.stress_runs * 4
            },                   
        ],
        "modulos": modules
    }
    post("https://flakybd-97b53-default-rtdb.firebaseio.com/.json", json=testsReportObject)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "tool", choices=["pytest", "maven", "jest", "karma"], help="specify testing tool"
    )
    parser.add_argument("directory", help="specify directory")
    parser.add_argument("-e", "--extra-arguments",
                        help="specify extra arguments")
    parser.add_argument("-o", "--output-folder", help="specify output folder")
    parser.add_argument(
        "-sr",
        "--stress-runs",
        type=int,
        default=3,
        help="specify number of stress runs",
    )
    parser.add_argument(
        "-nsr",
        "--no-stress-runs",
        type=int,
        default=0,
        help="specify number of no-stress runs",
    )

    parser.add_argument(
        "-tp",
        "--tests-path",
        help="specify the path of the test you want Shaker to run",
    )

    parser.add_argument(
        "-tc",
        "--tests-command",
        default="npm run test",
        type=str,
        help="specify the command to tun tests you want Flaky Forcer to run",
    )

    args = parser.parse_args()

    main(args)
