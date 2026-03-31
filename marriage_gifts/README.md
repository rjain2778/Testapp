# Marriage Gifts API

FastAPI application for managing wedding gift registries with overflow adjustment strategy.

## Features

- 🎁 Create gift parties and add items to wishlist
- 👥 Manage guests and send invitations
- 💰 Accept contributions with automatic overflow adjustment
- 💳 Process payments via Razorpay, Paytm, Bank Transfer, or Cash
- 📧 Send email notifications for invitations and receipts
- 📊 Calculate item funding status
- 🔄 Overflow adjustment: Contributions are automatically allocated to items, with overflow going as cash contribution

## Setup

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn main:app --reload

# Or use docker
docker-compose up
```

### Production

```bash
# Using gunicorn
gunicorn "main:app" --bind 0.0.0.0:8000 --workers 4
```

### Environment Variables

```bash
# Create .env file
cp .env.example .env

# Required:
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/marriage_gifts
```

## API Endpoints

### Parties

- `POST /party/` - Create a new gift party
- `GET /party/{party_id}/` - Get party by ID
- `GET /party/{party_id}/items/` - Get all items for a party
- `PUT /party/{party_id}/` - Update party details
- `DELETE /party/{party_id}/` - Delete a party

### Guests

- `POST /guest/` - Create a new guest invitation
- `GET /guest/{guest_id}/` - Get guest by ID
- `GET /guest/{party_id}/guest/{email}/` - Get guest by party and email
- `GET /guest/{party_id}/` - List guests for a party

### Items

- `POST /item/` - Create a new item
- `GET /item/{item_id}/` - Get item by ID
- `GET /item/{party_id}/` - Get all items for a party
- `PUT /item/{item_id}/` - Update item details
- `DELETE /item/{item_id}/` - Delete an item

### Contributions

- `POST /contribution/` - Create a new contribution
- `GET /contribution/{contribution_id}/` - Get contribution by ID
- `GET /contribution/{party_id}/` - List contributions for a party

## Architecture

```
┌─────────────────────────────────────────────┐
│              API Layer                      │
│         (FastAPI Endpoints)                 │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│              Service Layer                  │
│          (Business Logic + Strategies)      │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│              Repository Layer               │
│           (Data Access Abstraction)         │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│              In-Memory Storage              │
│            (For testing/development)        │
└─────────────────────────────────────────────┘
```

## Payment Strategies

The app uses the Strategy Pattern for payment processing:

- Cash Payment (Default)
- Razorpay Payment
- Paytm Payment
- Bank Transfer (NEFT/RTGS/IMPS)

## License

MIT License
