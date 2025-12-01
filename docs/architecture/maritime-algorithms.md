# Maritime Algorithms

## Route Planning Algorithms

### 1. Dijkstra's Algorithm

Used for finding the shortest path between ports.

**Complexity:** O((V + E) log V) with priority queue

**Use Case:** Simple direct routes with distance optimization

```python
def dijkstra(graph, start, end):
    """
    Find shortest path using Dijkstra's algorithm.
    
    Args:
        graph: Port connectivity graph with edge weights
        start: Origin port node
        end: Destination port node
        
    Returns:
        List of ports representing optimal path
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous = {}
    
    while priority_queue:
        current_distance, current = heappop(priority_queue)
        
        if current == end:
            return reconstruct_path(previous, start, end)
            
        if current_distance > distances[current]:
            continue
            
        for neighbor, weight in graph[current].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heappush(priority_queue, (distance, neighbor))
    
    return None
```

### 2. A* Algorithm

Heuristic-based pathfinding for faster route calculations.

**Complexity:** O(E) in best case with good heuristic

**Use Case:** Routes where great circle distance provides good estimation

```python
def a_star(graph, start, end, heuristic):
    """
    Find optimal path using A* algorithm with maritime heuristic.
    
    Heuristic: Great circle distance between ports
    """
    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    came_from = {}
    
    while open_set:
        _, current = heappop(open_set)
        
        if current == end:
            return reconstruct_path(came_from, start, end)
            
        for neighbor, cost in graph[current].items():
            tentative_g = g_score[current] + cost
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heappush(open_set, (f_score[neighbor], neighbor))
    
    return None
```

### 3. Hub-Based Routing

For complex multi-hop routes through major shipping hubs.

**Complexity:** O(H × E) where H = number of hubs

**Use Case:** Long-distance routes requiring transshipment

## Maritime Calculations

### Great Circle Distance

```python
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate great circle distance between two points.
    
    Returns: Distance in nautical miles
    """
    R = 3440.065  # Earth radius in nautical miles
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    return R * c
```

### Estimated Time of Arrival (ETA)

```python
def calculate_eta(distance_nm, speed_knots, departure_time):
    """
    Calculate estimated time of arrival.
    
    Args:
        distance_nm: Distance in nautical miles
        speed_knots: Vessel speed in knots
        departure_time: Departure datetime
        
    Returns:
        ETA as datetime
    """
    duration_hours = distance_nm / speed_knots
    return departure_time + timedelta(hours=duration_hours)
```

### Fuel Consumption Estimation

```python
def estimate_fuel_consumption(distance_nm, vessel_type, speed_knots):
    """
    Estimate fuel consumption for route.
    
    Based on vessel type and speed-fuel curves.
    """
    # Base consumption rates (metric tons per day)
    BASE_CONSUMPTION = {
        "container": 150,
        "tanker": 80,
        "bulk": 45,
        "general_cargo": 25,
    }
    
    base_rate = BASE_CONSUMPTION.get(vessel_type, 50)
    
    # Speed factor (cubic relationship)
    reference_speed = 15  # knots
    speed_factor = (speed_knots / reference_speed) ** 3
    
    # Calculate consumption
    duration_days = distance_nm / (speed_knots * 24)
    return base_rate * speed_factor * duration_days
```

## Optimization Criteria

| Criteria | Weight Factors | Algorithm Preference |
|----------|----------------|---------------------|
| Time | Distance, Speed | A* with time heuristic |
| Cost | Fuel, Port fees, Canal tolls | Dijkstra with cost weights |
| Reliability | Weather, Political risk | Multi-criteria optimization |
| Balanced | Equal weights | Weighted combination |
