#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.

# # Analysis

# In[388]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files

mouse_metadata_path = "C:/Users/evanm/OneDrive/Desktop/Starter_Code/Pymaceuticals/data/Mouse_metadata.csv"
study_results_path = "C:/Users/evanm/OneDrive/Desktop/Starter_Code/Pymaceuticals/data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame

mouse_study_results = pd.merge(mouse_metadata, study_results, how="left", on=["Mouse ID", "Mouse ID"])


# In[389]:


# Display the data table for preview
#print(mouse_study_results)

mouse_study_results.head(10)


# In[390]:


# Checking the number of mice.
#mouse_study_results["Mouse ID"].value_counts()


#Reminder since I had to look this up again: Nunique() - function return number of unique elements in the object.
#https://www.geeksforgeeks.org/python-pandas-index-nunique/

mouse_study_results["Mouse ID"].nunique()


# In[391]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 

#.loc - allows the return of specified rows and/or columns from that DataFrame
# Duplicated -returns a Series with True and False values that describe which rows in the DataFrame are duplicated and which are not
# Saw Joseph show this to Meredith on 7/31/23

DupMiceIds = mouse_study_results.loc[mouse_study_results.duplicated(subset=["Mouse ID", "Timepoint"]), "Mouse ID"].unique()
DupMiceIds


# In[392]:


# Optional: Get all the data for the duplicate mouse ID. 

# Reminder: Set_index - is used to set a List, Series or Data frame as index of a Data Frame
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html

allDup_df = mouse_study_results.set_index("Mouse ID")
allDup_df.loc["g989"]


# In[393]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.

# Had to look this up but remember from class - a type of command that helps you manage lists by explicitly deleting an element 

remove_Dup = allDup_df.drop(["g989"])
remove_Dup


# In[394]:


# Checking the number of mice in the clean DataFrame.


# Had to look this up but remember from class - method is used to reset the index of a DataFrame. It sets a list of integers ranging from 0 to the length of data as an index

clear_df = remove_Dup.reset_index()
clear_df["Mouse ID"].nunique()


# # Summary Statistics

# In[395]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 

# mean, median, variance, standard deviation, and SEM of the tumor volume. 

summary_st = mouse_study_results.groupby("Drug Regimen")

#Summary Statistical Methods
tumr_vol_mean = summary_st["Tumor Volume (mm3)"].mean()
tumr_vol_median = summary_st["Tumor Volume (mm3)"].median()
tumr_vol_var = summary_st["Tumor Volume (mm3)"].var()
tumr_vol_stndddev = summary_st["Tumor Volume (mm3)"].std()
tumr_vol_SEM = summary_st["Tumor Volume (mm3)"].sem()


# Assemble the resulting series into a single summary DataFrame.
summary_st = pd.DataFrame({
    
    "Mean": tumr_vol_mean, 
    "Median": tumr_vol_median,
    "Variance": tumr_vol_var, 
    "Standard Deviation": tumr_vol_stndddev, 
    "SEM": tumr_vol_SEM     })

#print(tumr_vol_stndddev)
#print(tumr_vol_SEM)
# Let this be a reminder to add paraentheses to the end of variables you want to call (EX:.std() & .sem()) (40 minutes just poof)
summary_st.head(10)


# In[396]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)

# Using the aggregation method, produce the same summary statistics in a single line

# Aggregation: groups the data by 'Id' value, selects the desired features, and aggregates each group by computing the 'mean' of each group
# https://stackoverflow.com/questions/53943319/what-are-all-pandas-agg-functions
# Find lecture when we covered this and rewatch


aggregation_st =  mouse_study_results.groupby(["Drug Regimen"])[["Tumor Volume (mm3)"]].agg(["mean", "median", "var", "std", "sem"])
aggregation_st


# In[397]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.

tested_mice  = clear_df["Drug Regimen"].value_counts()


# Module 5.2 notes

tested_mice.plot(kind = "bar", figsize = (10,5)) 
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.title("Mouse ID/Timepoints for each Drug Regimen using Pandas")
plt.show()


