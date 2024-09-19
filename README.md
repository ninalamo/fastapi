We’ll go through creating a complete FastAPI project with CRUD operations, including setting up the virtual environment, installing dependencies, and initializing the database.

### Complete Setup for FastAPI CRUD API

#### 1. **Create Project Directory**

```bash
mkdir fastapi-crud-docker
cd fastapi-crud-docker
```

#### 2. **Set Up Virtual Environment**

Create a virtual environment named `venv`:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 3. **Install Dependencies**

Install FastAPI, Uvicorn, and SQLAlchemy:

```bash
pip install fastapi uvicorn sqlalchemy
```

Add `python-dotenv` to handle environment variables (optional but recommended):

```bash
pip install python-dotenv
```

Create `requirements.txt`:

```bash
pip freeze > requirements.txt
```

#### 4. **Create Project Files**

**1. `app/main.py`**:
This file contains the FastAPI application and routes.

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from . import crud, models, database

app = FastAPI()

# Initialize database
database.init_db()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    done: bool = False

class ItemInDB(Item):
    id: int

# Create Item
@app.post("/items/", response_model=ItemInDB)
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item

# Read Items
@app.get("/items/", response_model=List[ItemInDB])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items

# Read Item by ID
@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Update Item
@app.put("/items/{item_id}", response_model=ItemInDB)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete Item
@app.delete("/items/{item_id}", response_model=ItemInDB)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

**2. `app/models.py`**:
Define the SQLAlchemy model for the items.

```python
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, default=False)
```

**3. `app/crud.py`**:
CRUD operations interact with the database.

```python
from sqlalchemy.orm import Session
from . import models
from .main import Item

def create_item(db: Session, item: Item):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: Item):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
```

**4. `app/database.py`**:
Database connection and session setup.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for simplicity

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
```

#### 5. **Run the Application Locally**

Make sure you are in your virtual environment and run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` in your browser to see the interactive API documentation provided by FastAPI.

#### 6. **Build and Run with Docker (Optional)**

**Create a `Dockerfile`:**

```Dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create a `docker-compose.yml`:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

**Build and run the Docker container:**

```bash
docker-compose up --build
```

Visit `http://localhost:8000/docs` to access the API.

### Summary

- **Project Structure**: Includes `main.py`, `models.py`, `crud.py`, and `database.py`.
- **Database Initialization**: `init_db` creates tables.
- **Running Locally**: Use Uvicorn to run the FastAPI app.
- **Docker Setup**: Optional but useful for containerizing the application.

Let me know if you encounter any issues or have further questions!

====================================================================================================================================================

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
