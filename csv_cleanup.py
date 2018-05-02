# This script removes all unusable data from the import csv and
# converts the usable data to the values used in osm.
# It will only keep the rows needed for the xml conversion:
# - osm_id
# - roof
# - material

import csv



#https://wiki.openstreetmap.org/wiki/Simple_3D_buildings#Roof
#roof:shape = flat, gabled, hipped

roof_shapes = {
    'flat': 'flat',
    'hipped': 'hipped',
    'pitched': 'gabled'
}


# returns osm roof:shape or None
def get_osm_roof_shape(roof):
    try:
        return roof_shapes[(roof)]
    except:
        pass




#https://wiki.openstreetmap.org/wiki/Key:roof:material
#roof:material = concrete, metal, roof_tiles, 

roof_materials = {
    1: 'concrete',
    2: 'roof_tiles',
    3: 'metal'
}


# returns osm roof:material or None
def get_osm_material(mat_id):
    try:
        return roof_materials[int(mat_id)]
    except:
        pass




input_file_name = 'roof_types_sxm.csv'
output_file_name = 'roof_types_sxm_clean.csv'


output_file = open(output_file_name, 'w')
output_fieldnames = ['osm_id', 'roof:shape', 'roof:material']
output_writer = csv.DictWriter(output_file, fieldnames=output_fieldnames, delimiter=';')


input_file = open(input_file_name, 'r')
input_reader = csv.DictReader(input_file, delimiter=';')


input_row_cnt = 0
output_row_cnt = 0

output_writer.writeheader()


for input_row in input_reader:
    input_row_cnt += 1
    osm_id = input_row['osm_id']
    roof_shape = get_osm_roof_shape(input_row['roof'])
    roof_material = get_osm_material(input_row['material'])

    if roof_material is not None or roof_shape is not None:
        output_writer.writerow({'osm_id': osm_id, 'roof:shape': roof_shape, 'roof:material': roof_material})
        output_row_cnt += 1


input_file.close()
output_file.close()

print(r'converted:  %s/%s records' % (output_row_cnt, input_row_cnt))
