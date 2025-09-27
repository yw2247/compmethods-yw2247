# Problem Set 1
**Name:** Yu (Irene) Wang<br>
**NetID:** yw2247        <br>
## Instructions to Run Code
- Python 3.x required  
- Install dependencies:  
  ```bash
  pip install pandas matplotlib sqlite3

### Exercise 1: Efficiently search patient data
**1a. Plot Age Distribution**<br> 
*Plot a histogram showing the distribution of ages.*<br>

<img src="plots/1a_age.png" width="700"/>

*Determine if any patients share the same exact age. Provide evidence for your findings.*<br>
I computed frequency counts for all ages and found no value occurring more than once; therefore, no patients share the same exact age.<br>
Evidence: dup_counts (duplicates-only dictionary) was {}, and len(ages) == len(age_counts), confirming no exact duplicates.

*Extra Credit: Explain how the existence (or non-existence) of multiple patients with the same age affects the solution to the rest of the problem.*<br>
If there are multiple patients with the same age:
- 1b. Gender distribution: No effect. The bar chart of gender counts is unchanged.
- 1c. Sort by age & identify the oldest: After sorting, the oldest age may appear multiple times.
- 1d. Second oldest: We must define what “second oldest” means if ties appear. For example, we can either choose the second record in sorted order (could have the same age as the oldest) or the second-oldest distinct age (the next lower age than the max). The timing will still be O(n) regardless. 
- 1e. Binary search for age = 41.5: Exact age search may return many patients, not just one.
- 1f. Count patients ≥ 41.5: No effect on the method or complexity. The number might change based on duplication. 
- 1g/1h. Count in an age range: totals (and male totals) might be higher if many patients share ages inside the interval. bisect_left(high) - bisect_left(low) still works. Time complexity remains the same.

**1b. Plot Gender Distribution**<br>
*Plot the distribution of genders from the dataset.*<br>

<img src="plots/1b_gender.png" width="700"/>

*Identify how gender is encoded in the data and list the categories used.*<br>
Gender is encoded as a string attribute (gender) on each <patient> element in the XML. There are three categories: female, male, and unknown (counts: female = 165,293; male = 158,992; unknown = 72).

**1c. Sort Patients by Age**<br>
*Sort the patients by age and store the result in a list. Identify the oldest patient.*<br>
The oldest patient is: {'name': 'Monica Caponera', 'age': 84.99855742449432, 'gender': 'female'}.<br>

**1d. Finding the Second Oldest Patient**<br>
*Describe a method to find the second oldest patient in O(n) time. Keep in mind sorting the list is O(n log n).*<br>
We scan the list once while keeping two variables:<br>
- top: the largest age seen so far,
- second: the largest age that is strictly less than top.

Steps:
1. Initialize top = None, second = None.
2. For each patient with age a:<br>
- If top is None or a > top:<br>
set second = top (if top exists), then set top = a.<br>
- Else if second is None or a > second:<br>
set second = a.<br>
3. After the scan:<br>
- If second is None, there are fewer than two distinct ages.
- Otherwise, second is the second-oldest distinct age. 

In this way, every age is compared only against the current best two. If an age beats top, it becomes the new top and the old top slides to second. Otherwise, if it sits between top and second, it updates second. Therefore, the time complexity is: exactly one pass, so O(n).<br>
The second oldest patient is: {'name': 'Raymond Leigh', 'age': 84.9982928781625, 'gender': 'male'}.

*Discuss scenarios where it is advantageous to sort the data versus using the O(n) solution.*<br>
It’s better to sort when we’ll reuse the ordering many times or need operations that depend on order. For example, after one sort (O(n log n)), we can quickly answer many follow-up questions like “who are the top k oldest?” and “how many are between 30 and 50?” using fast lookups (O(1) and O(log n), respectively). Sorting also helps when we need a ranked report or when we need to handle tie consistently. On the other hand, we can use the O(n) solution when we only need a single result like “what is the second oldest distinct age?”, and we don’t need the whole list in order.

**1e. Binary Search for Specific Age**<br>
*Implement a binary search (bisection) on your sorted list to find the patient who is exactly 41.5 years old.*<br>
The patient who is exactly 41.5 years old: {'name': 'John Braswell', 'age': 41.5, 'gender': 'male'}. 

**1f. Count Patients Above a Certain Age**<br>
*Use arithmetic to determine the number of patients who are at least 41.5 years old.*<br>
*Hint: There is a solution that follows almost immediately from the solution to 1e.*<br>
There are 150471 patients who are at least 41.5 years old.<br>

**1g. Function for Age Range Query**<br>
*Write a function that, in O(log n) time, returns the number of patients who are at least low_age years old but strictly less than high_age years old.*<br>
After sorting ages in ascending order, the function uses two binary searches to find the start and end indices of the interval [low_age,high_age). The count is the difference of those indices. Each query is O(log n).

*Test this function thoroughly and provide the test results.*<br>
Partition of the full range (should sum to n = 324357):<br>
[0, 21): 85645<br>
[21, 35): 60091<br>
[35, 50): 64112<br>
[50, 70): 74894<br>
[70, 90): 39615<br>
[90, 100): 0 (This aligns with what we found before: the max age is about 85)<br>
Sum check: The numbers add up to 324357, matching n. <br>

Small ranges:<br>
[41.5, 41.9): 1788<br>
[60, 61): 4211<br>

Boundary and degenerate cases:<br>
Empty interval [41.5, 41.5): 0<br>
Full span [-10^9, 10^9): 324357 (matching n)<br>
Below minimum [-100, 0): 0<br>
Above maximum [200, 300): 0 <br>

Check using 41.5:<br>
[41.4999999, 41.5): 0 (upper bound excluded)<br>
[41.5, 41.5000001): 1 (exactly one at 41.5)<br>

Additional Assertions:<br>
Expanding the interval shouldn't decrease the count: e.g., [40, 50) <= [18, 50); [10, 40) >= [10, 25).<br>
Another assertion for non-overlapping pieces add up to n (324357): [-∞, 41.5) + [41.5, 41.5) + [41.5, ∞) = n.<br>

**1h. Function for Age and Gender Range Query**<br>
*Modify your previous function(s) to also return the number of males in the specified age range, all in O(log n) time after initial data setup.*<br>
*Test this function thoroughly and justify its correctness.*<br>
Partition of the full range (totals and males; totals should sum to n = 324357; males should sum to 158992):<br>
[0, 21): total=85645, males=43648<br>
[21, 35): total=60091, males=29895<br>
[35, 50): total=64112, males=31751<br>
[50, 70): total=74894, males=35768<br>
[70, 90): total=39615, males=17930<br>
[90, 100): total=0, males=0<br>
Sum checks: totals add to 324357 (= n); males add to 158992 (dataset male total).<br>

Small ranges:<br>
[41.5, 41.9): total=1788, males=905<br>
[60, 61): total=4211, males=2060<br>

Boundary and degenerate cases:<br>
Empty interval [41.5, 41.5): total=0, males=0<br>
Full span [-10^9, 10^9): total=324357, males=158992<br>
Below minimum [-100, 0): total=0, males=0<br>
Above maximum [200, 300): total=0, males=0<br>

Check using 41.5:<br>
[41.4999999, 41.5): total=0, males=0 (upper bound excluded)<br>
[41.5, 41.5000001): total=1, males=1 (exactly one at 41.5, we know it's a male)<br>

Additional assertions:<br>
Expanding an interval shouldn't decrease counts (for totals and males): e.g., [40, 50) ≤ [18, 50); [10, 40) ≥ [10, 25).<br>
Another assertion for non-overlapping pieces add up to full span (for totals and males): [-∞, 41.5) + [41.5, 41.5) + [41.5, ∞) = full span.<br>

### Exercise 2: Low-level standards and their implications
**2a. Understanding the function**<br>
*Explain the logic behind this function; i.e., what does it appear that they are trying to do? What's the relationship between tstop, delta_t, and the number of doses administered?*<br>
The function is designed to simulate giving medication at regular intervals. It starts at time t = 0, and as long as the time is less than the total time tstop, it gives a dose and then adds delta_t to the time. Here, delta_t is the gap between doses, tstop is the overall treatment duration, and the number of doses depends on how many gaps of size delta_t fit before reaching tstop.

**2b. A first test case**<br>
*What happens when you call: administer_meds(0.25, 1)?* <br>
The function prints at t = 0, 0.25, 0.5, 0.75, so 4 doses are given as expected.<br>
Full result: <br>
Administering meds at t=0<br>
Administering meds at t=0.25<br>
Administering meds at t=0.5<br>
Administering meds at t=0.75<br>

**2c. A second test case**<br>
*What happens when you call: administer_meds(0.1, 1)*<br>
The function prints lines like t=0.30000000000000004 and it prints an extra time at about t=0.9999999999999999, so we get 11 doses instead of the expected 10.<br>
Full result:<br>
Administering meds at t=0<br>
Administering meds at t=0.1<br>
Administering meds at t=0.2<br>
Administering meds at t=0.30000000000000004<br>
Administering meds at t=0.4<br>
Administering meds at t=0.5<br>
Administering meds at t=0.6<br>
Administering meds at t=0.7<br>
Administering meds at t=0.7999999999999999<br>
Administering meds at t=0.8999999999999999<br>
Administering meds at t=0.9999999999999999<br>

**2d. Interpreting the surprise**<br>
*Discuss your findings. Did you always get the exact times you expected? Did you always get the number of doses you expected?*<br>
No, I didn't get the exact times and number of doses as I expected. The times don’t always print as neat decimals because computers can’t store numbers like 0.3 or 0.9 exactly in binary. Some values (like 0.1 or 0.2) round nicely when printed, but others show up as 0.30000000000000004 or 0.8999999999999999.<br>
This tiny error also makes the loop run too many times. Instead of stopping at exactly t = 1.0, the program ends at t = 0.9999999999999999, which is still less than 1, so it prints one extra dose.

**2e. Clinical implications**<br>
*Comment on the clinical significance (or insignificance) of each “surprise.” Why might even small deviations be important in a medical setting?*<br>
In real devices, even small mistakes can matter a lot. For example, an extra or missed dose could be harmful if the medicine is strong, like insulin or heart drugs. Also, small drifts in timing could make the treatment go out of sync with other equipment or safety checks. That’s why predictable and exact behavior is very important in medical settings.

**2f. A safer implementation**<br>
*Write a revised version of administer_meds that avoids surprises and behaves predictably.*<br>
*Explain what you changed and why it works better.*<br>
I changed the function to use Python’s Decimal type instead of normal floats. This avoids tiny rounding errors, so numbers like 0.3 or 0.9 print exactly as expected. It also stops the loop at the right time, so the number of doses is predictable and consistent.

### Exercise 3: Algorithm Analysis and Performance Measurement
**3a. Hypothesize the Operation**<br>
*Run a few tests on the algorithms and use the results to hypothesize what type of operation each function performs on a list of values. (To be clear, both algorithms create the same output.)*<br>
*Include your test cases and results in your README file to support your hypothesis.*<br>
I tested both alg1 and alg2 on several datasets (generated by data1, data2, data3, and manual examples). From these tests, both algorithms consistently sort the list into ascending order.They produce the same results regardless of input (already sorted, reverse sorted, random, or empty). Therefore, alg1 and alg2 are both sorting (ascending order) algorithms.<br>

| Dataset            | Input                                               | alg1 Output                                         | alg2 Output                                         | Same? |
| ------------------ | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | ----- |
| `data1(5)`         | `[31.0, 31.026, 31.075..., 31.145..., 31.236...]`   | `[31.0, 31.026, 31.075..., 31.145..., 31.236...]`   | `[31.0, 31.026, 31.075..., 31.145..., 31.236...]`   | yes     |
| `data2(10)`        | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`                    | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`                    | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`                    | yes     |
| `data3(10)`        | `[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]`                   | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`                   | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`                   | yes     |
| Manual random list | `[10, 3, 3, 4.1, 0, 7.99, 100, 2, 0, 1, -1, -0.01]` | `[-1, -0.01, 0, 0, 1, 2, 3, 3, 4.1, 7.99, 10, 100]` | `[-1, -0.01, 0, 0, 1, 2, 3, 3, 4.1, 7.99, 10, 100]` | yes     |
| Empty list         | `[]`                                                | `[]`                                                | `[]`                                                | yes     |

