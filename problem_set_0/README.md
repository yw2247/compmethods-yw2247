# Problem Set 0
**Name:** Yu (Irene) Wang

**NetID:** yw2247        
## Instructions to Run Code
- Python 3.x required  
- Install dependencies:  
  ```bash
  pip install pandas matplotlib sqlite3

### Exercise 1: Clinical Decision Support - Temperature Tester
**1a. Function Implementation**<br> 
See Code Appendix. 

**1b. Identify ambiguity in problem description**
*Are there any aspects of 1a that could be interpreted in more than one way? Discuss.*<br>                   
The problem does not define the units of temperature (i.e. Degrees F vs Degrees C). I assumed both the reference temperature and the tested values are in the same unit. Furthermore, the problem does not specify the type of input. I assumed only numerical values would be given. Also, "within 1 degree" is a bit ambiguious since it could be intepreted as either strictly less than 1 or less than or equal to 1. Here I chose the inclusive threshold (<=1). 

**1c. Testing**<br>
chicken_tester(42): True<br>
human_tester(42): False<br>
chicken_tester(43): False<br>
human_tester(35): False<br>
human_tester(98.6): False<br>

### Exercise 2:  Analyzing COVID-19 Case Data
**2a. Function Implementation**<br> 
See Code Appendix. 

**2b. Visualization of New Cases**<br> 
Below is the daily new cases plot (new cases versus date) for Washington, New York, and Illinois:
![Daily new cases plot](plots/2b_new_cases.png)
*Discuss any limitations of your approach*<br>
The data comes from cumulative totals, so “daily new cases” are just the differences between days. This can create odd results if states revise their numbers (sometimes even negative values). Moreover, some states don’t report every day. They may report weekly or in batches, which shows up as long flat stretches followed by very large spikes. Lastly, the graph uses total counts, so bigger states naturally look larger than smaller ones. It doesn’t adjust for population size, so it's not good for comparisons between states. 

**2c. Find Peak Case Dates**<br> 
*Test this function and provide examples of its use.*<br>
I tested this function on 4 states. Below are their peak dates and peak new case counts:
Washington:  2022-01-18, 63640 new cases
New York:    2022-01-08, 90132 new cases
Illinois:    2022-01-18, 93423 new cases
California:  2022-01-10, 227972 new cases
We can see that most states peaked during early January 2022. Among the 4 tested states, California’s peak was especially high due to its large population. This shows the function correctly identifies the highest daily new case count for each state.

**2d. Compare Peak Cases**<br> 
*Test this function and provide examples of its use.*<br>
Example Results:<br>
| States Compared         | First to Peak | Days Between Peaks |
| ----------------------- | ------------- | ------------------ |
| Washington vs. New York | New York      | 10                 |
| Illinois vs. California | California    | 8                  |
| Washington vs. Illinois | Same Peak     | 0                  |
New York’s peak occurred 10 days before Washington’s. California’s peak occurred 8 days before Illinois’s. Washington and Illinois peaked on the same day. These results show that most states reached their peaks around the same time, but there were small differences in timing between regions. The function is a straightforward way to compare peak dates. It gives a rough idea of how the outbreaks rose in different states.

**2e. Examine individual states**<br> 
*Review the data for Florida and identify any unusual patterns. Hypothesize about what might be happening.*<br>
Below is the daily new cases plot (new cases versus date) for Florida:
![Daily new cases plot for Florida](plots/2e_fl.png)
Two unusual patterns stand out:

1. Negative new case values — I hypothesize that this can appear when Florida revised its cumulative case counts downward.

2. Jump patterns after Nov 2022 — Long stretches of zeros followed by sudden large increases; 25% percentile is 0. 

The zoomed plot below makes this second pattern clearer:
![Daily new cases plot zoom for Florida](plots/2e_fl_tail.png)
I hypothesize that Florida stopped reporting daily during this period and instead updated case counts less frequently (weekly or biweekly). To test this, I measured the gaps between non-zero reporting days:

Count of gaps: 9<br>
Mean gap (days): 14.78<br>
Median gap (days): 14.0<br>
Top gap values:<br>
14    8<br>
21    1<br>
These results support the hypothesis: after November 2022, Florida reported new cases roughly every two weeks, with an occasional three-week gap.

### Exercise 3:  Analyzing Population Data
**3a. Load and Examine Data**<br> 
*What columns are present in the dataset?*<br>
There are 4 columns present in the dataset: "name", "age", "weight", and "eyecolor".

*How many rows (representing individuals) does the dataset contain?*<br>
The dataset contains 152361 rows. 

**3b. Analyze Age Distribution**<br>
*Compute and report the following statistics for the age column: mean, standard deviation, minimum, maximum.*<br>
mean: 39.510528<br>
std: 24.152760<br>
min: 0.000748<br>
max: 99.991547

*Plot a histogram of the age distribution with an appropriate number of bins.*<br>
Below is the histogram of the age distribution with number of bins = 20:
![Histogram of the Age Distribution](plots/3b_age.png)

*Describe the role of the number of bins.*
The number of bins decides how the age range is split into intervals. For example, with ages from 0 to 100 and 20 bins, each bin represents 5 years (0–5, 5–10, …). More bins give more details but can look messy, while fewer bins look simpler but may hide details.

*Comment on any outliers or patterns you observe in the age distribution.*
The age distribution looks fairly even up to around 70, with fewer individuals above 70. There are no impossible ages (e.g., below 0 or above 110), and no clear outliers.

**3c. Analyze Weight Distribution**<br>
*Compute and report the following statistics for the weight column: mean, standard deviation, minimum, maximum.*<br>
mean: 60.884134<br>
std: 18.411824<br>
min: 3.382084<br>
max: 100.435793

*Plot a histogram of the weight distribution with an appropriate number of bins.*<br>
Below is the histogram of the weight distribution with number of bins = 20:
![Histogram of the Weight Distribution](plots/3b_weight.png)

*Describe the role of the number of bins.*<br>
The number of bins decides how the weight range is split into intervals. For example, if weights range from 0 to 100 kg and we use 20 bins, each bin covers 5 kg (0–5, 5–10, …).

*Comment on any outliers or patterns you observe in the age distribution.*<br>
The weight distribution peaks around 65–75 kg and shows a long left tail. Outliers appear at both ends: a few very low weights (<20 kg, minimum about 3.4 kg), likely from children or infants, and some very high weights (around 95–100 kg) that are uncommon. Most individuals are in the adult range, with these low and high values standing out from the rest.

**3d. Explore Relationships**<br>
*Create a scatterplot of weights versus ages.*<br>
![Scatterplot of Weights versus Ages](plots/3e_scatter.png)

*Describe the general relationship between weights and ages as observed from the scatterplot.*<br>
Before about age 20, weight tends to increase with age, showing a clear positive relationship during growth and adolescence. After age 20, weights mostly fall between 50 and 100 kg, with variation depending on the individual, but no strong upward or downward trend with age.

*Identify and name any individual whose data does not follow the general relationship observed.*<br>
Anthony Freeman. 

*Explain your process for identifying this outlier.*<br>
From the scatterplot, I noticed one point that did not follow the general relationship between age and weight: an individual older than 40 with a weight below 30 kg. To confirm, I filtered the dataset with the condition age > 40 and weight < 30, which returned this individual. Such a low weight for an adult is unrealistic compared to the rest of the data, so this person is clearly an outlier.

### Exercise 4: Hospital Data Analysis
