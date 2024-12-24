#!/usr/bin/env python
# coding: utf-8

# ### 1. Install Required Libraries

# !pip install pandas numpy matplotlib seaborn xlwt
# 

# ### 2. Specify File Path

# In[4]:


file_path = r"C:\Assignment\Data Analyst Intern Assignment - Excel.xlsx"


# ### 3. Load Datasets

# In[7]:


import pandas as pd
user_details = pd.read_excel(file_path, sheet_name='UserDetails.csv')
cooking_sessions = pd.read_excel(file_path, sheet_name='CookingSessions.csv')
order_details = pd.read_excel(file_path, sheet_name='OrderDetails.csv')


# ### 4. Preview User Details Dataset

# In[8]:


user_details.head(20)


# ### 5. Check for Missing Values in All Datasets

# In[10]:


print(user_details.isnull().sum())
print(cooking_sessions.isnull().sum())
print(order_details.isnull().sum())


# ### 6. Handle Missing Values

# In[11]:


# Example: Fill missing values in Age with the average age
order_details['Rating'].fillna(order_details['Rating'].mean(), inplace=True)


# ### 7. Merge Cooking Sessions with User Details

# In[12]:


merged_data_1 = pd.merge(cooking_sessions, user_details, on='User ID', how='left')


# ### 8. Merge All Datasets

# In[13]:


final_data = pd.merge(merged_data_1, order_details, on='Session ID', how='left')


# ### 9. Identify and Drop Duplicate Columns

# In[14]:


# Check for duplicate columns by comparing the content
for col1 in final_data.columns:
    for col2 in final_data.columns:
        if col1 != col2 and final_data[col1].equals(final_data[col2]):
            print(f"Duplicate column found: {col1} and {col2}")

# Drop duplicate columns
# Example: If 'User ID_y' is identical to 'User ID_x', drop 'User ID_y'
final_data = final_data.drop(columns=['User ID_x'], errors='ignore')
final_data = final_data.drop(columns=['Dish Name_x'], errors='ignore')
final_data = final_data.drop(columns=['Meal Type_x'], errors='ignore')


# Verify the updated columns
print(final_data.columns)


# ### 10. Rename Columns for Consistency

# In[15]:


final_data = final_data.rename(columns={ 
    'Dish Name_y': 'Dish_Name',   
    'Meal Type_y': 'Meal_Type',              
    'User ID_y': 'User_ID'    
})
print(final_data.columns)


# ### 11. Check for Missing Values in Merged Dataset

# In[16]:


print(final_data.isnull().sum())


# ### 12. Data Cleaning and Preprocessing

# In[17]:


final_data['Registration Date'] = pd.to_datetime(final_data['Registration Date'], errors='coerce')
final_data['Order Date'] = pd.to_datetime(final_data['Order Date'], errors='coerce')
final_data['Session Start'] = pd.to_datetime(final_data['Session Start'], errors='coerce')
final_data['Session End'] = pd.to_datetime(final_data['Session End'], errors='coerce')


# In[18]:


final_data['Age'] = pd.to_numeric(final_data['Age'], errors='coerce')
final_data['Duration (mins)'] = pd.to_numeric(final_data['Duration (mins)'], errors='coerce')


# In[19]:


final_data['Session_Date'] = pd.to_datetime(final_data['Session Start'], errors='coerce').dt.date
final_data['Order_Date'] = pd.to_datetime(final_data['Order Date'], errors='coerce').dt.date


# ### 13. Save Merged Dataset

# In[20]:


final_data.to_excel(r"C:\Assignment\Merged_Dataset.xlsx", index=False)
print("Merged dataset saved successfully!")


# ### 14. Load Merged Dataset

# In[21]:


file_path = r"C:\Assignment\Merged_Dataset.xlsx"
Merged_Dataset = pd.read_excel(file_path)


# In[23]:


Merged_Dataset.head(10)


# ### 15. Popular Dishes Analysis
# 

# In[24]:


popular_dishes = Merged_Dataset['Dish_Name'].value_counts().head(10)
popular_dishes.head(10)


# ### 16. Demographic Influences Analysis

# In[25]:


age_meal_type = Merged_Dataset.groupby('Age')['Meal_Type'].value_counts().unstack().fillna(0)
location_meal_type = Merged_Dataset.groupby('Location')['Meal_Type'].value_counts().unstack().fillna(0)
age_meal_type.head(10)


# In[26]:


location_meal_type.head(10)


# ### 17. Visualize Top Dishes

# In[27]:


import matplotlib.pyplot as plt
import seaborn as sns


plt.figure(figsize=(10, 6))
sns.barplot(x=popular_dishes.index, y=popular_dishes.values, color='skyblue')  # Use a single color
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Most Ordered Dishes')
plt.xlabel("Dish Name")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()
print("Bar chart showing the frequency of the top 10 most ordered dishes.")


# ### 18. Visualize Meal Type Preferences by Age

# In[30]:


age_meal_type_simplified = age_meal_type.reset_index().melt(id_vars='Age', var_name='Meal Type', value_name='Count')

plt.figure(figsize=(12, 8))
sns.barplot(x='Age', y='Count', hue='Meal Type', data=age_meal_type_simplified, palette='Set2')
plt.title('Meal Type Preferences by Age')
plt.xlabel('Age Group')
plt.ylabel('Number of Preferences')
plt.legend(title='Meal Type')
plt.tight_layout()
plt.show()
print("Grouped bar chart showing meal type preferences across different age groups.")


# ### 19. Visualize Meal Type Preferences by Location

# In[31]:


location_meal_type_simplified = location_meal_type.reset_index().melt(id_vars='Location', var_name='Meal Type', value_name='Count')

plt.figure(figsize=(12, 8))
sns.barplot(x='Location', y='Count', hue='Meal Type', data=location_meal_type_simplified, palette='Set3')
plt.title('Meal Type Preferences by Location')
plt.xlabel('Location')
plt.ylabel('Number of Preferences')
plt.legend(title='Meal Type')
plt.tight_layout()
plt.show()
print("Grouped bar chart showing meal type preferences across different locations.")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### 20. Analyze Order Status

# In[32]:


if 'Order Status' in Merged_Dataset.columns:

    status_counts = Merged_Dataset['Order Status'].value_counts()
    status_percentages = Merged_Dataset['Order Status'].value_counts(normalize=True) * 100

  
    status_summary = pd.DataFrame({
        'Order Status': status_counts.index,
        'Count': status_counts.values,
        'Percentage': status_percentages.values
    })

   
    plt.figure(figsize=(8, 6))
    sns.barplot(
        x='Order Status', 
        y='Percentage', 
        data=status_summary, 
        hue='Order Status', 
        palette=['lightgreen', 'skyblue']
    )
    plt.title('Percentage of Order Status')
    plt.xlabel('Order Status')
    plt.ylabel('Percentage')
    plt.ylim(0, 100)  # Set y-axis to percentage range
    plt.tight_layout()
    plt.show()

    print("Bar chart showing the percentage of 'Completed' and 'Canceled' orders.")
else:
    print("Error: 'Order Status' column not found in the dataset.")


# In[ ]:




