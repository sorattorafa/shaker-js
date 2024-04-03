from pathlib import Path
from base_tool import BaseTool
from util import subprocess_run

import os

class Karma(BaseTool):

    def add_report_lib(self):
        command = f"npm i karma-junit-reporter"
        stdout_ = open(self.output_folder /
                       "exec_setup.out", "a")
        stderr_ = open(self.output_folder / "exec_setup.err", "a")
        subprocess_run(command, cwd=str(self.directory),
                       stdout=stdout_, stderr=stderr_)

    def setup(self):
        self.add_report_lib()
        arguments = " --force"
        command = f"npm install{arguments}"
        stdout_ = open(self.output_folder /
                       "exec_setup.out", "a")
        stderr_ = open(self.output_folder / "exec_setup.err", "a")
        subprocess_run(command, cwd=str(self.directory),
                       stdout=stdout_, stderr=stderr_)

    def run_tests(self, report_folder, tests_command):
        
        string_report = str(report_folder)
        output_dir, output_file = string_report.split('/output/')
        output_file += '.xml'
            
        print(output_dir, output_file, 'veja string reports');
            
        env = os.environ.copy()
        env["JEST_JUNIT_UNIQUE_OUTPUT_NAME"] = "true"
        env["JEST_JUNIT_OUTPUT_DIR"] = output_dir
        env["JEST_JUNIT_OUTPUT_NAME"] = output_file
        env["JEST_JUNIT_CLASSNAME"] = "{classname}"
        env["JEST_JUNIT_TITLE"] = "{title}"
            
        command = (
            f"{tests_command} {self.tests_path} --reporters=default --reporters=junit"
            if self.tests_path else f"{tests_command} --reporters=default --reporters=junit"
        )
        stdout_ = open(self.output_folder /
                    "exec_setup.out", "a")
        stderr_ = open(self.output_folder / "exec_setup.err", "a")
            
        subprocess_run(command, stderr=stderr_, stdout=stdout_, cwd=str(self.directory), env=env)