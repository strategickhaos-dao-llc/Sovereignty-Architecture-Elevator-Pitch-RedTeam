#!/bin/bash
# stream_to_twitch.sh - Sovereignty Architecture Twitch Streaming Automation
# Strategickhaos DAO LLC / Valoryield Engine™
# Purpose: Automated Twitch stream pipeline with protected DAO content
# Operator: Mobile Sovereignty Node
# Generated: 2025-11-25T23:00:00Z

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
STREAM_KEY="${TWITCH_STREAM_KEY:-}"
QUEUE_DIR="${QUEUE_DIR:-./queue}"
PLAYLIST_DIR="${PLAYLIST_DIR:-./playlists}"
PROTECTED_PLAYLIST="${PROTECTED_PLAYLIST:-./playlists/protected_dao.m3u}"
LOG_DIR="${LOG_DIR:-./logs}"
RTMP_URL="rtmp://live.twitch.tv/app"
STREAM_BITRATE="${STREAM_BITRATE:-4500k}"
AUDIO_BITRATE="${AUDIO_BITRATE:-160k}"
RESOLUTION="${RESOLUTION:-1920x1080}"
FPS="${FPS:-30}"

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
log() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[⚠]${NC} $*"
}

log_error() {
    echo -e "${RED}[✗]${NC} $*" >&2
}

log_info() {
    echo -e "${CYAN}[ℹ]${NC} $*"
}

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════════════════════
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║        SOVEREIGNTY ARCHITECTURE™ - TWITCH STREAM AUTOMATION          ║"
    echo "║                    Mobile Sovereignty Node Pipeline                   ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}  Strategickhaos DAO LLC / Valoryield Engine™${NC}"
    echo -e "${CYAN}  Protected DAO Content Streaming Pipeline${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
validate_dependencies() {
    log "Validating dependencies..."
    
    local deps=("ffmpeg" "curl")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${missing[*]}"
        log_info "Install with: sudo apt install ${missing[*]}"
        exit 1
    fi
    
    log_success "All dependencies verified"
}

validate_stream_key() {
    if [[ -z "$STREAM_KEY" ]]; then
        log_error "TWITCH_STREAM_KEY environment variable not set"
        log_info "Set with: export TWITCH_STREAM_KEY='your_stream_key'"
        exit 1
    fi
    
    log_success "Stream key configured"
}

validate_directories() {
    log "Validating directory structure..."
    
    # Create directories if they don't exist
    mkdir -p "$QUEUE_DIR" "$PLAYLIST_DIR" "$LOG_DIR"
    
    if [[ ! -d "$QUEUE_DIR" ]]; then
        log_error "Queue directory not accessible: $QUEUE_DIR"
        exit 1
    fi
    
    log_success "Directory structure validated"
}

