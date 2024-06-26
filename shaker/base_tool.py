import shutil
from time import sleep

from util import subprocess_Popen


class BaseTool:
    def __init__(self, directory, extra_arguments, configs, output_folder, tests_path, stress_ng_path):
        self.directory = directory
        self.extra_arguments = extra_arguments
        self.configs = configs
        self.output_folder = output_folder
        self.stress_ng_process = None
        self.tests_path = tests_path
        self.stress_ng_path = stress_ng_path

        # Clear the output folder
        shutil.rmtree(self.output_folder, ignore_errors=True)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.setup()

    def start_stress_ng(self, config):
        command = f"{self.stress_ng_path} --cpu {config['cpuWorkers']} --cpu-load {config['cpuLoad']} --vm {config['vmWorkers']} --vm-bytes {config['vmBytes']}%"
        # print(f"> {command}")
        self.stress_ng_process = subprocess_Popen(command)

        sleep(2)

    def stop_stress_ng(self):
        self.stress_ng_process.kill()

    def no_stress(self, run_number, tests_command):
        report_folder = self.output_folder / f"report.no-stress.{run_number}"

        self.run_tests(report_folder, tests_command)
        self.post_tests(report_folder)

    def stress(self, run_number, tests_command):
        for i, config in enumerate(self.configs):
            report_folder = self.output_folder / f"report.{i}.{run_number}"

            self.start_stress_ng(config)
            self.run_tests(report_folder, tests_command)
            self.stop_stress_ng()
            self.post_tests(report_folder)

    # Implement these
    def setup(self):
        pass

    def post_tests(self, report_folder):
        pass

    def run_tests(self, report_folder):
        pass
