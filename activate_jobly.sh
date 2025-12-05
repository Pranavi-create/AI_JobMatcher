#!/bin/bash
# Quick activation script for the jobly conda environment

source /opt/anaconda3/etc/profile.d/conda.sh
conda activate jobly

echo "✅ Activated jobly conda environment"
echo "Python: $(which python)"
echo "Version: $(python --version)"
echo ""
echo "You can now run:"
echo "  • cd linkedin_collector && python search_and_save.py"
echo "  • cd github_collector && python github_fetcher.py"
echo "  • python run_pipeline.py"
