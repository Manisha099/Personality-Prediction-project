# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.decomposition import PCA

# Load the dataset using comma as the separator
file_path = '/Users/robin/Desktop/Personalty_AI/sampled_100k_data.csv'
data = pd.read_csv(file_path, sep=',')

# Print all column names to verify correct loading
print("Column names:", data.columns.tolist())

# Filter to select only numeric columns, assuming that trait columns are numeric
numeric_data = data.select_dtypes(include=[np.number])

# Confirm that the numeric data is not empty
if numeric_data.empty:
    print("No numeric columns found for scaling or clustering. Check dataset structure.")
else:
    # Scale the numeric data
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(numeric_data)
    
    # Determine optimal clusters using a sample of 5000 rows for elbow visualization
    df_sample = pd.DataFrame(df, columns=numeric_data.columns).sample(5000)
    visualizer = KElbowVisualizer(KMeans(n_init=10), k=(2, 15))
    visualizer.fit(df_sample)
    visualizer.poof()

    # Create K-means clustering model with 5 clusters
    kmeans = KMeans(n_clusters=5, n_init=10)
    numeric_data['Clusters'] = kmeans.fit_predict(df)

    # Use PCA for 2D visualization of clusters
    pca = PCA(n_components=2)
    pca_fit = pca.fit_transform(df)
    df_pca = pd.DataFrame(data=pca_fit, columns=['PCA1', 'PCA2'])
    df_pca['Clusters'] = numeric_data['Clusters']

    # Plot PCA-reduced clusters
    plt.figure(figsize=(10,10))
    sns.scatterplot(data=df_pca, x='PCA1', y='PCA2', hue='Clusters', palette='Set2', alpha=0.8)
    plt.title('Personality Clusters after PCA')
    plt.show()
