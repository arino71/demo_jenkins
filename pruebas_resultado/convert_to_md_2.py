from robot.api import ResultVisitor, ExecutionResult
from robot.result.model import TestCase, Keyword
from datetime import datetime
import json
import logging

import sys
import os

class VisitTest(ResultVisitor):

    def __init__(self, output_file='hp_alm.md'):
        self.test_dict = {}
        # self.steps_list = []
        self.messages_list = []
        self.output_file = output_file
        
    def visit_test(self, test: TestCase):

        test_element = {}
        test_values =[]

        id_test = test.id
        name = test.name
        status = test.status
        start_time = test.start_time
        end_time = test.end_time
        date = start_time.date().isoformat()
        hour = start_time.time().isoformat(timespec='seconds')
        elapsed = test.elapsedtime/1000
        message = test.message

        logging.debug('Start Test'.center(80, '='))
        logging.debug(name + f" - Resultado: {status}")
        logging.debug(f"Start: {start_time} - End: {end_time} - Status: {status}")
        logging.debug(f"Executed in {elapsed} seconds.")
        logging.debug(''.center(80, '='))

        # agrego encabezado del test case

        test_element['test_name'] = name
        test_element['status'] = status
        test_element['start_time'] = start_time.isoformat()
        test_element['end_time'] = end_time.isoformat()
        test_element['date'] = date
        test_element['hour'] = hour
        test_element['duration'] = elapsed

        if status != 'PASS':
            logging.debug(f"Message: {test.message}")
            test_element['message'] = test.message

        test_case = test.body.filter()

        # recorro las keyword del objeto TestCase

        for tc in test_case:

            test_steps = tc.body.filter()

            steps_list = []

            # recorro los steps de test case

            for step in test_steps:

                # test step

                step_dict = {}

                step_start = step.start_time
                step_end = step.end_time
                step_dict['name'] = step.name
                step_dict['status'] = step.status
                step_dict['start_time'] = step_start.isoformat()
                step_dict['end_date'] = step_end.isoformat()
                step_dict['date'] = step_start.date().isoformat()
                step_dict['hour'] = step_start.time().isoformat(timespec='seconds')
                step_dict['duration'] = step.elapsedtime/1000

                # pasos y mensajes
                
                self.messages_list = []

                step.visit(self)

                step_dict['msg'] = ' \n'.join(self.messages_list)   # agrego los mensajes al step
            
                steps_list.append(step_dict)
            
        logging.debug('End Test'.center(80, '='))

        test_element['steps'] = steps_list  # agrego el step al test case

        self.test_dict[id_test] = test_element

    def visit_keyword(self, keyword: Keyword):
        logging.debug(keyword.name)
        self.messages_list.append(f"{keyword.type} - {keyword.start_time.isoformat()} - {keyword.name} {' '.join(keyword.args)} \n")
        # self.messages_list.append(f"<b>{keyword.type} - {keyword.start_time.isoformat()}</b> - {keyword.name} {' '.join(keyword.args)}<br />")

        keyword.body.visit(self)
        return keyword
    
    def visit_message(self, message):
        logging.debug(message.html_message)
        self.messages_list.append(f"{message.level} - {message.timestamp.isoformat()} - {message.html_message} \n")
        # tabla = f'<table widht="100"><tbody><tr class="message-row"><td>{message.timestamp.isoformat()}</td><td>{message.level}</td><td>{message.html_message}</td></tr></tbody></table>'
        # self.messages_list.append(tabla)
        return message.html_message
    
    # def itter_elements_keywords(self, element):
    #     return element.body.filter()   
    
    def end_result(self, result):
        # Create a new markdown file
        print(f"Writing output file {self.output_file}")    
        
        with open(self.output_file, 'w') as file:
            file.write(json.dumps(self.test_dict))
        
    def conversion_fechas(self, fecha):
        try:
            return datetime.fromisoformat(fecha)
        except:
            return datetime.strptime(fecha, '%Y%m%d %H:%M:%S.%f')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_output.xml>")
        sys.exit(1)
    
    output_xml_path = sys.argv[1]
    # Parse the output.xml file
    result = ExecutionResult(output_xml_path)
    # Visit results and create the Markdown file
    visitor = VisitTest('test_results.md')
    result.visit(visitor)