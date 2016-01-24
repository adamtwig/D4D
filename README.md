# Grand Valley State University (GVSU)
# Computational Science Research
## Adam Terwilliger
### Credits: Michael Baldwin, Bishal Chamling, Jonathan Leidig, Morgan Oneka, Greg Wolffe

#### Summary
##### Working with data obtained from the Data 4 Development (D4D) challenge, we look to better understand how people move and how diseases spread using over a billion observations. We are employing data mining and pattern recognition techniques using Python.   

##### Data Format:
[   
    ['user_id', 'timestamp', 'site_id']   
    ['user_id', 'timestamp', 'site_id']    
    ...     
]    

##### Data Info:
123 arrondisemonts
1666 antennas
~300,000 users


##### Guide to the repository
data -- timestamp removed datasets  
	 -- antenna/arrondisemont locations  

docs -- helpful links  
	 -- notes from research meetings  

output -- full_movement.txt -- show aggregate 2-mer number of movements   
	   -- out_data -- contains number of users for each antenna for all five definitions of home location for all weeks for antennas  
	   -- user1_out.txt -- contains enumeration of all of user 1 specific patterns for first two weeks  
  

src -- AMP_AT.py -- current working code to enumerate specific users patterns of movement  
	-- anon_data_AT.py -- generates an "anonymized" dataset with timesteps removed   
	-- ant_pairs_AT.py -- aggregates movements between antennas for all users   
	-- BC_working -- directory dedicated to Bishal's migration code   
	-- dist_between_antennas.py -- self evident   
	-- home_calc_AT.py -- generates five definitions of home location output for antennas   
	-- home_calc_functions_AT.py -- helper functions to generate home locations    

##### Current Work
* Aggregate specific users patterns of movements
* Enumerate first 10 users' specific patterns of movements
* Generate summary statistics on first 10 users' patterns
* Home location by arrondisemont by all home location definitions
* Enumerate a single user's abstract pattern of movements

##### Future Work
* Enumerate all users' specific patterns of movements
* Enumerate all users' abstract patterns of movements
* Home location user list for all weeks
* Generate a geographical and interactive data visualization using D3.js to understand aggregate user movement

##### Potential Directions
* Clustering users based on movement patterns and investigate their home location to infer any sociological and cultural phenomena
* Using movement patterns, develop a model that can generate a set of random users (synthetic dataset)
* Using movement patterns, develop a model that can differentiate (i.e classify) a user's country (Senegal vs. Ivory Coast)

- [Link to D4D](http://www.d4d.orange.com/)
