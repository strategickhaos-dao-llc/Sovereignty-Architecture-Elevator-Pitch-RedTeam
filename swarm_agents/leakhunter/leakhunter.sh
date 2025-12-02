#!/bin/bash
# LeakHunter Swarm - Shell Launcher
# For Linux/Unix/macOS systems

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Print header
echo -e "${CYAN}🛡️  LeakHunter Swarm Control Panel${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# Print usage
usage() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  quick-scan       Quick torrent scan (< 30 seconds)
  deep-scan        Deep torrent scan (30-60 minutes)
  darkweb          Dark web crawler (Tor/I2P/Lokinet)
  magnet           Magnet link harvester
  watermark        Watermark detector (requires --file or --directory)
  alert            Test Discord alert system
  global-sweep     Full global sweep (4+ hours)
  test             Run test suite

Options:
  --config FILE    Path to configuration file
  --output FILE    Path to save results
  --file FILE      File to scan (for watermark)
  --directory DIR  Directory to scan (for watermark)
  --webhook URL    Discord webhook URL (for alerts)

Examples:
  $0 quick-scan
  $0 deep-scan --output /tmp/results.json
  $0 darkweb --config config.json
  $0 watermark --file suspicious.gguf
  $0 global-sweep --output /var/log/leakhunter

EOF
    exit 1
}

# Parse arguments
COMMAND="${1:-quick-scan}"
shift || true

CONFIG=""
OUTPUT=""
FILE=""
DIRECTORY=""
WEBHOOK=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --file)
            FILE="$2"
            shift 2
            ;;
        --directory)
            DIRECTORY="$2"
            shift 2
            ;;
        --webhook)
            WEBHOOK="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Build common args
build_args() {
    local args=""
    [[ -n "$CONFIG" ]] && args="$args --config $CONFIG"
    [[ -n "$OUTPUT" ]] && args="$args --output $OUTPUT"
    echo "$args"
}

# Command handlers
cmd_torrent_scan() {
    local mode="$1"
    echo -e "${YELLOW}🔍 Launching Torrent Leak Scanner ($mode mode)...${NC}"
    python3 "$BASE_DIR/torrent_leak_scanner.py" "--$mode" $(build_args)
}

cmd_darkweb() {
    echo -e "${YELLOW}🕸️  Launching Dark Web Crawler...${NC}"
    python3 "$BASE_DIR/darkweb_onion_crawler.py" $(build_args)
}

cmd_magnet() {
    echo -e "${YELLOW}🧲 Launching Magnet Harvester...${NC}"
    python3 "$BASE_DIR/magnet_harvester.py" $(build_args)
}

cmd_watermark() {
    echo -e "${YELLOW}🔬 Launching Watermark Detector...${NC}"
    
    if [[ -z "$FILE" && -z "$DIRECTORY" ]]; then
        echo -e "${RED}❌ Error: --file or --directory required for watermark scanning${NC}"
        exit 1
    fi
    
    local args=$(build_args)
    [[ -n "$FILE" ]] && args="$args --file $FILE"
    [[ -n "$DIRECTORY" ]] && args="$args --directory $DIRECTORY"
    
    python3 "$BASE_DIR/watermark_detector.py" $args
}

cmd_alert() {
    echo -e "${YELLOW}📨 Testing Discord Alert System...${NC}"
    
    local args="--test $(build_args)"
    [[ -n "$WEBHOOK" ]] && args="$args --webhook $WEBHOOK"
    
    python3 "$BASE_DIR/alert_to_discord.py" $args
}

cmd_global_sweep() {
    echo -e "${YELLOW}🌍 Launching Full Global Sweep...${NC}"
    echo -e "${YELLOW}⚠️  This will take 4+ hours on a 64-core system${NC}"
    echo ""
    
    read -p "Continue? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    
    local args=$(build_args)
    python3 "$BASE_DIR/full_global_sweep.py" $args
}

cmd_test() {
    echo -e "${YELLOW}🧪 Running LeakHunter Test Suite...${NC}"
    python3 "$BASE_DIR/test_suite.py"
}

# Execute command
case "$COMMAND" in
    quick-scan)
        cmd_torrent_scan "quick-scan"
        ;;
    deep-scan)
        cmd_torrent_scan "deep-scan"
        ;;
    darkweb)
        cmd_darkweb
        ;;
    magnet)
        cmd_magnet
        ;;
    watermark)
        cmd_watermark
        ;;
    alert)
        cmd_alert
        ;;
    global-sweep)
        cmd_global_sweep
        ;;
    test)
        cmd_test
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        usage
        ;;
esac

echo ""
echo -e "${CYAN}======================================================================${NC}"
echo -e "${GREEN}✅ LeakHunter Swarm operation complete${NC}"