**3b. Explain the algorithms**<br>
*Provide an intuitive, high-level explanation of how alg1 works. Describe the overall approach without going into line-by-line detail.*<br>
alg1 (Bubble Sort):<br>
This algorithm goes through the list from left to right repeatedly and swaps neighbors if they are in the wrong order. After each pass, the biggest value moves to the end of the list, like a bubble rising to the top. The improvement here is the early exit check. If a whole pass finishes without any swaps, the algorithm stops right away because the list is already sorted. This makes it quick on sorted or nearly sorted lists (about O(n) time), but on average or in the worst case it still takes O(n²), which is slow for large and messy lists.

alg2 (Merge Sort):<br>
This algorithm sorts by dividing the list into smaller parts, sorting those parts, and then merging them back together. The list is split in half again and again until only single elements remain. Then the halves are merged: at each step, the smaller front element is picked and added to the new list. Because of this structured process, the algorithm always runs in about O(n log n) time, no matter how the input looks, which makes it reliable and efficient for large lists.

**3c. Performance Measurement and Analysis**<br>
*Time the performance of alg1 and alg2 using time.perf_counter for various sizes of data n. Use the data1 function to generate the data.*<br>
Times are generated using data1 with sizes = [1, 3, 13, 51, 193, 719, 2682, 10000] respectively.<br>
Example times of alg1 on data1:<br>
[3.7497375160455704e-07,<br>
 5.00003807246685e-07,<br>
 8.330098353326321e-07,<br>
 0.0001105829724110663,<br>
 0.0013671659980900586,<br>
 0.04737920896150172,<br>
 0.7581884160172194,<br>
 10.548196875024587] <br>

 Example times of alg2 on data1:<br>
 [2.92027834802866e-07,<br>
 3.167020622640848e-06,<br>
 2.158299321308732e-05,<br>
 6.679102079942822e-05,<br>
 0.00027304200921207666,<br>
 0.0012139170430600643,<br>
 0.004626166948582977,<br>
 0.02261916600400582]<br>

