# Trading Engine API Reference v1.0

> **Document Type**: API Reference  
> **Status**: DRAFT  
> **Last Updated**: 2025-11-25  
> **Base URL**: `https://api.trading.sovereignty.local/v1`

---

## 1. Overview

### 1.1 Authentication

All API requests require authentication via Bearer token:

```bash
Authorization: Bearer <access_token>
```

Tokens are obtained via Keycloak OAuth2 flow.

### 1.2 Rate Limits

| Endpoint Type | Rate Limit | Burst |
|---------------|------------|-------|
| Orders | 100/minute | 20 |
| Queries | 300/minute | 50 |
| Market Data | 600/minute | 100 |
| Admin | 30/minute | 5 |

### 1.3 Response Format

All responses follow standard JSON format:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-11-25T12:00:00Z"
  }
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { ... }
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-11-25T12:00:00Z"
  }
}
```

---

## 2. Orders API

### 2.1 Create Order

**Endpoint**: `POST /orders`

**Request Body**:
```json
{
  "symbol": "BTC-USD",
  "side": "buy",
  "type": "limit",
  "quantity": "1.5",
  "price": "50000.00",
  "time_in_force": "GTC",
  "client_order_id": "optional-client-id"
}
```

**Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Trading pair symbol |
| side | string | Yes | `buy` or `sell` |
| type | string | Yes | `limit`, `market`, `stop_limit` |
| quantity | string | Yes | Order quantity (decimal string) |
| price | string | Conditional | Required for limit orders |
| time_in_force | string | No | `GTC`, `IOC`, `FOK` (default: `GTC`) |
| client_order_id | string | No | Client-provided order ID |
| stop_price | string | Conditional | Required for stop orders |

**Response**:
```json
{
  "success": true,
  "data": {
    "order_id": "ord_123456789",
    "client_order_id": "optional-client-id",
    "symbol": "BTC-USD",
    "side": "buy",
    "type": "limit",
    "quantity": "1.5",
    "price": "50000.00",
    "status": "pending",
    "created_at": "2025-11-25T12:00:00Z"
  }
}
```

### 2.2 Get Order

**Endpoint**: `GET /orders/{order_id}`

**Response**:
```json
{
  "success": true,
  "data": {
    "order_id": "ord_123456789",
    "symbol": "BTC-USD",
    "side": "buy",
    "type": "limit",
    "quantity": "1.5",
    "filled_quantity": "0.5",
    "price": "50000.00",
    "average_price": "49999.50",
    "status": "partially_filled",
    "created_at": "2025-11-25T12:00:00Z",
    "updated_at": "2025-11-25T12:05:00Z"
  }
}
```

### 2.3 Cancel Order

**Endpoint**: `DELETE /orders/{order_id}`

**Response**:
```json
{
  "success": true,
  "data": {
    "order_id": "ord_123456789",
    "status": "cancelled"
  }
}
```

### 2.4 List Orders

**Endpoint**: `GET /orders`

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| symbol | string | Filter by symbol |
| status | string | Filter by status |
| side | string | Filter by side |
| start_time | datetime | Start of time range |
| end_time | datetime | End of time range |
| limit | integer | Results per page (max 100) |
| cursor | string | Pagination cursor |

**Response**:
```json
{
  "success": true,
  "data": [
    { "order_id": "ord_123", ... },
    { "order_id": "ord_124", ... }
  ],
  "meta": {
    "cursor": "next_page_cursor",
    "has_more": true
  }
}
```

---

## 3. Positions API

### 3.1 Get Positions

**Endpoint**: `GET /positions`

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTC-USD",
      "quantity": "5.0",
      "average_entry_price": "48000.00",
      "current_price": "50000.00",
      "unrealized_pnl": "10000.00",
      "realized_pnl": "5000.00",
      "margin_used": "24000.00"
    }
  ]
}
```

### 3.2 Get Position by Symbol

**Endpoint**: `GET /positions/{symbol}`

**Response**:
```json
{
  "success": true,
  "data": {
    "symbol": "BTC-USD",
    "quantity": "5.0",
    "average_entry_price": "48000.00",
    "current_price": "50000.00",
    "unrealized_pnl": "10000.00",
    "realized_pnl": "5000.00"
  }
}
```

