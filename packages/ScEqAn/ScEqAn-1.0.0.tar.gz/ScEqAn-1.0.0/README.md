# ScEqAn (Scientific Equation/Expression Analysis)

- Dynamic Expression Analysis for research on equations and algorithms.
- Used for providing boundary values to any equations to make sure how far the input dependencies have impact on outcomes
- Altering the x, y multiple times to check individual impact of x & y on f(x, y) is the ultimate goal of ScEqAn.
- Check out the example code in repo ( https://github.com/Palani-SN/ScEqAn ) for reference.

**Note:** 
- **Recommended for Educational & Research purposes only,**
- **Not Recommended for Verification & Validation (Testing)**

## Step 1 : Create ScEqAn input scripts in *Input.txt*

```txt
[P] = p{-10.0, 70.0} + r{-50.0, 50.0} * t{0.0, 0.20};
[Q] = q{-20.0, 20.0} + s{-50.0, 50.0} * t;
```
- save the above content to *Input.txt* and use that to create the *Output.log*

### Rules to be followed in writing ScEqAn script

- All Input Variables of any equation should be provided with a range as specified below.

```txt
... = input_variable{lower_bound, upper_bound}
```

- And Output variables should be enclosed within square brackets.

```txt
[output_variable] = ...
```

- Otherwise you can write the equations the same way you would write in a python code.

## Step 2 : Use the following example Code to get reports

### Analysis 
- Sample usage of the file is as given below (Refer Examples for more understanding)

```python
from ScEqAn.Analysis import DynamicProgramAnalysis

OBJ = DynamicProgramAnalysis("InputFiles/Input.txt", "OutputFiles/Output.log");

# For printing the results to console, set Debug = True
OBJ.Run(Debug = True);

# For printing the results to console, set Debug = False
OBJ.Run(Debug = False);
```
#### CodeFlow

![](https://github.com/Palani-SN/ScEqAn/blob/master/AnalysisCodeflow.PNG?raw=true)

#### DynamicProgramAnalysis (class from Analysis.py)

- Initialising class helps to configure the Input txt file to be used and output report needs to be generated with the worst case values.
- Arguments
  - Arg1 - FileName (name of the input file which has ScEqAn script)
  - Arg2 - LogFileName (name of the output file for the reports)
- Sample usage of DynamicProgramAnalysis Initialisation is shown below.

```python
from ScEqAn.Analysis import DynamicProgramAnalysis

OBJ = DynamicProgramAnalysis("Input.txt", "Output.log")
```
#### Run()

- Initiates the Dynamic Program Analysis with the already set Input and Output files as configuration.
- Additionally we can select Debug as True to print the current status of the run to console.

```python
## Definition
def Run(self, Debug = False):
```
- Arguments
  - Arg1 - Debug (If True prints the run info to console, If false doesnt print)

## Step 3 : Check output reports in *Output.log* 

- you will be getting the extreme values of input with respect to output extremes as shown below.

![](https://github.com/Palani-SN/ScEqAn/blob/master/AnalysisOutput.PNG?raw=true)
