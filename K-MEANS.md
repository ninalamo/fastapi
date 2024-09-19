
To apply **K-Means clustering** with **GIS data**, we combine geospatial data (e.g., latitude and longitude coordinates) with the K-Means algorithm to group spatial points based on proximity. In this scenario, you might cluster locations (e.g., cities, delivery points, or stores) to identify regional groupings or patterns.

### Steps to Apply K-Means Clustering with GIS:

1. **Collect Geospatial Data**:
   Obtain data with geographical coordinates (latitude and longitude). This data can represent anything from store locations to points of interest in a city.

2. **Preprocess the Data**:
   Ensure the data is cleaned and ready for clustering (remove missing values, handle outliers, etc.).

3. **Apply K-Means Clustering**:
   Use K-Means to group the locations based on their proximity to one another.

4. **Visualize the Clusters on a Map**:
   Visualize the clusters using libraries like `geopandas` and `matplotlib` for maps or `folium` for interactive maps.

### Example: K-Means Clustering with Geospatial Data

#### Step 1: Install Required Libraries

You'll need the following Python libraries:
```bash
pip install pandas numpy sklearn geopandas matplotlib folium
```

#### Step 2: Example Geospatial Dataset

Let's create a sample dataset with coordinates representing some locations. You can also use real-world data from sources like OpenStreetMap, Google Maps API, or public datasets.

```python
import pandas as pd
import numpy as np

# Sample dataset with geospatial coordinates (latitude, longitude)
data = {
    'location': ['Location1', 'Location2', 'Location3', 'Location4', 'Location5',
                 'Location6', 'Location7', 'Location8', 'Location9', 'Location10'],
    'latitude': [37.7749, 34.0522, 40.7128, 41.8781, 47.6062, 29.7604, 25.7617,
                 39.7392, 32.7767, 36.1627],
    'longitude': [-122.4194, -118.2437, -74.0060, -87.6298, -122.3321, -95.3698,
                  -80.1918, -104.9903, -96.7970, -86.7816]
}

# Create a DataFrame
df = pd.DataFrame(data)
print(df.head())
```

#### Step 3: Preprocess the Data for K-Means

K-Means requires numeric data, so we'll work with latitude and longitude coordinates directly. Normally, you'd need to consider scaling or projecting the coordinates for better clustering results.

```python
from sklearn.cluster import KMeans

# Extract the latitude and longitude into a new variable
coords = df[['latitude', 'longitude']].values

# Specify the number of clusters (e.g., 3)
kmeans = KMeans(n_clusters=3, random_state=42)

# Fit the KMeans model and predict the clusters
df['cluster'] = kmeans.fit_predict(coords)

# Show the resulting dataframe with cluster assignments
print(df)
```

#### Step 4: Visualize the Clusters on a Map

To visualize the clusters, we can use `geopandas` for static maps or `folium` for interactive maps.

##### Using `geopandas` and `matplotlib` for Static Maps

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Plot the clusters with different colors
gdf.plot(column='cluster', cmap='viridis', legend=True, figsize=(10, 6))
plt.title('K-Means Clustering of Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
```

##### Using `folium` for Interactive Maps

```python
import folium

# Initialize a Folium map centered around the average latitude and longitude
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

# Define colors for clusters
cluster_colors = ['red', 'blue', 'green']

# Add markers for each location
for i, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['location'],
        icon=folium.Icon(color=cluster_colors[row['cluster']])
    ).add_to(m)

# Show the interactive map
m.save("map.html")  # This saves the map to an HTML file
m  # If you're in a Jupyter notebook, this will display the map directly
```

### Step 5: Interpret the Results

Once the clusters are assigned and visualized, you can:
- Identify which locations are grouped together based on their geographic proximity.
- Analyze the clusters to understand regional patterns, e.g., which cities are grouped into certain regions or zones.
- Use this information for decision-making in business (e.g., optimizing delivery routes, store placements).

### Full Example Code

```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

# Step 1: Create a sample dataset with latitude and longitude
data = {
    'location': ['Location1', 'Location2', 'Location3', 'Location4', 'Location5',
                 'Location6', 'Location7', 'Location8', 'Location9', 'Location10'],
    'latitude': [37.7749, 34.0522, 40.7128, 41.8781, 47.6062, 29.7604, 25.7617,
                 39.7392, 32.7767, 36.1627],
    'longitude': [-122.4194, -118.2437, -74.0060, -87.6298, -122.3321, -95.3698,
                  -80.1918, -104.9903, -96.7970, -86.7816]
}

df = pd.DataFrame(data)

# Step 2: Prepare data for K-Means clustering
coords = df[['latitude', 'longitude']].values
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(coords)

# Step 3: Visualize using geopandas and matplotlib
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
gdf.plot(column='cluster', cmap='viridis', legend=True, figsize=(10, 6))
plt.title('K-Means Clustering of Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Step 4: Visualize interactively using folium
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)
cluster_colors = ['red', 'blue', 'green']
for i, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['location'],
        icon=folium.Icon(color=cluster_colors[row['cluster']])
    ).add_to(m)
m.save("map.html")
m  # If in a Jupyter notebook, this will display the map
```

### Summary

By using K-Means clustering with GIS data:
- You can group locations based on geographical proximity.
- It’s a powerful tool for spatial analysis in areas such as urban planning, delivery route optimization, and customer segmentation.
- The clusters can be easily visualized on a map, which helps in decision-making.