---

## 4. Account API

### 4.1 Get Account Balance

**Endpoint**: `GET /account/balance`

**Response**:
```json
{
  "success": true,
  "data": {
    "total_equity": "100000.00",
    "available_balance": "75000.00",
    "margin_used": "25000.00",
    "unrealized_pnl": "5000.00",
    "currencies": [
      {
        "currency": "USD",
        "total": "100000.00",
        "available": "75000.00",
        "hold": "25000.00"
      }
    ]
  }
}
```

### 4.2 Get Account Activity

**Endpoint**: `GET /account/activity`

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | `trade`, `deposit`, `withdrawal`, `fee` |
| start_time | datetime | Start of time range |
| end_time | datetime | End of time range |
| limit | integer | Results per page |

---

## 5. Market Data API

### 5.1 Get Ticker

**Endpoint**: `GET /market/ticker/{symbol}`

**Response**:
```json
{
  "success": true,
  "data": {
    "symbol": "BTC-USD",
    "last_price": "50000.00",
    "bid": "49999.00",
    "ask": "50001.00",
    "volume_24h": "1000000.00",
    "change_24h": "2.5",
    "high_24h": "51000.00",
    "low_24h": "48000.00",
    "timestamp": "2025-11-25T12:00:00Z"
  }
}
```

### 5.2 Get Order Book

**Endpoint**: `GET /market/orderbook/{symbol}`

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| depth | integer | Number of levels (default: 20, max: 100) |

**Response**:
```json
{
  "success": true,
  "data": {
    "symbol": "BTC-USD",
    "bids": [
      ["49999.00", "1.5"],
      ["49998.00", "2.0"]
    ],
    "asks": [
      ["50001.00", "1.0"],
      ["50002.00", "1.5"]
    ],
    "timestamp": "2025-11-25T12:00:00Z"
  }
}
```

### 5.3 Get Trades

**Endpoint**: `GET /market/trades/{symbol}`

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| limit | integer | Number of trades (default: 50, max: 500) |

---

## 6. WebSocket API

### 6.1 Connection

**Endpoint**: `wss://ws.trading.sovereignty.local/v1`

**Authentication**:
```json
{
  "type": "auth",
  "token": "<access_token>"
}
```

### 6.2 Subscriptions

**Subscribe to channel**:
```json
{
  "type": "subscribe",
  "channel": "ticker",
  "symbol": "BTC-USD"
}
```

**Available channels**:
- `ticker` - Real-time price updates
- `orderbook` - Order book updates
- `trades` - Recent trades
- `orders` - User order updates
- `positions` - Position updates

### 6.3 Messages

**Ticker update**:
```json
{
  "channel": "ticker",
  "symbol": "BTC-USD",
  "data": {
    "last_price": "50000.00",
    "volume": "100.5",
    "timestamp": "2025-11-25T12:00:00.123Z"
  }
}
```

---

## 7. Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Malformed request |
| AUTHENTICATION_FAILED | 401 | Invalid or expired token |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMITED | 429 | Rate limit exceeded |
| INSUFFICIENT_FUNDS | 400 | Not enough balance |
| ORDER_REJECTED | 400 | Order failed risk checks |
| MARKET_CLOSED | 400 | Market not available |
| INTERNAL_ERROR | 500 | Server error |

---

## 8. SDKs and Libraries

### 8.1 Official SDKs

- **Python**: `pip install trading-engine-sdk`
- **JavaScript**: `npm install @sovereignty/trading-sdk`
- **Java**: Maven/Gradle package available

### 8.2 Example (Python)

```python
from trading_engine import Client

client = Client(api_key="your_key", api_secret="your_secret")

# Place order
order = client.create_order(
    symbol="BTC-USD",
    side="buy",
    type="limit",
    quantity="1.0",
    price="50000.00"
)

print(f"Order ID: {order.id}")
```

---

**Related Documentation**:
- [architecture.md](architecture.md) - System architecture
- [deployment.md](deployment.md) - Deployment guide
- [security.md](security.md) - Security controls