# ═══════════════════════════════════════════════════════════════════════════════
# QUEUE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
load_queue() {
    log "Loading stream queue from: $QUEUE_DIR"
    
    local queue_files=()
    
    # Load video files from queue directory
    while IFS= read -r -d '' file; do
        queue_files+=("$file")
    done < <(find "$QUEUE_DIR" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" -o -name "*.mov" -o -name "*.webm" \) -print0 2>/dev/null | sort -z)
    
    if [ ${#queue_files[@]} -eq 0 ]; then
        log_warn "No video files found in queue directory"
        return 1
    fi
    
    log_success "Loaded ${#queue_files[@]} files from queue"
    
    # Export queue for use
    printf '%s\n' "${queue_files[@]}"
}

load_protected_playlist() {
    log "Loading protected DAO playlist..."
    
    if [[ ! -f "$PROTECTED_PLAYLIST" ]]; then
        log_warn "Protected playlist not found: $PROTECTED_PLAYLIST"
        log_info "Creating default protected playlist..."
        
        cat > "$PROTECTED_PLAYLIST" << 'PLAYLIST'
# Protected DAO Playlist
# Strategickhaos DAO LLC - Protected Content
# This playlist contains content protected under DAO governance
#
# Format: M3U
# Version: 1.0
#
# Files listed here are governed by DAO voting mechanisms
# and require authorization for public broadcast
#
#EXTM3U
#EXTINF:-1,DAO Welcome Message
# Add protected content paths here
PLAYLIST
        
        log_success "Created default protected playlist template"
    else
        log_success "Protected playlist loaded: $PROTECTED_PLAYLIST"
    fi
    
    # Count entries (excluding comments and empty lines)
    local entry_count
    entry_count=$(grep -cv '^#\|^$' "$PROTECTED_PLAYLIST" || echo "0")
    log_info "Protected playlist entries: $entry_count"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STREAM FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
generate_concat_file() {
    local concat_file="$LOG_DIR/concat_list.txt"
    local queue_input="$1"
    
    log "Generating concatenation file..."
    
    : > "$concat_file"
    
    while IFS= read -r video; do
        if [[ -n "$video" && -f "$video" ]]; then
            echo "file '$video'" >> "$concat_file"
        fi
    done <<< "$queue_input"
    
    # Verify the concat file has content
    if [[ ! -s "$concat_file" ]]; then
        log_error "No valid video files found in queue"
        return 1
    fi
    
    log_success "Concatenation file generated: $concat_file"
    echo "$concat_file"
}

start_stream() {
    local input_source="$1"
    local log_file
    log_file="$LOG_DIR/stream_$(date +%Y%m%d_%H%M%S).log"
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                      STARTING TWITCH STREAM                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log_info "Stream Resolution: $RESOLUTION"
    log_info "Stream Bitrate: $STREAM_BITRATE"
    log_info "Audio Bitrate: $AUDIO_BITRATE"
    log_info "FPS: $FPS"
    log_info "Log File: $log_file"
    
    # FFmpeg streaming command
    ffmpeg -hide_banner -loglevel warning \
        -re \
        -f concat -safe 0 -i "$input_source" \
        -c:v libx264 -preset veryfast -maxrate "$STREAM_BITRATE" -bufsize 9000k \
        -pix_fmt yuv420p -g $((FPS * 2)) \
        -c:a aac -b:a "$AUDIO_BITRATE" -ar 44100 \
        -s "$RESOLUTION" \
        -f flv "${RTMP_URL}/${STREAM_KEY}" \
        2>&1 | tee "$log_file"
}

stream_single_file() {
    local video_file="$1"
    local log_file
    log_file="$LOG_DIR/stream_$(date +%Y%m%d_%H%M%S).log"
    
    if [[ ! -f "$video_file" ]]; then
        log_error "Video file not found: $video_file"
        exit 1
    fi
    
    log_info "Streaming single file: $video_file"
    
    ffmpeg -hide_banner -loglevel warning \
        -re -i "$video_file" \
        -c:v libx264 -preset veryfast -maxrate "$STREAM_BITRATE" -bufsize 9000k \
        -pix_fmt yuv420p -g $((FPS * 2)) \
        -c:a aac -b:a "$AUDIO_BITRATE" -ar 44100 \
        -s "$RESOLUTION" \
        -f flv "${RTMP_URL}/${STREAM_KEY}" \
        2>&1 | tee "$log_file"
}

stream_test_pattern() {
    local log_file
    log_file="$LOG_DIR/test_stream_$(date +%Y%m%d_%H%M%S).log"
    
    log_info "Starting test pattern stream (60 seconds)..."
    
    ffmpeg -hide_banner -loglevel warning \
        -f lavfi -i "testsrc2=size=${RESOLUTION}:rate=${FPS}" \
        -f lavfi -i "sine=frequency=440:sample_rate=44100" \
        -t 60 \
        -c:v libx264 -preset veryfast -maxrate "$STREAM_BITRATE" -bufsize 9000k \
        -pix_fmt yuv420p -g $((FPS * 2)) \
        -c:a aac -b:a "$AUDIO_BITRATE" \
        -f flv "${RTMP_URL}/${STREAM_KEY}" \
        2>&1 | tee "$log_file"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STATUS FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
show_status() {
    echo -e "${BLUE}"
    echo "┌──────────────────────────────────────────────────────────────────────┐"
    echo "│                     STREAM PIPELINE STATUS                           │"
    echo "└──────────────────────────────────────────────────────────────────────┘"
    echo -e "${NC}"
    
    echo -e "${WHITE}Configuration:${NC}"
    echo -e "  Queue Directory:      ${CYAN}$QUEUE_DIR${NC}"
    echo -e "  Playlist Directory:   ${CYAN}$PLAYLIST_DIR${NC}"
    echo -e "  Protected Playlist:   ${CYAN}$PROTECTED_PLAYLIST${NC}"
    echo -e "  Log Directory:        ${CYAN}$LOG_DIR${NC}"
    echo ""
    
    echo -e "${WHITE}Stream Settings:${NC}"
    echo -e "  Resolution:           ${CYAN}$RESOLUTION${NC}"
    echo -e "  Video Bitrate:        ${CYAN}$STREAM_BITRATE${NC}"
    echo -e "  Audio Bitrate:        ${CYAN}$AUDIO_BITRATE${NC}"
    echo -e "  FPS:                  ${CYAN}$FPS${NC}"
    echo ""
    
    echo -e "${WHITE}Queue Status:${NC}"
    local queue_count
    queue_count=$(find "$QUEUE_DIR" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" -o -name "*.mov" -o -name "*.webm" \) 2>/dev/null | wc -l || echo "0")
    echo -e "  Videos in Queue:      ${CYAN}$queue_count${NC}"
    echo ""
    
    if [[ -n "${TWITCH_STREAM_KEY:-}" ]]; then
        echo -e "  Stream Key:           ${GREEN}✓ Configured${NC}"
    else
        echo -e "  Stream Key:           ${RED}✗ Not Set${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
show_help() {
    show_banner
    
    echo -e "${WHITE}USAGE:${NC}"
    echo "  $0 <command> [options]"
    echo ""
    echo -e "${WHITE}COMMANDS:${NC}"
    echo "  start         Start streaming from queue"
    echo "  stream <file> Stream a single video file"
    echo "  test          Stream test pattern (60 seconds)"
    echo "  status        Show pipeline status"
    echo "  queue         List files in queue"
    echo "  help          Show this help message"
    echo ""
    echo -e "${WHITE}ENVIRONMENT VARIABLES:${NC}"
    echo "  TWITCH_STREAM_KEY     Your Twitch stream key (required)"
    echo "  QUEUE_DIR             Queue directory (default: ./queue)"
    echo "  PLAYLIST_DIR          Playlist directory (default: ./playlists)"
    echo "  PROTECTED_PLAYLIST    Protected playlist file (default: ./playlists/protected_dao.m3u)"
    echo "  LOG_DIR               Log directory (default: ./logs)"
    echo "  STREAM_BITRATE        Video bitrate (default: 4500k)"
    echo "  AUDIO_BITRATE         Audio bitrate (default: 160k)"
    echo "  RESOLUTION            Stream resolution (default: 1920x1080)"
    echo "  FPS                   Frames per second (default: 30)"
    echo ""
    echo -e "${WHITE}EXAMPLES:${NC}"
    echo "  # Start streaming from queue"
    echo "  export TWITCH_STREAM_KEY='live_xxxxx'"
    echo "  $0 start"
    echo ""
    echo "  # Stream a single file"
    echo "  $0 stream /path/to/video.mp4"
    echo ""
    echo "  # Run test stream"
    echo "  $0 test"
    echo ""
    echo -e "${CYAN}Part of the Sovereignty Architecture™ - Mobile Node Pipeline${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
main() {
    local command="${1:-help}"
    
    case "$command" in
        start)
            show_banner
            validate_dependencies
            validate_stream_key
            validate_directories
            load_protected_playlist
            
            local queue_output
            queue_output=$(load_queue) || {
                log_error "No files in queue. Add videos to $QUEUE_DIR"
                exit 1
            }
            
            local concat_file
            concat_file=$(generate_concat_file "$queue_output") || {
                log_error "Failed to generate concat file"
                exit 1
            }
            
            start_stream "$concat_file"
            ;;
        stream)
            show_banner
            validate_dependencies
            validate_stream_key
            
            local video_file="${2:-}"
            if [[ -z "$video_file" ]]; then
                log_error "No video file specified"
                log_info "Usage: $0 stream <video_file>"
                exit 1
            fi
            
            stream_single_file "$video_file"
            ;;
        test)
            show_banner
            validate_dependencies
            validate_stream_key
            validate_directories
            
            stream_test_pattern
            ;;
        status)
            show_banner
            validate_directories
            show_status
            ;;
        queue)
            show_banner
            validate_directories
            log "Files in queue:"
            load_queue | while read -r file; do
                echo -e "  ${CYAN}→${NC} $file"
            done
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main with all arguments
main "$@"
