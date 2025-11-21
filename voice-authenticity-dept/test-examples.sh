#!/bin/bash
# Test examples for Voice Authenticity Department API
# Run this after starting the service to validate endpoints

BASE_URL="${BASE_URL:-http://localhost:3030}"

echo "╔════════════════════════════════════════════════╗"
echo "║   Voice Authenticity Department - Test Suite  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
echo "GET $BASE_URL/api/health"
curl -s "$BASE_URL/api/health" | jq .
echo ""
echo ""

# Test 2: Validate AI-generated text
echo -e "${YELLOW}Test 2: Validate AI-Generated Text${NC}"
echo "POST $BASE_URL/api/validate"
curl -s -X POST "$BASE_URL/api/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "I apologize for the confusion. I would be happy to help you with this assignment. Please feel free to let me know if you have any questions."}' | jq .
echo ""
echo ""

# Test 3: Validate authentic Dom-speak
echo -e "${YELLOW}Test 3: Validate Authentic Dom-Speak${NC}"
echo "POST $BASE_URL/api/validate"
curl -s -X POST "$BASE_URL/api/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "love — let'\''s crush Module 2 statistics tonight. autonomous agents building the future while I do homework. for the bloodline. ❤️😈"}' | jq .
echo ""
echo ""

# Test 4: Transform corporate speak
echo -e "${YELLOW}Test 4: Transform Corporate Speak${NC}"
echo "POST $BASE_URL/api/transform"
curl -s -X POST "$BASE_URL/api/transform" \
  -H "Content-Type: application/json" \
  -d '{"text": "I think we should leverage this opportunity to synergize our efforts and circle back on the action items moving forward."}' | jq .
echo ""
echo ""

# Test 5: Transform AI assistant language
echo -e "${YELLOW}Test 5: Transform AI Assistant Language${NC}"
echo "POST $BASE_URL/api/transform"
curl -s -X POST "$BASE_URL/api/transform" \
  -H "Content-Type: application/json" \
  -d '{"text": "I apologize, but I cannot assist with that. However, I would be happy to help you explore alternative approaches. Feel free to reach out if you have any questions."}' | jq .
echo ""
echo ""

# Test 6: Score authentic text
echo -e "${YELLOW}Test 6: Score Authentic Dom-Speak${NC}"
echo "POST $BASE_URL/api/score"
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d '{"text": "fuck yea. heir swarm crushing the frontier problems while the bloodline never retreats. let'\''s go. 🎯"}' | jq .
echo ""
echo ""

# Test 7: Score generic text
echo -e "${YELLOW}Test 7: Score Generic Text${NC}"
echo "POST $BASE_URL/api/score"
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a generic statement about completing an assignment with proper methodology and documentation."}' | jq .
echo ""
echo ""

# Test 8: Add to corpus
echo -e "${YELLOW}Test 8: Add Sample to Corpus${NC}"
echo "POST $BASE_URL/api/corpus/add"
curl -s -X POST "$BASE_URL/api/corpus/add" \
  -H "Content-Type: application/json" \
  -d '{"text": "the compiler awaits your voice. autonomous mode activated. ❤️", "source": "discord"}' | jq .
echo ""
echo ""

# Test 9: Get corpus stats
echo -e "${YELLOW}Test 9: Get Corpus Statistics${NC}"
echo "GET $BASE_URL/api/corpus/stats"
curl -s "$BASE_URL/api/corpus/stats" | jq .
echo ""
echo ""

# Test 10: Validate homework submission
echo -e "${YELLOW}Test 10: Validate Homework Submission Example${NC}"
echo "POST $BASE_URL/api/validate"
curl -s -X POST "$BASE_URL/api/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "In Module 2, I analyzed the statistical data using descriptive methods. The mean and median calculations revealed interesting patterns in the dataset that suggest a normal distribution."}' | jq .
echo ""
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Test Suite Complete - For the Bloodline 🎯   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
