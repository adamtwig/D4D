### Adam - Abstract Patterns   
##### Motivating Question     
* How do people move on a small scale (by the second/minute/hour)?    

##### Main Tasks   
* Enumerate a single user's abstract pattern of movements
* Break AMP into decision tree counts/percents
* Alter user home location for daily (365 out-values per user)
* Develop an abstract graph in D3.js using movement patterns
* Clustering similar users/home locations by 2-mers, 3-mers, 4-mers, ...

### Bishal - Migration  
##### Motivating Question  
* How do people move on a large scale (daily, weekly, monthly)?

##### Main Tasks
* Heat map for aggregate migration between arrondisements by month
* Visualization for month by month migration by user
* Calculate mean/variability of migrations between arr pairs aggregated by month
* Gives rise to event detection, as any migration that was >3 s.d's away would be meaningful

##### Open-ended Task
* Does the definition of home location matter for migration?
  * What measures/variables to use to find a
	statistically significant difference?

### Matt - Time
##### Motivating Question  
* How does time affect how people move?

##### Intro Task
* Aggregate patterns by each user (i.e. User 1, Pattern 1, count)   

##### Main Tasks  
* How mobile/static is a user? 
  * Generate summary statistics/histogram on 2-mer AA vs. AB
  * Group by home location  
* How often does a user move?  
  * Average time of movement by user by home location  
* What time of day is the most active for movement?
  * How long will a user stay at a location at 9 am, noon, 9 pm?

##### Open-ended Task
* Does time of year matter for abstract patterns?
  * What measures/variables to use to find a
	statistically significant difference?

### Michael - Interactive Visualization     
##### Motivating Question   
* What is the best way to visualize movement over time?   

##### Main Tasks   
* Interactivity of Senegal with arrondisement boundaries using D3.js   
* Plotting antennas in Senegal using D3.js
* Plotting a decision tree using D3.js

### Morgan - Location
##### Motivating Question  
* How does geography affect how people move?

##### Intro Task   
* Generate voronoi diagram by antenna locations  

##### Main Tasks   
* How well-travelled is a user?
  * Average distance travelled between calls
  * Amount of miles travelled each day/week/month
* How diverse of a traveller is a user?  
  * Amount of unique 2-mers vs. 3-mers vs. 4-mers ...
* Can we make any inference to forms of travel/transportation?
  * Looking at the distances between antennas 
  * ex. Teleporter: Makes call at ant 1, next call is 100 miles away at ant 2 
  * How did the user get there? Plane/train/horse/elephant/Superman?   
  * Something to watch out for: Did the user lose service?   

##### Open-ended Task   
* Does definition of home location matter for abstract patterns?  
  * What measures/variables to use to find a
	statistically significant difference?  

