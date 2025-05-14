# Import necessary libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.decomposition import PCA

# Load the Big Five Personality dataset with tab-separated values
data_raw = pd.read_csv('/Users/robin/Desktop/Personalty_AI/sampled_100k_data.csv', sep='\t')

data = data_raw.copy()

# Check for missing values
print('Is there any missing value? ', data.isnull().values.any())
print('How many missing values? ', data.isnull().values.sum())

# Drop rows with missing values
data.dropna(inplace=True)
print('Number of participants after eliminating missing values: ', len(data))

# Drop unnecessary columns (non-personality-related columns)
data.drop(data.columns[50:107], axis=1, inplace=True)
data.drop(data.columns[51:], axis=1, inplace=True)

# Check the number of participants
print('Number of participants: ', len(data))

# Country distribution plot
countries = pd.DataFrame(data['country'].value_counts())
countries_5000 = countries[countries['country'] >= 5000]
plt.figure(figsize=(15,5))
sns.barplot(data=countries_5000, x=countries_5000.index, y='country')
plt.title('Countries With More Than 5000 Participants')
plt.ylabel('Participants')
plt.show()  # Display plot and wait for it to be closed

# Define questions related to each personality trait
ext_questions = {'EXT1' : 'I am the life of the party', 'EXT2' : 'I don’t talk a lot', 'EXT3' : 'I feel comfortable around people', 'EXT4' : 'I keep in the background', 'EXT5' : 'I start conversations', 'EXT6' : 'I have little to say', 'EXT7' : 'I talk to a lot of different people at parties', 'EXT8' : 'I don’t like to draw attention to myself', 'EXT9' : 'I don’t mind being the center of attention', 'EXT10': 'I am quiet around strangers'}
est_questions = {'EST1' : 'I get stressed out easily', 'EST2' : 'I am relaxed most of the time', 'EST3' : 'I worry about things', 'EST4' : 'I seldom feel blue', 'EST5' : 'I am easily disturbed', 'EST6' : 'I get upset easily', 'EST7' : 'I change my mood a lot', 'EST8' : 'I have frequent mood swings', 'EST9' : 'I get irritated easily', 'EST10': 'I often feel blue'}
agr_questions = {'AGR1' : 'I feel little concern for others', 'AGR2' : 'I am interested in people', 'AGR3' : 'I insult people', 'AGR4' : 'I sympathize with others’ feelings', 'AGR5' : 'I am not interested in other peoples’ problems', 'AGR6' : 'I have a soft heart', 'AGR7' : 'I am not really interested in others', 'AGR8' : 'I take time out for others', 'AGR9' : 'I feel others’ emotions', 'AGR10': 'I make people feel at ease'}
csn_questions = {'CSN1' : 'I am always prepared', 'CSN2' : 'I leave my belongings around', 'CSN3' : 'I pay attention to details', 'CSN4' : 'I make a mess of things', 'CSN5' : 'I get chores done right away', 'CSN6' : 'I often forget to put things back in their proper place', 'CSN7' : 'I like order', 'CSN8' : 'I shirk my duties', 'CSN9' : 'I follow a schedule', 'CSN10' : 'I am exacting in my work'}
opn_questions = {'OPN1' : 'I have a rich vocabulary', 'OPN2' : 'I have difficulty understanding abstract ideas', 'OPN3' : 'I have a vivid imagination', 'OPN4' : 'I am not interested in abstract ideas', 'OPN5' : 'I have excellent ideas', 'OPN6' : 'I do not have a good imagination', 'OPN7' : 'I am quick to understand things', 'OPN8' : 'I use difficult words', 'OPN9' : 'I spend time reflecting on things', 'OPN10': 'I am full of ideas'}

# Group column names for each personality trait
EXT = [column for column in data if column.startswith('EXT')]
EST = [column for column in data if column.startswith('EST')]
AGR = [column for column in data if column.startswith('AGR')]
CSN = [column for column in data if column.startswith('CSN')]
OPN = [column for column in data if column.startswith('OPN')]

# Function to visualize distributions of answers for a personality trait
def vis_questions(groupname, questions, color):
    plt.figure(figsize=(20,10))
    for i in range(1, 11):
        plt.subplot(2,5,i)
        plt.hist(data[groupname[i-1]], bins=14, color=color, alpha=.5)
        plt.title(questions[groupname[i-1]], fontsize=12)
    plt.show()  # Display each set of subplots one by one

# Visualizing distributions for each trait individually
vis_questions(EST, est_questions, 'pink')  # Neuroticism
vis_questions(AGR, agr_questions, 'red')   # Agreeableness

# Apply scaling to the entire data without sampling
df = data.drop('country', axis=1)
columns = list(df.columns)
scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(df)

# Determine optimal clusters using a sample of 5000 rows for elbow visualization
df_sample = pd.DataFrame(df, columns=columns).sample(5000)
visualizer = KElbowVisualizer(KMeans(n_init=10), k=(2, 15))
visualizer.fit(df_sample)
visualizer.poof()

# Create K-means clustering model with 5 clusters on all data
kmeans = KMeans(n_clusters=5, n_init=10)
data['Clusters'] = kmeans.fit_predict(df)

# Summing responses for each trait to visualize clusters
col_list = list(df_sample.columns)
traits = {'extroversion': col_list[0:10], 'neurotic': col_list[10:20], 'agreeable': col_list[20:30], 'conscientious': col_list[30:40], 'open': col_list[40:50]}
data_sums = pd.DataFrame({trait: data[cols].sum(axis=1)/10 for trait, cols in traits.items()})
data_sums['clusters'] = data['Clusters']

# Plot average trait values per cluster
dataclusters = data_sums.groupby('clusters').mean()
plt.figure(figsize=(22,3))
for i in range(5):
    plt.subplot(1,5,i+1)
    plt.bar(dataclusters.columns, dataclusters.iloc[i], color='green', alpha=0.2)
    plt.plot(dataclusters.columns, dataclusters.iloc[i], color='red')
    plt.title(f'Cluster {i}')
    plt.xticks(rotation=45)
    plt.ylim(0,4)
plt.show()  # Display cluster bar charts one at a time

# Use PCA for 2D visualization of clusters
pca = PCA(n_components=2)
pca_fit = pca.fit_transform(df)
df_pca = pd.DataFrame(data=pca_fit, columns=['PCA1', 'PCA2'])
df_pca['Clusters'] = data['Clusters']

# Plot the PCA-reduced clusters
plt.figure(figsize=(10,10))
sns.scatterplot(data=df_pca, x='PCA1', y='PCA2', hue='Clusters', palette='Set2', alpha=0.8)
plt.title('Personality Clusters after PCA')
plt.show()
