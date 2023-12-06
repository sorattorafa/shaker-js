from requests import post

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