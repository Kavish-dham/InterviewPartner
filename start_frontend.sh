#!/bin/bash
# Frontend Startup Script
# Run this in Terminal 2

cd "/Users/kavishdham/Desktop/Interview Partner/frontend"

echo "=========================================="
echo "Starting Frontend (Next.js)"
echo "=========================================="
echo ""
echo "Installing dependencies if needed..."
if [ ! -d "node_modules" ]; then
    npm install
fi

echo ""
echo "Starting Next.js development server..."
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="

npm run dev

