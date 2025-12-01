# Route Planning Guide

## Step-by-Step Route Planning

### Step 1: Define Origin and Destination

Enter port names or UN/LOCODE codes:
- **UN/LOCODE**: 5-letter code (e.g., SGSIN for Singapore)
- **Port Name**: Full or partial name

**Pro Tip**: Start typing and select from autocomplete suggestions for accurate results.

### Step 2: Set Departure Time

- Select date and time for departure
- Times are in UTC by default
- Consider port operating hours

### Step 3: Configure Vessel Constraints

#### Vessel Type
| Type | Typical Use |
|------|-------------|
| Container | TEU cargo |
| Tanker | Liquid cargo |
| Bulk | Dry bulk cargo |
| RoRo | Vehicles |
| General Cargo | Mixed cargo |

#### Dimensions
- **Length**: Overall vessel length (meters)
- **Beam**: Maximum width (meters)
- **Draft**: Maximum depth below waterline (meters)

**Important**: Accurate dimensions affect:
- Canal eligibility (Suez, Panama)
- Port accessibility
- Route alternatives

#### Speed
- **Cruise Speed**: Normal operating speed (knots)
- Affects fuel consumption and ETA

### Step 4: Choose Optimization Criteria

| Criteria | Optimizes For | Best When |
|----------|--------------|-----------|
| **Time** | Fastest arrival | Urgent cargo |
| **Cost** | Lowest total cost | Cost-sensitive shipping |
| **Reliability** | Safest route | Valuable/fragile cargo |
| **Balanced** | Best trade-off | General shipping |

### Step 5: Review and Calculate

1. Review all parameters
2. Click "Calculate Route"
3. Wait for results (typically < 500ms)

## Understanding Results

### Route Map

- **Blue line**: Primary recommended route
- **Gray lines**: Alternative routes
- **Red markers**: Waypoints/ports
- **Green marker**: Origin
- **Red marker**: Destination

### Route Details

#### Waypoints
Each waypoint shows:
- Port name and code
- Estimated arrival time
- Estimated departure time
- Distance from previous point

#### Cost Breakdown
- Fuel costs (based on consumption model)
- Port fees (entry/exit)
- Canal tolls (if applicable)
- Total estimated cost

### Comparing Routes

Click on alternative routes to compare:
- Distance difference
- Time difference
- Cost difference
- Risk assessment

## Advanced Options

### Multiple Waypoints
Add intermediate stops:
1. Click "Add Waypoint"
2. Select intermediate port
3. Set minimum port time
4. Reorder as needed

### Constraints
- Maximum draft at waypoints
- Canal compatibility requirements
- Avoiding specific regions

## Exporting Routes

Export calculated routes:
- **PDF Report** - Detailed route documentation
- **Excel** - Waypoint data for analysis
- **JSON** - API integration format

## Best Practices

1. **Verify vessel data** - Incorrect dimensions affect route validity
2. **Consider weather** - Check seasonal patterns
3. **Review alternatives** - Cost savings may outweigh time
4. **Plan port time** - Allow buffer for port operations
