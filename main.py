import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#1.Loading, Cleaning 

#Load data
df = pd.read_csv('retail_store_sales.csv')

# Display basic information about the dataset
#print(df.shape)
#print(df.head())
#print(df.dtypes)
#print(df.describe(include='all'))

#Filtering by missing items
bool_series = pd.isnull(df['Item'])

#print(df[bool_series])

#Filling Item column based on Category and Price Per Unit columns
df['Item'] = df.apply(
    lambda row: df[(df['Category'] == row['Category']) *
                   (df['Price Per Unit'] == row['Price Per Unit'])]['Item'].dropna().mode()[0]
    if pd.isnull(row['Item']) and not df[(df['Category'] == row['Category']) &
                                         (df['Price Per Unit'] == row['Price Per Unit'])]['Item'].dropna().empty
    else row['Item'], axis = 1
)
#Filling Price Per Unit column based on Category and Item columns
df['Price Per Unit'] = df.apply(
    lambda row: df[(df['Category'] == row['Category']) &
                   (df['Item'] == row['Item'])]['Price Per Unit'].dropna.median()
    if pd.isnull(row['Price Per Unit']) and not df[(df['Category'] == row['Category']) &
                                                   (df['Item'] == row['Item'])]['Price Per Unit'].dropna().empty
    else row['Price Per Unit'], axis = 1
)
df['Discount Applied'].fillna(False, inplace=True)


#Dropping missing values
df = df.dropna()

#Univariate analysis
numerical_cols = ['Price Per Unit', 'Quantity', 'Total Spent']
df[numerical_cols].hist(bins = 30, figsize=(15,10))
plt.suptitle('Histograms of Numerical Variables')
plt.show()
plt.close()

plt.figure(figsize=(15, 10))
sns.boxplot(data=df[numerical_cols])
plt.title('Boxplots of Numerical Variables')
plt.show()
plt.close()

categorical_cols = ['Category', 'Item', 'Payment Method', 'Location', 'Discount Applied']

for col in categorical_cols:
    plt.figure(figsize=(10, 6))
    sns.countplot(y = col, data = df, order = df[col].value_counts().index)
    plt.title(f'Count of {col}')
    plt.show()
    plt.close()

#Bivariate analysis

#Correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
plt.close()
plt.savefig('visualizations/corr_matrix.jpg')

#Scatter plot between Price Per Unit and Total Spent
sns.scatterplot(x = 'Price Per Unit', y = 'Total Spent', data = df)
plt.title('Price Per Unit vs Total Spent')
plt.show()
plt.close()

#Boxplot for Category vs Total Spent
plt.figure(figsize=(12, 8))
sns.boxplot(x = 'Category', y = 'Total Spent', data = df)
plt.title('Boxplot: Category vs Total Spent')
plt.xticks(rotation = 45)
plt.savefig('visualizations/category_vs_total_spent.jpg')
plt.show()
plt.close()

#Cross-tabulation between two categorical variables
cross_tab = pd.crosstab(df['Category'], df['Discount Applied'])
print(cross_tab)

#Stacked bar plot
cross_tab.plot(kind = 'bar', stacked = True, figsize = (10, 6))
plt.title('Stacked Bar Plot: Category vs Discount Applied')
plt.show()

#Multivariate Analysis

#Grouped bar plot for Category, Discount Applied, and Total Spent
grouped = df.groupby(['Category', 'Discount Applied'])['Total Spent'].mean().unstack()
grouped.plot(kind = 'bar', figsize = (12, 8))
plt.title('Category vs Discount Applied vs Total Spent')
plt.ylabel('Average Total Spent')
plt.show()
plt.savefig('visualizations/cat_vs_discount_vs_total_spent.jpg')

#Time series analysis

#Convert Transaction Date to datetime
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

#Time series plot
plt.figure(figsize = (12, 6))
df.set_index('Transaction Date')['Total Spent'].resample('M').sum().plot()
plt.title('Monthly Total Spent Over Time')
plt.show()
plt.close()

#Outlier Detection

#Outlier Detecion using boxplot
plt.figure(figsize = (12, 8))
sns.boxplot(data = df[['Price Per Unit', 'Quantity', 'Total Spent']])
plt.title('Boxplot for Outlier Detection')
plt.show()
plt.close()

#Average Price Per Unit Per Category
df['Avg Price Per Unit Per Category'] = df.groupby('Category')['Price Per Unit'].transform('mean')

#Total Revenue
df['Total Revenue'] = df['Price Per Unit'] * df['Quantity']

print(df.dtypes)

df.to_csv('retail_store_sales_cleaned.csv', index = 0)