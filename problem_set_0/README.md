# Problem Set 0
**Name:** Yu (Irene) Wang<br>       
**NetID:** yw2247<br>           
## Instructions to Run Code
- Python 3.x required  
- Install dependencies:  
  ```bash
  pip install pandas matplotlib sqlite3

### Exercise 1: Clinical Decision Support - Temperature Tester
**1a. Function Implementation**
**1b. Identify ambiguity in problem description**
- Are there any aspects of 1a that could be interpreted in more than one way? Discuss.<br>                   
Answer: The problem does not define the units of temperature (i.e. Degrees F vs Degrees C). I assumed both the reference temperature and the tested values are in the same unit. Furthermore, the problem does not specify the type of input. I assumed only numerical values would be given. Also, "within 1 degree" is a bit ambiguious since it could be intepreted as either strictly less than 1 or less than or equal to 1. Here I chose the inclusive threshold (<=1). 

**1c. Testing**
chicken_tester(42): True<br>
human_tester(42): False<br>
chicken_tester(43): False<br>
human_tester(35): False<br>
human_tester(98.6): False<br>



