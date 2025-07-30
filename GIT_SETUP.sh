#!/bin/bash

# Initialize git repository
git init

# Add all project files
git add .

# Commit with a meaningful message
git commit -m "Initial commit of Tehi: Emergent AI Field"

# Set the default branch name
git branch -M main

# Add your GitHub repository (final version with .git)
git remote add origin https://github.com/ATKmxy/tehi.git

# Push to GitHub
git push -u origin main

echo "✅ Tehi_Project uploaded successfully!"
