from robot.api import ExecutionResult, ResultVisitor
import sys
import os

class MarkdownVisitor(ResultVisitor):
    def __init__(self, markdown_file='report.md'):
        self.failed_tests = []
        self.passed_tests = []
        self.markdown_file = markdown_file

    def visit_test(self, test):
        """Collects test names and statuses."""
        if test.status == 'FAIL':
            self.failed_tests.append(test.name)
        elif test.status == 'PASS':
            self.passed_tests.append(test.name)

    def end_result(self, result):
        """Writes the collected data to a Markdown file."""
        cr = os.linesep
        with open(self.markdown_file, "w") as f:
            f.write(f"# Robot Framework Report{cr}")
            f.write(f"| Test | Status |{cr}")
            f.write(f"|---|---|{cr}")
            for test in self.passed_tests:
                f.write(f"| {test} | PASS |{cr}")
            for test in self.failed_tests:
                f.write(f"| {test} | FAIL |{cr}")
        print(f"Report generated: {self.markdown_file}")

# Usage:
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_output.xml>")
        sys.exit(1)
    
    output_xml_path = sys.argv[1]
    # Parse the output.xml file
    result = ExecutionResult(output_xml_path)
    # Visit results and create the Markdown file
    visitor = MarkdownVisitor('test_results.md')
    result.visit(visitor)