*Plot the performance on a log-log graph as a function of n. Describe the apparent big-O scaling of each algorithm.*<br>
log-log graph for alg1 on d1:

<img src="plots/3c_a1_d1.png" width="700"/>

log-log graph for alg2 on d1:

<img src="plots/3c_a2_d1.png" width="700"/>

Comparison of performance for alg1 and alg2 on d1:

<img src="plots/3c_compare_d1.png" width="700"/>

Apparent big-O scaling of each algorithm on d1:
alg1 (bubble sort): Runtime grows approximately O(n^2) on data1. We can see that the log–log curve is steep and close to a slope of ~2.
alg2 (merge sort): Runtime grows approximately O(nlogn) regardless of input order. We can see that the log–log curve is much shallower than n^2, which is consistent with nlogn.

*Repeat the timing and plotting process using the data2 function to generate data.*<br>
Comparison of performance for alg1 and alg2 on d2:

<img src="plots/3c_compare_d2.png" width="700"/>

*Repeat the timing and plotting process using the data3 function to generate data.*<br>
Comparison of performance for alg1 and alg2 on d3:

<img src="plots/3c_compare_d3.png" width="700"/>

**3d. Conclusions and recommendations**<br>
*Discuss how the performance scales across the three data sets.*<br>
data1 (random floats):<br>
alg1: grows ≈ O(n²).<br>
alg2: grows ≈ O(n log n).<br>
So alg2 is much faster as n increases.<br>

