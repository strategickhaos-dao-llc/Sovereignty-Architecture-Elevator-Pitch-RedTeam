#!/bin/bash
# Script to collect CSS examples and related resources
# Created based on the curl commands provided in the issue

# Configuration
REQUEST_DELAY=0.5  # Delay between requests to be polite to servers

# Create directory for examples
mkdir -p examples/css_resources

# Change to repository root
cd "$(dirname "$0")" || exit

echo "🎯 Starting CSS examples collection..."
echo ""

# Define sources with unique output filenames
declare -a sources=(
  "transitive_web_css,https://www.the-transitive-web.com/v2/300/css.html,css_transitive_web.txt"
  "w3schools_css,https://www.w3schools.com/examples/examples_css.asp,css_w3schools.txt"
  "w3schools_math,https://www.w3schools.com/examples/examples_math.asp,math_w3schools.txt"
  "w3schools_programming,https://www.w3schools.com/examples/examples_programming.asp,programming_w3schools.txt"
  "w3schools_python,https://www.w3schools.com/examples/examples_python.asp,python_w3schools.txt"
  "linux_readme,https://raw.githubusercontent.com/torvalds/linux/master/README,linux_readme.txt"
)

count=0
success=0
failed=0
total=${#sources[@]}

for source in "${sources[@]}"; do
  count=$((count + 1))
  IFS=',' read -r id url file <<< "$source"
  echo "[$count/$total] Downloading $id..."
  
  if curl -L -s \
    --max-time 30 --retry 2 --retry-delay 1 \
    "$url" -o "examples/css_resources/$file"; then
    
    if [ -s "examples/css_resources/$file" ]; then
      size=$(stat -f%z "examples/css_resources/$file" 2>/dev/null || stat -c%s "examples/css_resources/$file")
      if [ "$size" -gt 100 ]; then
        echo "✅ Success: $file ($size bytes)"
        success=$((success + 1))
      else
        echo "⚠️  Warning: $file too small ($size bytes)"
        failed=$((failed + 1))
      fi
    else
      echo "❌ Failed: $file (empty)"
      failed=$((failed + 1))
    fi
  else
    echo "❌ Failed: $file (curl error)"
    failed=$((failed + 1))
  fi
  
  # Small delay between requests to be polite
  sleep "$REQUEST_DELAY"
done

echo ""
echo "🎯 COLLECTION COMPLETE:"
echo "Total sources: $total"
echo "Successful: $success"
echo "Failed: $failed"
if [ "$total" -gt 0 ]; then
  echo "Success rate: $(( success * 100 / total ))%"
fi
echo ""
echo "Files saved to: examples/css_resources/"
