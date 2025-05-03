#!/usr/bin/env bash

cd "$(dirname "$0")"

echo "🧹 Cleaning project..."

# remove __pycache__ folders
echo "🔍 Searching for __pycache__ folders..."
find . -type d -name '__pycache__' -print -exec rm -rf {} +
echo "✅ Removed all __pycache__ folders."

# remove *.egg-info directories or files
echo "🔍 Searching for *.egg-info files or folders..."
find . -name '*.egg-info' -print -exec rm -rf {} +
echo "✅ Removed all *.egg-info files/folders."

# remove user-created folders
for folder in tonic/images tonic/models tonic/predicted tonic/datasets; do
  if [ -d "$folder" ]; then
    rm -rf "$folder"
    echo "🗑️  Removed $folder"
  else
    echo "ℹ️  $folder not found, skipping."
  fi
done

echo "✅ Cleanup complete."