data2 (sorted ascending):<br>
alg1: ≈ O(n) (no swaps needed; stops after one pass).<br>
alg2: ≈ O(n log n) (splits/merges regardless of order).<br>
For small or medium sized lists, alg1 can be as fast as (or faster than) alg2. For large lists, alg2 is the safer choice.<br>

data3 (sorted descending):<br>
alg1: near worst-case O(n²) (many passes and swaps).<br>
alg2: ≈ O(n log n) (splits/merges regardless of order).<br>
alg2 strongly dominates.<br>

*Recommend which algorithm would be preferable for different types of data and justify your recommendation based on your findings.*<br>
Most cases/ large lists/ unknown order: use alg2 (merge sort). It stays fast and reliable (about O(nlogn)) no matter how the data looks.<br>
Already or nearly sorted, and the list isn’t big: alg1 (bubble sort with early exit) is fine and can be faster because it may finish after one pass (about o(n)).<br>
Reverse-sorted or bad order: avoid alg1 (it can be O(n^2) and very slow). Use alg2 instead.<br>
If we want safe performance without guessing about the data: Use alg2. It stays consistent and reliable all the time.<br>
Thereofore, pick merge sort by default, especially for big or messy data; use bubble sort with early exit only for small lists that are already or almost sorted.<br>

