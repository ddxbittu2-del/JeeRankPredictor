#!/usr/bin/env python3
"""
JoSAA Data Download Script
Automated download from multiple sources with fallback strategies
"""

import os
import sys
import json
import time
import requests
import pandas as pd
import zipfile
import io
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import subprocess

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

# ===== CONFIGURATION =====
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data')
TIMEOUT = 10

# ===== STRATEGY 1: DIRECT JoSAA URLs =====

def download_from_josaa(year: int, round_no: int) -> Optional[pd.DataFrame]:
    """Try downloading from official JoSAA website"""
    print_info(f"Trying JoSAA direct URL for {year} Round {round_no}...")
    
    # Try multiple URL patterns
    urls = [
        f"https://josaa.nic.in/webinfocms/api/getfile?FileName=OR{year}R{round_no}.xlsx",
        f"https://josaa.nic.in/webinfocms/api/getfile?FileName=CR{year}R{round_no}.xlsx",
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                # Try to read as Excel
                try:
                    df = pd.read_excel(io.BytesIO(response.content))
                    print_success(f"Downloaded from JoSAA: {year} Round {round_no}")
                    return df
                except:
                    pass
        except Exception as e:
            pass
    
    return None

# ===== STRATEGY 2: GITHUB MIRRORS =====

def download_from_github(year: int, round_no: int) -> Optional[pd.DataFrame]:
    """Try downloading from GitHub mirrors"""
    print_info(f"Trying GitHub mirrors for {year} Round {round_no}...")
    
    repos = [
        f"https://raw.githubusercontent.com/nitk-nest/JoSAA-Data/main/data/{year}/Round{round_no}.csv",
        f"https://raw.githubusercontent.com/amankumarjain/josaa-data/main/{year}_round{round_no}.csv",
        f"https://raw.githubusercontent.com/deedy/india-college-data/master/josaa/{year}.csv",
    ]
    
    for url in repos:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                print_success(f"Downloaded from GitHub: {year} Round {round_no}")
                return df
        except Exception as e:
            pass
    
    return None

# ===== STRATEGY 3: DATA.GOV.IN API =====

def download_from_datagov() -> Optional[pd.DataFrame]:
    """Try downloading from data.gov.in"""
    print_info("Trying data.gov.in API...")
    
    try:
        api_key = "579b464db66ec23bdd0000015ef30099f2f44f2e9ce6bc9bdf5a"
        endpoint = "https://data.gov.in/api/datastore/resource.json"
        
        params = {
            "resource_id": "josaa-opening-closing-ranks",
            "api-key": api_key,
            "limit": 10000
        }
        
        response = requests.get(endpoint, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            if records:
                df = pd.DataFrame(records)
                print_success(f"Downloaded from data.gov.in ({len(records)} records)")
                return df
    except Exception as e:
        pass
    
    return None

# ===== STRATEGY 4: KAGGLE CLI =====

def download_from_kaggle() -> Optional[pd.DataFrame]:
    """Try downloading using Kaggle CLI"""
    print_info("Checking Kaggle CLI...")
    
    try:
        # Check if kaggle is installed
        result = subprocess.run(["kaggle", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print_warning("Kaggle CLI not installed")
            print_info("Install via: pip install kaggle")
            return None
        
        print_success("Kaggle CLI found")
        
        # Try to download datasets
        datasets = [
            "ranitsaha/jee-josaa-college-predictor",
            "ayushsoni1010/josaa-2023-counselling-dataset",
        ]
        
        for dataset in datasets:
            try:
                print_info(f"Downloading {dataset}...")
                subprocess.run(
                    ["kaggle", "datasets", "download", "-d", dataset],
                    cwd=DATA_DIR,
                    capture_output=True
                )
                
                # Find and extract ZIP
                for file in os.listdir(DATA_DIR):
                    if file.endswith('.zip'):
                        zip_path = os.path.join(DATA_DIR, file)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(DATA_DIR)
                        os.remove(zip_path)
                        print_success(f"Extracted {dataset}")
                        return True
            except Exception as e:
                pass
        
        return None
    except Exception as e:
        print_warning(f"Kaggle download failed: {e}")
        return None

# ===== STRATEGY 5: SYNTHETIC DATA FALLBACK =====

def generate_synthetic_data() -> pd.DataFrame:
    """Generate realistic synthetic JoSAA data"""
    import numpy as np
    
    print_warning("Generating synthetic JoSAA data...")
    
    institutes = {
        'IIT Bombay': ('IIT', 600),
        'IIT Delhi': ('IIT', 1000),
        'IIT Madras': ('IIT', 1200),
        'IIT Kanpur': ('IIT', 1500),
        'IIT Kharagpur': ('IIT', 1800),
        'IIT Roorkee': ('IIT', 2500),
        'IIT Guwahati': ('IIT', 4000),
        'IIT BHU': ('IIT', 5000),
        'IIT Hyderabad': ('IIT', 5500),
        'IIT ISM Dhanbad': ('IIT', 8000),
        'NIT Trichy': ('NIT', 8000),
        'NIT Warangal': ('NIT', 12000),
        'NIT Surathkal': ('NIT', 15000),
        'NIT Calicut': ('NIT', 18000),
        'NIT Rourkela': ('NIT', 20000),
        'IIIT Hyderabad': ('IIIT', 18000),
        'IIIT Delhi': ('IIIT', 25000),
        'IIIT Bangalore': ('IIIT', 22000),
    }
    
    branches = ['CSE', 'ECE', 'ME', 'CE', 'EE', 'Chemical', 'Metallurgy', 'Physics', 'Maths']
    categories = ['GEN', 'OBC-NCL', 'SC', 'ST', 'EWS']
    seat_pools = ['GN', 'FO']
    
    rows = []
    for year in range(2019, 2025):
        for round_no in range(1, 7):
            for inst, (itype, base_rank) in institutes.items():
                for branch in branches:
                    for category in categories:
                        for pool in seat_pools:
                            # Add realistic variation
                            cat_mult = {
                                'GEN': 1.0,
                                'OBC-NCL': 1.2,
                                'SC': 1.6,
                                'ST': 1.8,
                                'EWS': 1.05
                            }[category]
                            
                            pool_mult = 1.0 if pool == 'GN' else 0.85
                            round_mult = 1.0 + (round_no - 1) * 0.08
                            branch_mult = 1.0 if branch == 'CSE' else np.random.uniform(1.1, 2.0)
                            
                            noise = np.random.normal(1.0, 0.1)
                            closing_rank = int(base_rank * cat_mult * pool_mult * round_mult * branch_mult * noise)
                            opening_rank = int(closing_rank * 0.75)
                            
                            rows.append({
                                'Institute': inst,
                                'Program': branch,
                                'Type': itype,
                                'Quote': 'AI',
                                'Category': category,
                                'Seat_Pool': pool,
                                'Opening_Rank': opening_rank,
                                'Closing_Rank': closing_rank,
                                'Year': year,
                                'Round': round_no,
                            })
    
    df = pd.DataFrame(rows)
    print_success(f"Generated {len(df)} synthetic data rows")
    return df

# ===== MAIN DOWNLOAD FUNCTION =====

def download_all_data(
    years: list = None,
    rounds: list = None,
    source: str = None,
    synthetic_only: bool = False,
    validate_only: bool = False
):
    """
    Main function to download JoSAA data
    
    Args:
        years: List of years to download (default: 2019-2024)
        rounds: List of rounds to download (default: 1-6)
        source: Specific source (josaa, github, datagov, kaggle, synthetic)
        synthetic_only: Skip to synthetic data immediately
        validate_only: Only validate existing files
    """
    if years is None:
        years = [2019, 2020, 2021, 2022, 2023, 2024]
    if rounds is None:
        rounds = [1, 2, 3, 4, 5, 6]
    
    # Create data directory
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if validate_only:
        validate_downloaded_data()
        return
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'years': years,
        'downloads': {}
    }
    
    all_dfs = []
    
    if synthetic_only:
        print_warning("Skipping downloads, using synthetic data only")
        all_dfs.append(generate_synthetic_data())
    else:
        # Try to download for each year and round
        for year in years:
            for round_no in rounds:
                df = None
                strategy_used = None
                
                try:
                    # Strategy selection
                    if source == 'josaa':
                        df = download_from_josaa(year, round_no)
                        strategy_used = 'josaa'
                    elif source == 'github':
                        df = download_from_github(year, round_no)
                        strategy_used = 'github'
                    elif source == 'datagov':
                        df = download_from_datagov()
                        strategy_used = 'datagov'
                    elif source == 'kaggle':
                        download_from_kaggle()
                        strategy_used = 'kaggle'
                    else:
                        # Auto-select best strategy
                        for strategy in [download_from_josaa, download_from_github, download_from_datagov]:
                            df = strategy(year, round_no)
                            if df is not None:
                                strategy_used = strategy.__name__
                                break
                    
                    if df is not None:
                        all_dfs.append(df)
                        report['downloads'][f"{year}_r{round_no}"] = {
                            'status': 'success',
                            'strategy': strategy_used,
                            'rows': len(df)
                        }
                    else:
                        report['downloads'][f"{year}_r{round_no}"] = {
                            'status': 'failed',
                            'strategy': strategy_used
                        }
                        print_warning(f"Could not download {year} Round {round_no}")
                
                except Exception as e:
                    print_error(f"Error downloading {year} Round {round_no}: {e}")
                    report['downloads'][f"{year}_r{round_no}"] = {
                        'status': 'error',
                        'error': str(e)
                    }
        
        # If no data was downloaded, use synthetic fallback
        if not all_dfs:
            all_dfs.append(generate_synthetic_data())
            report['fallback'] = 'synthetic'
    
    # Merge all data
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        
        # Save merged CSV
        merged_path = os.path.join(DATA_DIR, 'josaa_all.csv')
        merged_df.to_csv(merged_path, index=False)
        print_success(f"Merged data saved: {merged_path} ({len(merged_df)} rows)")
        
        # Save report
        report_path = os.path.join(DATA_DIR, 'download_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print_success(f"Report saved: {report_path}")
        
        # Print summary
        print("\n" + "="*50)
        print_info("DOWNLOAD SUMMARY")
        print("="*50)
        print(f"Total rows: {len(merged_df)}")
        print(f"Years: {merged_df['Year'].unique() if 'Year' in merged_df.columns else 'Unknown'}")
        print(f"Save location: {DATA_DIR}")
        print("="*50 + "\n")

def validate_downloaded_data():
    """Validate downloaded data files"""
    print_info("Validating downloaded data...")
    
    csv_files = list(Path(DATA_DIR).glob('josaa_*.csv'))
    
    if not csv_files:
        print_error("No CSV files found in data directory")
        return
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print_success(f"{csv_file.name}: {len(df)} rows")
        except Exception as e:
            print_error(f"Failed to read {csv_file.name}: {e}")

# ===== CLI INTERFACE =====

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download JoSAA data")
    parser.add_argument("--year", type=int, help="Download specific year only")
    parser.add_argument("--round", type=int, help="Download specific round only")
    parser.add_argument("--source", choices=['josaa', 'github', 'datagov', 'kaggle', 'synthetic'],
                       help="Force specific download source")
    parser.add_argument("--synthetic", action="store_true", help="Generate synthetic data only")
    parser.add_argument("--validate", action="store_true", help="Validate downloaded files only")
    
    args = parser.parse_args()
    
    years = [args.year] if args.year else None
    rounds = [args.round] if args.round else None
    
    download_all_data(
        years=years,
        rounds=rounds,
        source=args.source,
        synthetic_only=args.synthetic,
        validate_only=args.validate
    )