# In[398]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.

# Ascending = a parameter used to sort data in descending order (i.e., from highest to lowest)

tested_mice2 = tested_mice.sort_values(ascending = False) 
plt.bar(tested_mice2 .index, tested_mice2 .values)
plt.xlabel("Drug Regimen") 
plt.ylabel("# of Observed Mouse Timepoints", size = 10) 
plt.title("Mouse ID/Timepoints for each Drug Regimen using Pyplot")
plt.xticks (rotation = "vertical") 
plt.show()


# In[399]:


# Generate a pie plot showing the distribution of female versus male mice using Pandas

# Autopct: enables you to display the percent value using Python string formatting
#https://stackoverflow.com/questions/44076203/getting-percentages-in-legend-from-pie-matplotlib-pie-chart

sex_plot = clear_df["Sex"].value_counts()

sex_plot.plot(kind = "pie", autopct = "%1.1f%%") 
plt.title("Female V.S. Male Mice using Pandas")
plt.show()


# In[400]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot

sex_plot2 = clear_df["Sex"].value_counts()

# Startangle: parameter in Matplotlib’s pie() function is used to rotate the start of the pie chart by angle degrees counterclockwise from the x-axis12.
#startangle=360


plt.pie(sex_plot2, autopct="%1.1f%%",  labels = sex_plot2.index.values) 
plt.title("Female V.S. Male Mice using Pyplot")
plt.show()


# ## Quartiles, Outliers and Boxplts

# In[408]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin

# Start by getting the last (greatest) timepoint for each mouse

last_timepoint = clear_df.groupby(["Mouse ID"]).max()
last_greatest_timepoint_df = last_timepoint.reset_index()


# For that .\ merge
#https://stackoverflow.com/questions/53645882/pandas-merging-101#:~:text=If%20your%20index%20is%20named%2C%20then,%28or%20left_on%20and%20right_on%20as%20necessary%29.&text=If%20your%20index%20is,and%20right_on%20as%20necessary%29.&text=index%20is%20named%2C%20then,%28or%20left_on%20and%20right_on


merged_df = last_greatest_timepoint_df[['Mouse ID','Timepoint']].\
    merge(clear_df,on=['Mouse ID','Timepoint'],how="left")

merged_df


# In[402]:


# Put treatments into a list for for loop (and later for plot labels)

# I did put treatments in a list, but couldn't figure out to a way to make a for loop with this data that didn't result in errors
treatments = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]

# Create empty list to fill with tumor vol data (for plotting)

tumr_vol_data = []

# Locate the rows which contain mice on each drug and get the tumor volumes
# Figured out a diffferent way to look for the outliers
#https://www.geeksforgeeks.org/detect-and-remove-the-outliers-using-python/
def outliers(drugs):
    tumr_vol_data = merged_df.loc[merged_df["Drug Regimen"] == drugs]['Tumor Volume (mm3)']
    
# Calculate the IQR and quantitatively determine if there are any potential outliers.


# Module 5.3 notes
# https://stats.stackexchange.com/questions/156778/percentile-vs-quantile-vs-quartile

    quartiles = tumr_vol_data.quantile([.25,.5,.75])
    quart_first = quartiles[0.25]
    quart_last = quartiles[0.75]
    iqr = quart_last - quart_first
    lower_bound = quart_first - (1.5 * iqr)
    upper_bound = quart_last + (1.5 * iqr)
    

# Determining outliers using upper and lower bounds
# |: represents OR logic
# https://www.geeksforgeeks.org/detect-and-remove-the-outliers-using-python/
# Return: Return will exit the definition at the exact point that it is called, passing the variable after it directly out of the definition. Break will only cause the end of a loop that it is situated in.
   
    outliers = tumr_vol_data.loc[(tumr_vol_data < lower_bound) | (tumr_vol_data > upper_bound)]
    print(f"{drugs}'s potential outliers: {outliers}")
    return tumr_vol_data
    
    
