#!/bin/bash
# Import all guides from the knowledge repo

cd "$(dirname "$0")/.." || exit 1

knowledge_repo="../knowledge/initiatives"

for file in "$knowledge_repo"/*/outputs/*-edited.md; do
  if [ -f "$file" ]; then
    echo "Processing: $(basename "$file")"
    python3 scripts/add-guide.py "$file"
    echo "---"
  fi
done

echo ""
echo "All guides imported!"
echo ""
echo "Next steps:"
echo "  npm start                    # Preview site"
echo "  git add guides/"
echo "  git commit -m 'Import all guides from knowledge repo'"
echo "  git push"