### Exercise 4: Implementing and Analyzing a Binary Search Tree as a tool for organizing data
**4a. Implement the add Method** <br>
*Extend the given Tree class to create a binary search tree. Implement the add method to insert a value and associated data (e.g., patient ID and patient information) into the tree according to the rules for a binary search tree.*<br>
my_tree is constructed successfully using the add method.

**4b. Implement a __contains__ Method**<br>
*Test this functionality. (Include your tests in the readme. In your tests, be sure to use in not __contains__.)*<br>
Positive tests:<br>
print(24601 in my_tree)   # True<br>
print(42 in my_tree)      # True<br>
print(8675309 in my_tree) # True<br>
print(7 in my_tree)       # True<br>
print(143 in my_tree)     # True<br>

Negative tests:<br>
print(1492 in my_tree)    # False<br>
print(1 in my_tree)       # False<br>
print(2333 in my_tree)    # False<br>

Empty tree test:<br>
empty = Tree()<br>
print(0 in empty)         # False<br>

Keys that were inserted (24601, 42, 7, 8675309, 143) return True.<br>
Keys not present (1492, 1, 2333) return False.<br>
An empty tree correctly reports False for any key.<br>

**4c. Implement and Test a has_data Method**<br>
*Test your method and provide evidence that it works.*<br>
Positive tests:<br>
has_data('JV'): True<br>
has_data('DA'): True<br>
has_data('JB'): True<br>
has_data('FR'): True<br>
has_data('JNY'): True<br>

Negative tests:<br>
has_data('ABC'): False<br>
has_data(24601): False<br>

Empty tree test:<br>
empty.has_data('BALABALA') -> False<br>

Data that was inserted ('JV', 'DA', 'JB', 'FR', 'JNY') returns True.<br>
Data not present ('ABC') returns False. 24601 was intended to be a key, not a data, so it returns False. <br>
An empty tree correctly reports False for any data.<br>

**4d. Performance Analysis of __contains__ and has_data**<br>
*Timing the __contains__ Method: Populate the tree with random patient IDs and associated data of various sizes n. Measure the time taken for multiple in operations (after the tree has been constructed). Plot these timings on a log-log graph. The graph should show that the time required for checking if a number is in the tree approaches O(logn) for sufficiently large n.*<br>


*Timing the has_data Method. Discuss how the performance of both methods compares.*<br>


*Setup Time Analysis: Measure and plot the time to construct the tree for various sizes. The runtime should be between curves representing O(n) and O(n^2).*<br>

**4e. Discussing Choice of Test Data**<br>
*Explain why it is unrepresentative to always use a specific value (e.g., patient_id = 1) as test data or to only use one test point for performance analysis. Discuss the implications of choosing appropriate test data for accurately assessing performance.*<br>
Always using the same value (e.g., patient_id = 1) or only one test point gives a biased view of performance. The time to search in a binary search tree depends on how deep the value is in the tree and whether it is found or not. A single fixed value may be very fast or very slow, but it does not reflect the average case. Also, one measurement cannot show how runtime changes as the tree grows. To assess performance fairly, we need many test values (both present and absent) across different tree sizes. This provides a more accurate picture of average behavior and allows us to see whether the results match the expected growth rates (log n for key search and linear for data search).

