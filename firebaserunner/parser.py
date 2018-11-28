import xml.etree.ElementTree as ET

tree = ET.parse('../test_result/test_result_1.xml')
root = tree.getroot()

print('Tests Ran: ' + root.attrib['tests'])
print('Errors: ' + root.attrib['failures'])
print('Skipped: ' + root.attrib['skipped'])