import xml.etree.ElementTree as ET

# Parse coverage XML report
tree = ET.parse('coverage.xml')
root = tree.getroot()

# Find coverage percentage
total_statements = int(root.find('totals').get('statements'))
covered_statements = int(root.find('totals').get('covered'))
coverage_percentage = (covered_statements / total_statements) * 100

# Check if coverage is less than 10%
if coverage_percentage < 10:
    print(f"Coverage is less than 10% ({coverage_percentage:.2f}%)")
    exit(1)  # Fails the build