### Exercise 5: Choosing ontologies for clinical research data
**5a. Recommended ontology set**<br>
1. SNOMED CT (SCTID) — for clinician notes and imaging reports (findings, anatomy, procedures)<br>
- Gap it fills: Gives a single, standard way to label problems, symptoms, body sites, and procedures, which is something the drug and genomics vocabularies don’t cover.<br>
- How complete/specific: Very large and detailed; good for turning free text in notes and radiology/pathology reports into consistent, searchable terms.<br>
- Why it helps across data types: The same anatomy/findings terms work in both notes and imaging narratives, so searches line up across sources.<br>

2. RxNorm (RXNORM) - for medication records and drug mentions in notes<br>
- Gap it fills: Provides normalized IDs for clinical drugs at the level people actually order (ingredient + strength + dose form).<br>
- How complete/specific: Highly specific to real products and updated frequently, which helps merge different spellings or brand/generic names.<br>
- Why it helps across data types: Connects structured med lists with drug mentions in notes so medication queries are consistent everywhere.<br>

3. NCI Thesaurus (NCIt) - for oncology concepts in notes, imaging/pathology, and biomarkers<br>
- Gap it fills: Adds cancer-specific detail (histology, staging, biomarkers, therapies) that general clinical vocabularies don’t cover well.<br>
- How complete/specific: Broad, research-grade coverage with clear terms and synonyms, which is well suited to a cancer hospital.<br>
- Why it helps across data types: The same NCIt IDs can tag pathology diagnoses, radiology impressions, staging in notes, and biomarker results, keeping cancer terms aligned.<br>

4. Sequence Ontology (SO) - for gene sequence metadata<br>
- Gap it fills: Standard names for genomic features and variant consequences (e.g., exon, missense_variant) that clinical/drug ontologies lack.<br>
- How complete/specific: Widely used in genomics; specific enough to filter by variant type instead of only searching text.<br>
- Why it helps across data types: Lets molecular results link cleanly to cancer concepts (e.g., variants related to certain tumor types or biomarkers).<br>

5. RadLex (RADLEX) - for imaging concepts and protocol names (radiology)<br>
- Gap it fills: Gives standard, easy-to-read names for radiology exams and sequences (e.g., “CT pulmonary angiography”). This fixes messy, inconsistent local protocol names.
- How complete/specific: Radiology-focused and well-maintained by RSNA; widely used for protocol naming and search. It also links to the RSNA/LOINC Playbook.
- Why it helps across data types: Pairs nicely with SCTID/NCIt. You can search findings/diagnoses (SNOMED/NCIt) together with standardized exam/protocol names (RadLex).

This keeps the set small but covers everything we need: genes, meds, clinical text, and imaging contents.<br>

**5b. Licensing and alternatives**<br>
1) SNOMED CT (SCTID)
- License / access: It's free to use in the United States through a UMLS account, which requires accepting the UMLS license terms. Outside the U.S., use follows SNOMED International’s country/affiliate rules.
- Alternative: MONDO Disease Ontology (CC BY 4.0) (free to use worldwide; strong for disease normalization across sources). 
- Why the alternative is acceptable: MONDO is open, actively maintained, and works well for normalizing disease names in research.
- Why the preferred choice is still better: It covers not only diseases but also findings, symptoms, anatomy, and procedures. It is deeper and more flexible for coding free-text notes and imaging findings.
- Discovery/maintenance trade-offs: SNOMED CT has strong vendor support, frequent updates via UMLS, and many existing mappings, which makes search and integration easier.

2) RxNorm (RXNORM)
- License / access: RxNorm is distributed by the U.S. National Library of Medicine. It is free to use with a UMLS account and license acceptance.
- Alternative: WHO ATC/DDD (good open option for drug classes and utilization studies).
- Why the alternative is acceptable: ATC/DDD is well-known internationally and useful for class-level analysis.
- Why the preferred choice is still better: RxNorm represents clinical drugs at the level clinicians order and dispense (ingredient + strength + dose form). This is important for reconciling EHR orders, pharmacy data, and drug mentions in notes.
- Discovery/maintenance trade-offs: RxNorm has regular monthly and weekly updates and mature APIs/browsers, which supports reliable data integration.

