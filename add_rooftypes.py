#! /bin/python3
import xml.etree.ElementTree as ElementTree
import csv


csv_file_name = 'roof_types_sxm_clean.csv'
input_osm_file_name = "buildings_sxm_input.osm"
output_osm_file_name = "buildings_sxm_output.osm"


csv_file = open(csv_file_name, 'r')
csv_reader = csv.DictReader(csv_file, delimiter=';')




# create roof_info lookup
roof_info_lookup = {}

for row in csv_reader:
    roof_info_lookup[row['osm_id']] = {'roof_shape': row['roof:shape'], 'roof_material': row['roof:material']}

csv_file.close()

print('input roof info count: %s' % (len(roof_info_lookup)))





tree = ElementTree.parse(input_osm_file_name)
osm = tree.getroot()
osm.set('generator', 'add_rooftypes.py')

building_count = 0
match_count = 0
material_edit_count = 0
shape_edit_count = 0


for child in osm:
    if child.tag in {"way", "relation"}:
        building_count += 1
        osm_id = child.get('id')

        roof_info = None
        try:
            roof_info = roof_info_lookup[osm_id]
            match_count += 1
            #print('found %s' % (roof_info))
        except:
            pass
        
        if roof_info is not None:
            
            is_edited = 0

            # add roof shape
            rt = child.findall("./tag[@k='roof:shape']")

            if len(rt) == 0:
                shp = roof_info['roof_shape']
                if shp != '':
                    shape_element = ElementTree.Element('tag')
                    shape_element.set('k', 'roof:shape')
                    shape_element.set('v', shp)
                    child.append(shape_element)
                    shape_edit_count += 1
                    is_edited += 1

            # add roof material
            rt = child.findall("./tag[@k='roof:material']")

            if len(rt) == 0:
                mat = roof_info['roof_material']
                if mat != '':
                    material_element = ElementTree.Element('tag')
                    material_element.set('k', 'roof:material')
                    material_element.set('v', mat)
                    child.append(material_element)
                    material_edit_count += 1
                    is_edited += 1
        
            # mark element as modified.
            if is_edited > 0:
                child.set('action', 'modify')
        

print('matches:               %s/%s' % (match_count, building_count))
print('roof shapes added:     %s/%s' % (shape_edit_count, match_count))
print('roof materials added:  %s/%s' % (material_edit_count, match_count))

tree.write(output_osm_file_name)
