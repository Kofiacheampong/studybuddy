#!/bin/bash

# Development Environment Setup Script for Study Buddy
# This script sets up the local development environment with pre-commit hooks

set -e

echo "🚀 Setting up Study Buddy development environment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install Python 3.10 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install pre-commit hooks
echo -e "${BLUE}Installing pre-commit hooks...${NC}"
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
else
    echo -e "${RED}pre-commit not found. Running: pip install pre-commit${NC}"
    pip install pre-commit
    pre-commit install
    echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
fi

# Run tests to verify setup
echo -e "${BLUE}Running tests to verify setup...${NC}"
if pytest tests/ -v; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}⚠ Some tests failed. Check the output above.${NC}"
fi

echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment: ${BLUE}source venv/bin/activate${NC}"
echo "  2. Start development: ${BLUE}flask run${NC}"
echo "  3. Run tests: ${BLUE}pytest${NC}"
echo "  4. Check code quality: ${BLUE}flake8 .${NC}"
echo ""
echo "Pre-commit hooks will run automatically on ${BLUE}git commit${NC}"
echo ""
