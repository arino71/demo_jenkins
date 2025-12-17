import json
from robot.api import ExecutionResult

# Path to your output.xml file
output_xml_path = 'output.xml'
# Path where you want to save the JSON file
output_json_path = 'output.json'

# Parse the output.xml file using the Robot Framework API
result = ExecutionResult(output_xml_path)

# Convert the result object to a JSON string and save it
# The 'to_json' method handles the complex structure of the results
result.save(output_json_path)

print(f"Successfully converted '{output_xml_path}' to '{output_json_path}'")
