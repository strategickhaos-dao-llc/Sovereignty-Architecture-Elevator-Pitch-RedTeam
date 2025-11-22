#!/bin/bash
# View events from the webhook inbox

CONTAINER_NAME="strategickhaos-webhook-inbox"
INBOX_FILE="/inbox/events.log"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}⚠️  Container ${CONTAINER_NAME} is not running${NC}"
    echo "Start it with: ./start.sh"
    exit 1
fi

# Parse command line arguments
MODE="${1:-tail}"
LINES="${2:-50}"

case "$MODE" in
    all)
        echo -e "${GREEN}📥 All events from inbox:${NC}"
        # More efficient: read all lines at once and format with jq if available
        if command -v jq &> /dev/null; then
            docker exec "$CONTAINER_NAME" cat "$INBOX_FILE" | jq -r '.'
        else
            docker exec "$CONTAINER_NAME" cat "$INBOX_FILE"
        fi
        ;;
    tail)
        echo -e "${GREEN}📥 Last $LINES events:${NC}"
        # More efficient: read all lines at once and format with jq if available
        if command -v jq &> /dev/null; then
            docker exec "$CONTAINER_NAME" tail -n "$LINES" "$INBOX_FILE" | jq -r '.'
        else
            docker exec "$CONTAINER_NAME" tail -n "$LINES" "$INBOX_FILE"
        fi
        ;;
    follow|watch)
        echo -e "${GREEN}📥 Following new events (Ctrl+C to stop):${NC}"
        docker exec "$CONTAINER_NAME" tail -f "$INBOX_FILE"
        ;;
    count)
        count=$(docker exec "$CONTAINER_NAME" sh -c "wc -l < $INBOX_FILE" 2>/dev/null || echo "0")
        echo -e "${GREEN}📊 Total events logged: $count${NC}"
        ;;
    *)
        echo "Usage: $0 [all|tail|follow|count] [lines]"
        echo ""
        echo "Modes:"
        echo "  all     - Show all events (formatted JSON)"
        echo "  tail    - Show last N events (default: 50)"
        echo "  follow  - Follow new events in real-time"
        echo "  count   - Show total event count"
        echo ""
        echo "Examples:"
        echo "  $0 tail 100    # Show last 100 events"
        echo "  $0 follow      # Watch for new events"
        echo "  $0 count       # Show event count"
        exit 1
        ;;
esac