3) NCI Thesaurus (NCIt)
- License / access: NCIt is open and released under CC BY 4.0, which allows reuse with attribution.
- Discovery/maintenance trade-offs: NCIt is actively curated by the NCI, with stable releases, web browsers, and APIs, which makes it easy to discover and maintain terms.

4) Sequence Ontology (SO)
- License / access: SO is open and released under CC BY 4.0, which allows reuse with attribution.
- Discovery/maintenance trade-offs: SO is part of the OBO community, has active maintainers, and is widely used in bioinformatics pipelines, which helps with long-term usability.

5) RadLex (RADLEX)
- License / access: RadLex is free to use (worldwide, commercial and non-commercial). We just need to accept the RSNA RadLex license. There is no fee.
- Alternative: DICOM Controlled Terminology (PS3.16). It’s part of the DICOM standard and is free to read and implement.
- Why the alternative is acceptable: DICOM gives exact, machine-level codes for how the scan was done. It’s great if we mainly need technical parameters for filtering and reproducibility.
- Why the preferred choice is still better: It's better if we want clear, human-friendly names for exams and protocols. RadLex is designed for clinicians, uses easy-to-read labels, and links to the RSNA/LOINC Playbook, which makes search, protocol naming, and QA dashboards easier.
- Discovery/maintenance trade-offs: RADLEX is maintained by RSNA, updated regularly, widely used in radiology. It's easy to browse and download.

**5c. Search methodology and stopping rule**<br>
Search methodology: <br>

1) Start with realistic text, then run a recommender.<br>
I submitted short sentences that look like our data to NCBO BioPortal Ontology Recommender.<br>
Example texts: “CT chest with contrast shows a 12 mm ground-glass nodule; pathology report: lung adenocarcinoma, PD-L1 positive; NGS found EGFR exon 19 deletion; patient started osimertinib.”<br>

2) Check official catalogs/pages.<br>
I confirmed scope, updates, and licenses in OBO Foundry (SO), NCBO BioPortal, and steward sites: NLM/UMLS (SNOMED CT, RxNorm), NCI EVS (NCIt), and RSNA RadLex pages (for RadLex and Playbook/LOINC-RSNA links).<br>

3) Quick coverage check.
Molecular/variants: Sequence Ontology (SO)<br>
Clinical/notes (+ imaging findings): SNOMED CT<br>
Medications: RxNorm<br>
Cancer terms across sources: NCIt<br>
Imaging concepts & protocol naming (radiology): RadLex<br>

4) Quick manual check.
I mapped a few real phrases:<br>
“Ground-glass opacity” → SNOMED CT<br>
“Lung adenocarcinoma / PD-L1” → NCIt<br>
“Osimertinib” → RxNorm<br>
“Missense_variant” → SO<br>
“CT pulmonary angiography / MR T2 FLAIR” (exam/protocol names) → RadLex<br>
These checks showed each ontology covers a distinct need with little overlap.<br>

Stopping rules:<br>

- Rule 1: One primary per data type.<br>
SO (molecular), SNOMED CT (clinical/notes + imaging findings), RxNorm (meds), RadLex (radiology imaging concepts/protocol names).<br>

- Rule 2: One cross-cutting cancer layer.<br>
Add NCIt for histology, staging, and biomarkers that appear in notes, imaging, and molecular results.<br>

- Rule 3: No duplication.<br>
Do not include two ontologies for the same slice (e.g., a second drug ontology).<br>

- Rule 4: Handle heavy overlap by picking one.<br>
If two options overlap a lot on the same concept set (>~40%), keep the one with better mapping for hospital use.<br>

- Rule 5: Must be practical to maintain.<br>
Each ontology must have stable releases and easy access (UMLS/EVS/OBO/RSNA downloads and APIs).<br>