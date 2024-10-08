# Project 2

# Importing packages.
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Loading in csv as data frame. Ask for user input for file path.
file_path = input('Please enter the file path for "cereal.csv":\n')
df = pd.read_csv(file_path)


# Function to compute mean and standard deviation of each column and return both as a list.
def MeanAndStd(col):
    mu = col.mean()   # Mean
    sig = col.std()   # Standard Deviation
    return [mu, sig]


# Quick function to find max cereal.
def MaxCereal(col):
    mx = df[col].max()   # Find the max.
    ind = df.index[df[col] == mx]   # Find its index.
    cereal = df.loc[ind]['name']   # Select cereal.
    return cereal.values[0]   # Get string out of array.


# Making dictionary of means and standard deviations.
msm_dict = {}
# Iterate through columns.
for name in df.columns:
    try:   # Only works if numeric.
        msm_dict[name] = MeanAndStd(df[name])   # Store column's mean and std in corresponding dictionary entry.
    except:   # If non-numeric, skip.
        continue

# Making dictionary of maxes.
max_dict = {}
# Iterate through selected columns.
for col in ['calories', 'protein', 'fat', 'sodium', 'fiber']:
    max_dict[col] = MaxCereal(col)   # Assign maxes.


# Function to format output of MeanAndStd.
def formatMS(ms, colname, i_val=1):   # Output list, then column name used for output.
    output = (str(i_val) + ". " + colname + "\n\tMean: " + str(ms[0]) +
              "\n\tStandard Deviation: " + str(ms[1]))
    return output   # Return compiled string.


# Function to format MaxCereal.
def formatMax(mx, colname, i_val):   # Output, then column name used for output.
    output = str(i_val + 1) + ". Max " + colname + " Cereal: " + mx
    return output   # Return compiled string.


# Creating outputs.
# Setting up values to iterate through.
outMS = ""
cols = ["calories", "protein", "fat",
        "sodium", "fiber", "carbo",
        "sugars", "weight", "cups"]
colnames = ["Calories", "Protein", "Fat",
            "Sodium", "Fiber", "Carbohydrates",
            "Sugars", "Weight per Serving", "Cups per Serving"]

# First set of outputs: Means and Standard Deviations.
for i in range(0, len(cols)):
    outMS = outMS + formatMS(msm_dict[cols[i]], colnames[i], i+1) + "\n\n"

# Second iteration sets.
outMx = ""
c2 = cols[:5]
cn2 = colnames[:5]

# Second set of outputs: Maxes
for i in range(0, len(c2)):
    outMx = outMx + formatMax(max_dict[c2[i]], cn2[i], i) + "\n\n"

# Writing output.
# Input file path to be saved as.
fname = input('Please enter an output path with file type ".txt":\n')

# Open file path.
fout = open(fname, 'w')

# Writing output.
fout.write("Cereal Statistics Report\n\n")
fout.write("I. List of Sample Statistics:\n\n")
fout.write(outMS)
fout.write("II. List of Max Values Cereals:\n\n")
fout.write(outMx)
# Saving output.
fout.close()

# Onto the graphs.
# Calculating unique manufacturers.
# One line. Count occurrences of each category, then sort reverse alphabetically.
mfr_freq = df['mfr'].value_counts().sort_index(ascending=True)

# Big 3x1 plot.
plt.figure(figsize=(7, 15))

# First plot.
plt.subplot(311)

# Manufacturer First Letters.
labels = ["A", "G", "K", "N",
          "P", "Q", "R"]
# Colors.
colors = ["#E5272D", "#234291", "#D31245", "#ffffff",
          "#FFA216", "#182B55", "#292526"]

# Making a horizontal bar plot. y-axis is labels. x is frequencies.
plt.barh(labels, mfr_freq, color=colors, linewidth=0.5, edgecolor='k')

# Applying titles.
plt.title("Number of Cereals By Company")
plt.xlabel("Number of Cereals")
plt.ylabel("Company")

# Second plot.
plt.subplot(312)
# Creates a histogram and stores the count values, # of bins, and object type.
count, bins, oType = plt.hist(df["calories"], 20, density=True, color="r")

# Parameters for distribution curve.
mu, sigma = msm_dict['calories']

# Plotting normal distribution as literally as possible.
plt.plot(bins, 1/(sigma*np.sqrt(2 * np.pi))*np.exp(-(bins-mu)**2/(2*sigma**2)),
         linewidth=3, color='g')
# Not a terribly good fit. Too high std for distribution.

# Adding aesthetics.
plt.title("Distribution of Calories")
plt.xlabel("Quantity of Calories")
plt.ylabel("Frequency of Calorie Quantity")

# Third plot.
plt.subplot(313)

# Get values for our box plot.
sList = []   # Dummy list.
for i in df['mfr'].unique():   # Iterate through manufacturers.
    # Append a Pandas Series containing calories from cereals by each manufacturer to list.
    sList.append(df["calories"][df["mfr"] == i])

# Create the boxplot using slist. matplot automatically makes multiple bp's.
bp = plt.boxplot(sList, labels=df['mfr'].unique(), patch_artist=True)

# Colors for the bar plot.
colors = ["#ffffff", "#182B55", "#D31245", "#292526", "#234291", "#FFA216", "#E5272D"]
# Select each box and color and set that box's color to selected color.
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Aesthetics again.
plt.title("Box Plot of Calories by Manufacturer")
plt.xlabel("Manufacturer (Coded by First Letter)")
plt.ylabel("Calories")

# File path to save graphs on.
plt.savefig(input('Please enter an output path with file type ".png":\n'))
plt.show()
