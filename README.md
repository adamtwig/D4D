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
Five definitions of home: overall, daytime, nighttime, weekday, weekend  

- [Link to D4D](http://www.d4d.orange.com/)

##### Guide to the repository
docs   
	 -- helpful links  
	 -- notes from research meetings  

output    
	   -- full_movement.txt - show aggregate 2-mer number of movements   
	   -- out_data - contains number of users for each antenna for all five definitions of home location for all weeks for antennas  
	   -- user1_out.txt - contains enumeration of all of user 1 specific patterns for first two weeks  
  

src    
	-- AMP_AT.py - current working code to enumerate specific users patterns of movement  
	-- anon_data_AT.py - generates an "anonymized" dataset with timesteps removed   
	-- ant_pairs_AT.py - aggregates movements between antennas for all users   
	-- BC_working - directory dedicated to Bishal's migration code   
	-- dist_between_antennas.py - self evident   
	-- uHome_calc_AT.py - generates five definitions of home location output aggregated by antennas and users  
	-- uHome_calc_functions_AT.py - helper functions to generate home locations    

##### Previous Work
* Home Locations by antenna (SET2) all 24 datasets for all five home defs
* Home Locations by arrondisemont (SET3) all 12 datasets all five home defs
* Aggregate movement between antennas (2-mers) for first dataset
* Visualizations of graphs showing overall movement between antennas
* Distances between each antenna
* Enumeration of specific patterns of movement by antenna for first five users
* Home Locations by user for each month (SET3) all five home defs
* Output well-formatted specific 1-mers to 10-mers for first 80, 800, 8000 users

##### Current Work
* Adam -- Enumerate a single user's abstract pattern of movements   
* Adam -- Alter user home location for daily (365 out-values per user)    
* Adam -- Develop an abstract graph in D3.js using movement patterns  
* Adam -- Clustering similar users/home locations by 2-mers, 3-mers, 4-mers, ... 
* Bishal -- Heat map for aggregate migration between arrondisements by month   
* Bishal -- Visualization for month by month migration by user   
* Matt -- Aggregate patterns by each user (i.e. User 1, Pattern 1, count)   
* Matt -- How active is a user? (Generate summary statistics/histogram on 2-mer AA vs. AB)  
* Matt -- How well-travelled is a user? (Amount of unique 2-mers vs. 3-mers vs. 4-mers ...)  
* Michael -- Interactivity of Senegal with arrondisement boundaries using D3.js    
* Michael -- Plotting antennas in Senegal using D3.js     
* Morgan -- Generate voronoi diagram by antenna locations   
* Morgan -- Abstract out movement (i.e. I don't care where they moved to, just did they move? AA vs. AB) to address   
Time patterns (i.e. average time of movement by user by home location)
* Morgan -- Does definition of home location matter? (statistically significant difference)
* Morgan -- Does time of year matter? (statistically significant difference)

##### Implementation Issues
* Dynamic programming approach to enumeration 
* Best data structure to hold specific/abstract patterns by user  

##### Future Work
* Adam -- Enumerate all users' specific patterns of movements
* Adam -- Enumerate all users' abstract patterns of movements
* Bishal -- Day by day migration by user
* Matt -- Abstract patterns summary statistics/histograms on first 100 users

##### Potential Directions
* Clustering users based on movement patterns and investigate their home location to infer any sociological and cultural phenomena
* Using movement patterns, develop a model that can generate a set of random users (synthetic dataset)
* Using movement patterns, develop a model that can differentiate (i.e classify) a user's country (Senegal vs. Ivory Coast)

