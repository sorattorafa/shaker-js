from pathlib import Path
from xml.etree import ElementTree
import time

def order(entry):
    # Sort by configuration then run number
    if entry["config"] == "no-stress":
        return (-1, int(entry["run_number"]))
    else:
        return (int(entry["config"]), int(entry["run_number"]))

def find_xml_files(dir):
    xml_files = []
    if(len(list(Path(dir.absolute().name).rglob('*.xml'))) != 0):
        xml_files = list(Path(dir.absolute().name).rglob('*.xml'))
    elif(len(list(Path(dir).rglob('*.xml'))) != 0):
        xml_files = list(Path(dir).rglob('*.xml'))
    print(xml_files,  'xml_files')
    return xml_files
    
# Parses all xml files in the project folder
def parse(dir):

    failures = dict()
    
    for sub_directory_name in find_xml_files(dir):
        sub_directory = Path(sub_directory_name)
        config = sub_directory.name.split(".")[1].strip()
        run_number = sub_directory.name.split(".")[2].strip()

        if(sub_directory_name != None):
            xml_file = sub_directory_name
            root = ElementTree.parse(xml_file).getroot()

            testcases = root.findall("testcase")

            if testcases == []:
                testcases = root.findall("testsuite/testcase")

            for testcase in testcases:
                attributes = testcase.attrib

                class_name = attributes["classname"].strip()
                name = attributes["name"].strip()

                for failure in testcase.findall("failure"):
                    description = failure.text.strip()

                    key = class_name
                    key2 = name
                    value = [
                        {
                            "config": config,
                            "run_number": run_number,
                            "description": description,
                        }
                    ]

                    if key not in failures:
                        failures[key] = dict()
                        failures[key][key2] = value
                    else:
                        if key2 not in failures[key]:
                            failures[key][key2] = value
                        else:
                            failures[key][key2].extend(value)

    #for key in failures:
    #    for key2 in failures[key]:
    #        failures[key][key2].sort(key=order)

    return failures


"""import json
failures = parse(Path("./output"))
print(json.dumps(failures, indent = 4))
import print_failures
print_failures.print_failures(failures, 1, 1, 4)"""
