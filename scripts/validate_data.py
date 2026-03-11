#!/usr/bin/env python3
"""
JoSAA Data Validation Script
Validates downloaded CSVs for quality and completeness
"""

import os
import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List

# ===== ANSI COLOR CODES =====
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_success(msg):
    print(f"{GREEN}✅  {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌  {msg}{RESET}")

def print_info(msg):
    print(f"{BOLD}ℹ️  {msg}{RESET}")

# ===== VALIDATION FUNCTIONS =====

def validate_dataframe(df: pd.DataFrame, filename: str) -> Dict:
    """Validate a single dataframe"""
    issues = []
    
    # Check required columns
    required_cols = ['Institute', 'Program', 'Opening_Rank', 'Closing_Rank']
    for col in required_cols:
        if col not in df.columns:
            # Try alternative names
            alt_names = {
                'Institute': ['institute_name', 'institute'],
                'Program': ['program_name', 'program'],
                'Opening_Rank': ['opening_rank', 'Opening Rank'],
                'Closing_Rank': ['closing_rank', 'Closing Rank'],
            }
            found = False
            for alt in alt_names.get(col, []):
                if alt in df.columns:
                    found = True
                    break
            
            if not found:
                issues.append(f"Missing column: {col}")
    
    # Check for nulls
    null_cols = df.isnull().sum()
    for col, count in null_cols.items():
        if count > 0:
            issues.append(f"Found {count} null values in {col}")
    
    # Check rank order (opening <= closing)
    if 'Opening_Rank' in df.columns and 'Closing_Rank' in df.columns:
        violations = (df['Opening_Rank'] > df['Closing_Rank']).sum()
        if violations > 0:
            issues.append(f"{violations} rows with Opening_Rank > Closing_Rank")
    
    # Check for duplicates (within same year/round/category)
    dup_cols = ['Institute', 'Program', 'Category', 'Seat_Pool']
    available_dup_cols = [col for col in dup_cols if col in df.columns]
    if available_dup_cols:
        duplicates = df.duplicated(subset=available_dup_cols, keep=False).sum()
        if duplicates > 0:
            issues.append(f"{duplicates} duplicate rows")
    
    return {
        'filename': filename,
        'rows': len(df),
        'columns': df.shape[1],
        'issues': issues,
        'valid': len(issues) == 0
    }

def validate_all_data():
    """Validate all downloaded data files"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data')
    
    print_info("Starting data validation...")
    print("="*60)
    
    csv_files = sorted(Path(data_dir).glob('josaa_*.csv'))
    
    if not csv_files:
        print_error(f"No CSV files found in {data_dir}")
        return
    
    results = []
    total_rows = 0
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            total_rows += len(df)
            
            result = validate_dataframe(df, csv_file.name)
            results.append(result)
            
            if result['valid']:
                print_success(f"{result['filename']}: {result['rows']} rows")
            else:
                print_warning(f"{result['filename']}: {result['rows']} rows")
                for issue in result['issues']:
                    print(f"    • {issue}")
        
        except Exception as e:
            print_error(f"Failed to read {csv_file.name}: {e}")
            results.append({
                'filename': csv_file.name,
                'rows': 0,
                'valid': False,
                'issues': [str(e)]
            })
    
    # Print summary
    print("\n" + "="*60)
    print_info("VALIDATION SUMMARY")
    print("="*60)
    
    valid_files = sum(1 for r in results if r['valid'])
    total_files = len(results)
    
    print(f"Valid files: {valid_files}/{total_files}")
    print(f"Total rows: {total_rows:,}")
    
    if valid_files == total_files:
        print_success("All files validated successfully!")
    else:
        print_warning(f"{total_files - valid_files} file(s) have issues")
    
    print("="*60 + "\n")
    
    # Check coverage by year
    coverage = {}
    for result in results:
        if 'josaa_' in result['filename']:
            year = result['filename'].split('_')[1]
            if year not in coverage:
                coverage[year] = []
            coverage[year].append(result['filename'])
    
    if coverage:
        print_info("YEAR/ROUND COVERAGE")
        print("="*60)
        for year in sorted(coverage.keys()):
            files = coverage[year]
            rounds = sorted([int(f.split('round')[1].replace('.csv', '')) for f in files if 'round' in f])
            if rounds:
                print(f"Year {year}: Rounds {min(rounds)}-{max(rounds)} ({len(rounds)} files)")
            else:
                print(f"Year {year}: {len(files)} file(s)")
        print("="*60 + "\n")

if __name__ == "__main__":
    validate_all_data()
