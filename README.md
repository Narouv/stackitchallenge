# Notification Service API

A RESTful web service that forwards notifications to Discord based on their type.

## Setup

1. **Create `.env` file**
   ```bash
   WEBHOOK_URL=<your_discord_webhook_url>
   ```

2. **Start the service**
   ```bash
   docker-compose up -d
   ```

3. **Test it works**
   ```bash
   curl http://localhost:8000/docs
   ```
   or open this up in a browser

## Usage

**Sending a warning gets forwarded immediately:**
```bash
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{"type": "warning", "name": "Alert", "description": "Something happened"}'
```

**Sending a info message gets saved for later:**
```bash
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{"type": "info", "name": "Update", "description": "System updated"}'
```

**Sending warning with ?send_saved adds last 2 saved messages:**
```bash
curl -X POST "http://localhost:8000/notify?send_saved=2" \
  -H "Content-Type: application/json" \
  -d '{"type": "warning", "name": "Alert", "description": "Something urgent"}'
```

**delete saved messages:**
```bash
curl http://localhost:8000/clear
```

## Message Types

- **warning/critical**: Sent to Discord immediately
- **info/fortnite**: Saved in memory, sent when requested via `?send_saved=N`
