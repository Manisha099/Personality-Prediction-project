# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load the dataset using comma as the separator
file_path = '/Users/robin/Desktop/Personalty_AI/sampled_100k_data.csv'
data = pd.read_csv(file_path, sep=',')

# Select only trait columns without "_e" suffix or metadata columns
trait_columns = [col for col in data.columns if not col.endswith('_e') and col not in ['dateload', 'screenw', 'screenh', 'introelapse', 'testelapse', 'endelapse', 'ipc', 'lat_appx_lots_of_err', 'long_appx_lots_of_err']]
data = data[trait_columns]

# Convert columns to numeric, handling any non-numeric values
data = data.apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True)  # Drop rows with any missing values

# Run KMeans clustering with k=6 (as suggested by elbow plot)
kmeans = KMeans(n_clusters=6, n_init=10, random_state=42)
data['Clusters'] = kmeans.fit_predict(data)

# 1. Calculate average trait values per cluster and visualize as a bar plot
traits_per_cluster = data.groupby('Clusters').mean()

# Plotting average trait values per cluster
plt.figure(figsize=(20, 8))
traits_per_cluster.T.plot(kind='bar', figsize=(20, 8), alpha=0.7, colormap="viridis")
plt.title("Average Trait Values Per Cluster")
plt.xlabel("Personality Traits")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.legend(title="Cluster", loc="upper right")
plt.tight_layout()
plt.show()

# 2. Show distributions for each trait as histograms (one plot per trait across clusters)
# Define the trait groups for looping
trait_groups = {
    'Extroversion': [col for col in data.columns if col.startswith('ext')],
    'Neuroticism': [col for col in data.columns if col.startswith('est')],
    'Agreeableness': [col for col in data.columns if col.startswith('agr')],
    'Conscientiousness': [col for col in data.columns if col.startswith('csn')],
    'Openness': [col for col in data.columns if col.startswith('opn')]
}

# Visualizing distributions for each trait group across clusters
for trait_name, columns in trait_groups.items():
    plt.figure(figsize=(20, 8))
    for cluster in sorted(data['Clusters'].unique()):
        subset = data[data['Clusters'] == cluster]
        for col in columns:
            sns.kdeplot(subset[col], label=f"Cluster {cluster} - {col}", alpha=0.6)
    plt.title(f"Distribution of {trait_name} Traits Across Clusters")
    plt.xlabel("Score")
    plt.ylabel("Density")
    plt.legend(title="Clusters")
    plt.show()
