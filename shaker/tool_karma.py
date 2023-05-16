from pathlib import Path
from base_tool import BaseTool
from util import subprocess_run

class Karma(BaseTool):

    def add_report_lib(self):
        command = f"npm install karma-junit-reporter"
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
        string_report = string_report.split('/output/')[1] + '.xml'
        command = (
            f"{tests_command} {self.tests_path} --reporters=default --reporters=junit --outputFile=${string_report} --outputDir='output/'"
            if self.tests_path else f"{tests_command} --reporters=default --reporters=junit --outputFile=${string_report} --outputDir='output/'"
        )
        stdout_ = open(self.output_folder /
                       "exec_setup.out", "a")
        stderr_ = open(self.output_folder / "exec_setup.err", "a")
        
        subprocess_run(command, stderr=stderr_, stdout=stdout_, cwd=str(self.directory), env=None)