# add subset    
# Is this what they mean by subset?

Capomulin = outliers("Capomulin")
Ramicane = outliers("Ramicane")
Infubinol = outliers("Infubinol")
Ceftamin = outliers("Ceftamin")
    


# In[403]:


# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.
# https://matplotlib.org/stable/gallery/statistics/boxplot_demo.html
# Found this for coloring in  the dot - https://matplotlib.org/stable/gallery/statistics/boxplot.html
# Check 5.3 notes

fig1, ax1 = plt.subplots()
ax1.boxplot([Capomulin, Ramicane, Infubinol, Ceftamin], labels = ["Capomulin","Ramicane","Infubinol","Ceftamin"], flierprops = red_point)
plt.ylabel("Final Tumor Volume (mm3)")
plt.title("Distrubution of the Tumor Volume for each Treatment Group")
plt.show()


# ## Line and Scatter Plots

# In[404]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
# Module 5.2 notes

capo_mouse = clear_df.loc[clear_df["Drug Regimen"] == "Capomulin"]

# Can't believe search for 1509 worked

mouseline_df = capo_mouse.loc[capo_mouse["Mouse ID"] == "l509",:]



fig2, ax2 = plt.subplots()
axis1 = mouseline_df["Timepoint"]
axis2 = mouseline_df["Tumor Volume (mm3)"]
ax2.plot(axis1, axis2 )
plt.xlabel("Timepoint (days)")
plt.ylabel("Tumor Volume (mm3)")
plt.title("Capomulin treatmeant of mouse l509")
plt.show()


# In[405]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen
# Module 5.3 notes

fig3, ax3 = plt.subplots()
avg_tumr_vol = capo_mouse.groupby(["Mouse ID"]).mean()

ax3.scatter(avg_tumr_vol["Weight (g)"],avg_tumr_vol["Tumor Volume (mm3)"])
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")
plt.title("Mouse weight vs. the Average observed Tumor Volume for the entire Capomulin regimen")
plt.show()


# ## Correlation and Regression

# In[406]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen
# Check notes for 5.1-5.3

# (I thought we talked about this before) st.pearsonr - Pearson correlation coefficient measures the linear relationship
# between two datasets. Strictly speaking, Pearson's correlation requires
# that each dataset be normally distributed. Like other correlation
# coefficients, this one varies between -1 and +1 with 0 implying no
# correlation. Correlations of -1 or +1 imply an exact linear
# relationship. Positive correlations imply that as x increases, so does
# y. Negative correlations imply that as x increases, y decreases
#https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python

# round - takes two numeric arguments, n and ndigits, and returns the number n rounded to ndigits
#https://realpython.com/python-rounding/
    
# st.linregress - calculate the parameters that establish a linear relationship between two sets of variables using the least-squares method.
#https://www.delftstack.com/api/scipy/scipy-scipy.stats.linregress-method/#:~:text=Python%20Scipy%20scipy.stats.linregress%20method%20is%20used%20to%20calculate,two%20sets%20of%20variables%20using%20the%20least-squares%20method.

correlation_coefficient = st.pearsonr(avg_tumr_vol['Weight (g)'],avg_tumr_vol['Tumor Volume (mm3)'])
print(f"The correlation between mouse weight and the average tumor volume is {round(correlation_coefficient[0],2)}")


(slope, intercept, rvalue, pvalue, stderr) = st.linregress(avg_tumr_vol["Weight (g)"],avg_tumr_vol["Tumor Volume (mm3)"])
regress_values = avg_tumr_vol["Weight (g)"]* slope + intercept



fig4, ax4 = plt.subplots()
ax4.scatter(avg_tumr_vol["Weight (g)"],avg_tumr_vol["Tumor Volume (mm3)"])
plt.plot(avg_tumr_vol["Weight (g)"], regress_values, color='red')
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")
plt.title("Weight and average observed Tumor Volume for the entire Capomulin regimen")
#plt.annotate()
plt.show()






