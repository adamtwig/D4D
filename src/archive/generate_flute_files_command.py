from worker_flow import *
#file_paths = ['/opt2/D4D/senegal/data/SET3/raw/SET3_M01.CSV']
'''
# Construct a sample data set for testiing
sample_set(sample_file,'../data_files/set_3_stunted_sample.CSV',1000)
print 'Sample Set Created!!!'
'''

caller_movement_file = '/opt2/D4D/senegal/data/SET3/meta_data/user_cronological_locality.csv'
caller_ids_file = '/opt2/D4D/senegal/data/SET3/meta_data/set_3_caller_ids.csv'
num_regions = 123
regions_file = '/opt2/D4D/senegal/data/SET3/meta_data/senegal_region.csv'
coordinates_file = '/opt2/D4D/senegal/data/SET3/meta_data/senegal_region_coordinates.csv'
worker_flow_file = '/opt2/D4D/senegal/data/SET3/meta_data/flute_worker_flow.csv'
tract_population_file = '/opt2/D4D/senegal/data/SET3/meta_data/flute_tract_population.csv'
'''
caller_movement_file = '../metadata/user_cronological_locality.csv'
caller_ids_file = '../metadata/set_3_caller_ids.csv'
num_regions = 123
regions_file = '../metadata/senegal_region.csv'
coordinates_file = '../metadata/senegal_region_coordinates.csv'
worker_flow_file = '../metadata/flute_worker_flow.csv'
tract_population_file = '../metadata/flute_tract_population.csv'
'''
file_paths = load_in_files('../data_files/set_3_files.csv')

caller_Movement(file_paths,caller_movement_file, num_regions, caller_ids_file)
print 'user_cronological_locality.csv		Constructed!!!'

