import xml.etree.ElementTree as ET
bboxes = [{'xmin': 1346, 'ymin': 1060, 'xmax': 1372, 'ymax': 1111}, {'xmin': 1372, 'ymin': 1058, 'xmax': 1398, 'ymax': 1109}]

classes = ['N_0', 'N_2']
xml_path = "C:/Users/rt_la/PycharmProjects/check_label"
file_name = "8-강원-02-보-5169.xml"

try:
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = "8-강원-02-보-5169.xml"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = "1969"
    ET.SubElement(size, "height").text = "1806"
    ET.SubElement(size, "depth").text = "3"

    for index, box in enumerate(bboxes):
        objectBox = ET.SubElement(annotation, 'object')
        ET.SubElement(objectBox, 'name').text = classes[index]
        ET.SubElement(objectBox, 'pose').text = 'Unspecified'
        ET.SubElement(objectBox, 'truncated').text = '0'
        ET.SubElement(objectBox, 'difficult').text = '0'
        bndbox = ET.SubElement(objectBox, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(box['xmin'])
        ET.SubElement(bndbox, 'ymin').text = str(box['ymin'])
        ET.SubElement(bndbox, 'xmax').text = str(box['xmax'])
        ET.SubElement(bndbox, 'ymax').text = str(box['ymax'])

    arquivo = ET.Element(annotation)
    arquivo.write(f'{xml_path}/{file_name.split(".")[0]}.xml')
except Exception as e:
    print('Error to generate the XML for image {}'.format(file_name))
    print(e)
