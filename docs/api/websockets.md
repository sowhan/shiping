# WebSocket API

## Overview

Real-time updates are provided via WebSocket connections for:
- Live vessel position tracking
- Route progress updates
- System notifications

## Connection

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.maritime-routes.com/ws');

// Authenticate after connection
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'your_jwt_token'
  }));
};
```

## Message Types

### Subscribe to Vessel Positions

```javascript
// Subscribe
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'vessel_positions',
  vessels: ['9876543', '1234567']  // IMO numbers
}));

// Incoming message
{
  "type": "vessel_position",
  "imo_number": "9876543",
  "position": {
    "latitude": 29.9187,
    "longitude": 32.5483,
    "heading": 315,
    "speed_knots": 12.5
  },
  "timestamp": "2024-01-25T14:30:00Z"
}
```

### Subscribe to Route Progress

```javascript
// Subscribe
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'route_progress',
  route_id: '550e8400-e29b-41d4-a716-446655440000'
}));

// Incoming message
{
  "type": "route_progress",
  "route_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress_percent": 45.2,
  "current_position": {
    "latitude": 12.3456,
    "longitude": 78.9012
  },
  "next_waypoint": {
    "port_code": "EGPSD",
    "eta": "2024-02-01T14:30:00Z"
  },
  "status": "on_schedule",
  "timestamp": "2024-01-25T14:30:00Z"
}
```

### Subscribe to Notifications

```javascript
// Subscribe
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'notifications'
}));

// Incoming message
{
  "type": "notification",
  "severity": "warning",
  "title": "Weather Alert",
  "message": "Storm warning in Mediterranean Sea",
  "affected_routes": ["route_123", "route_456"],
  "timestamp": "2024-01-25T14:30:00Z"
}
```

## Unsubscribe

```javascript
ws.send(JSON.stringify({
  type: 'unsubscribe',
  channel: 'vessel_positions'
}));
```

## Heartbeat

The server sends ping messages every 30 seconds. Client should respond with pong:

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'ping') {
    ws.send(JSON.stringify({ type: 'pong' }));
  }
};
```

## Reconnection

Implement exponential backoff for reconnection:

```javascript
let reconnectDelay = 1000;
const maxDelay = 30000;

function connect() {
  const ws = new WebSocket('wss://api.maritime-routes.com/ws');
  
  ws.onclose = () => {
    setTimeout(() => {
      reconnectDelay = Math.min(reconnectDelay * 2, maxDelay);
      connect();
    }, reconnectDelay);
  };
  
  ws.onopen = () => {
    reconnectDelay = 1000;
  };
}
```

## Error Handling

```javascript
{
  "type": "error",
  "code": "SUBSCRIPTION_FAILED",
  "message": "Invalid vessel IMO number",
  "details": {
    "imo_number": "invalid"
  }
}
```

## Rate Limits

- Maximum 100 subscriptions per connection
- Maximum 10 messages per second
- Connections limited to 8 hours (re-authenticate after)

## Browser Support

WebSocket is supported in all modern browsers. For older browsers, consider using Socket.IO for fallback support.
