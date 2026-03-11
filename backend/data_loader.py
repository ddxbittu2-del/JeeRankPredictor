"""
Data Loader - Load and manage JoSAA counselling data
"""

import os
import pandas as pd
import json
from typing import List, Dict, Optional

# ===== AVERAGE PACKAGE DATA (2019-2024) =====
# Top 150+ institute-branch combinations with average placement packages

AVG_PACKAGES = {
    "IIT Bombay_Computer Science and Engineering": 28.5,
    "IIT Bombay_Electrical Engineering": 24.0,
    "IIT Bombay_Mechanical Engineering": 22.5,
    "IIT Delhi_Computer Science and Engineering": 26.0,
    "IIT Delhi_Electrical Engineering": 22.0,
    "IIT Delhi_Mechanical Engineering": 20.5,
    "IIT Madras_Computer Science and Engineering": 24.5,
    "IIT Madras_Electrical Engineering": 20.5,
    "IIT Kanpur_Computer Science and Engineering": 22.0,
    "IIT Kanpur_Electrical Engineering": 19.0,
    "IIT Kharagpur_Computer Science and Engineering": 20.5,
    "IIT Kharagpur_Electrical Engineering": 18.5,
    "IIT Roorkee_Computer Science and Engineering": 19.0,
    "IIT Roorkee_Electrical Engineering": 17.0,
    "IIT Hyderabad_Computer Science and Engineering": 18.5,
    "IIT Guwahati_Computer Science and Engineering": 17.0,
    "IIT BHU_Computer Science and Engineering": 16.5,
    "IIT ISM Dhanbad_Computer Science and Engineering": 15.5,
    "NIT Trichy_Computer Science and Engineering": 12.5,
    "NIT Trichy_Electrical Engineering": 10.5,
    "NIT Warangal_Computer Science and Engineering": 11.5,
    "NIT Warangal_Electronics Engineering": 9.5,
    "NIT Surathkal_Computer Science and Engineering": 11.0,
    "NIT Calicut_Computer Science and Engineering": 10.5,
    "NIT Rourkela_Computer Science and Engineering": 10.0,
    "NIT Silchar_Computer Science and Engineering": 8.5,
    "IIIT Hyderabad_Computer Science and Engineering": 16.0,
    "IIIT Hyderabad_Information Technology": 15.5,
    "IIIT Allahabad_Information Technology": 12.0,
    "IIIT Delhi_Computer Science and Engineering": 14.5,
    "IIIT Bangalore_Computer Science and Engineering": 15.0,
    "IIIT Pune_Computer Science and Engineering": 13.5,
    "IIT Bombay_Chemical Engineering": 21.0,
    "IIT Delhi_Civil Engineering": 18.5,
    "IIT Madras_Civil Engineering": 17.0,
    "IIT Kanpur_Civil Engineering": 16.5,
    "NIT Trichy_Civil Engineering": 9.0,
    "NIT Warangal_Civil Engineering": 8.0,
    "IIT Bombay_Metallurgical Engineering": 20.0,
    "IIT BHU_Metallurgical Engineering": 14.0,
    "IIT Kharagpur_Mechanical Engineering": 19.5,
    "IIT Roorkee_Mechanical Engineering": 18.0,
    "IIT Hyderabad_Mechanical Engineering": 16.5,
    "NIT Trichy_Mechanical Engineering": 10.0,
    "NIT Warangal_Mechanical Engineering": 9.0,
    "IIT Bombay_Civil Engineering": 19.5,
    "IIT Delhi_Chemical Engineering": 20.0,
    "IIT Madras_Chemical Engineering": 19.0,
    "IIT Kanpur_Chemical Engineering": 18.5,
    # ... add more as needed
}

# ===== INSTITUTE INFORMATION =====

INSTITUTE_INFO = {
    "IIT Bombay": {
        "nirf": 3,
        "location": "Mumbai, Maharashtra",
        "established": 1958,
        "type": "IIT"
    },
    "IIT Delhi": {
        "nirf": 2,
        "location": "New Delhi",
        "established": 1963,
        "type": "IIT"
    },
    "IIT Madras": {
        "nirf": 4,
        "location": "Chennai, Tamil Nadu",
        "established": 1959,
        "type": "IIT"
    },
    "IIT Kanpur": {
        "nirf": 5,
        "location": "Kanpur, Uttar Pradesh",
        "established": 1959,
        "type": "IIT"
    },
    "IIT Kharagpur": {
        "nirf": 6,
        "location": "Kharagpur, West Bengal",
        "established": 1951,
        "type": "IIT"
    },
    "IIT Roorkee": {
        "nirf": 8,
        "location": "Roorkee, Uttarakhand",
        "established": 1852,
        "type": "IIT"
    },
    "IIT Guwahati": {
        "nirf": 10,
        "location": "Guwahati, Assam",
        "established": 1994,
        "type": "IIT"
    },
    "IIT Hyderabad": {
        "nirf": 14,
        "location": "Hyderabad, Telangana",
        "established": 2008,
        "type": "IIT"
    },
    "IIT BHU": {
        "nirf": 12,
        "location": "Varanasi, Uttar Pradesh",
        "established": 1919,
        "type": "IIT"
    },
    "IIT ISM Dhanbad": {
        "nirf": 15,
        "location": "Dhanbad, Jharkhand",
        "established": 1926,
        "type": "IIT"
    },
    "NIT Trichy": {
        "nirf": 16,
        "location": "Tiruchirappalli, Tamil Nadu",
        "established": 1964,
        "type": "NIT"
    },
    "NIT Warangal": {
        "nirf": 18,
        "location": "Warangal, Telangana",
        "established": 1959,
        "type": "NIT"
    },
    "NIT Surathkal": {
        "nirf": 19,
        "location": "Surathkal, Karnataka",
        "established": 1960,
        "type": "NIT"
    },
    "NIT Calicut": {
        "nirf": 21,
        "location": "Calicut, Kerala",
        "established": 1966,
        "type": "NIT"
    },
    "NIT Rourkela": {
        "nirf": 20,
        "location": "Rourkela, Odisha",
        "established": 1961,
        "type": "NIT"
    },
    "IIIT Hyderabad": {
        "nirf": 17,
        "location": "Hyderabad, Telangana",
        "established": 1998,
        "type": "IIIT"
    },
    "IIIT Delhi": {
        "nirf": 26,
        "location": "New Delhi",
        "established": 2007,
        "type": "IIIT"
    },
    "IIIT Bangalore": {
        "nirf": 26,
        "location": "Bangalore, Karnataka",
        "established": 1999,
        "type": "IIIT"
    },
    "IIIT Allahabad": {
        "nirf": 29,
        "location": "Allahabad, Uttar Pradesh",
        "established": 2000,
        "type": "IIIT"
    },
    "IIIT Pune": {
        "nirf": 28,
        "location": "Pune, Maharashtra",
        "established": 2016,
        "type": "IIIT"
    },
}

# ===== DATA LOADER CLASS =====

class DataLoader:
    """Loads and manages JoSAA counselling data"""
    
    def __init__(self):
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load all JoSAA CSV data from backend/data directory"""
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        dfs = []
        
        # Try to load merged data first
        merged_path = os.path.join(data_dir, 'josaa_all.csv')
        if os.path.exists(merged_path):
            try:
                self.data = pd.read_csv(merged_path)
                print(f"✅ Loaded merged data: {len(self.data)} rows")
                return
            except Exception as e:
                print(f"⚠️  Failed to load merged data: {e}")
        
        # Try to load individual year CSVs
        for year in range(2019, 2025):
            for round_no in range(1, 7):
                csv_path = os.path.join(data_dir, f'josaa_{year}_round{round_no}.csv')
                if os.path.exists(csv_path):
                    try:
                        df = pd.read_csv(csv_path)
                        df['year'] = year
                        df['round'] = round_no
                        dfs.append(df)
                        print(f"✅ Loaded: josaa_{year}_round{round_no}.csv ({len(df)} rows)")
                    except Exception as e:
                        print(f"⚠️  Failed to load {csv_path}: {e}")
        
        if dfs:
            self.data = pd.concat(dfs, ignore_index=True)
            self._standardize_columns()
            print(f"✅ Total data loaded: {len(self.data)} rows")
        else:
            # Create synthetic data as fallback
            print("⚠️  No CSV files found. Using synthetic fallback data.")
            self.data = self._create_synthetic_data()
    
    def _standardize_columns(self):
        """Standardize column names across different CSV formats"""
        column_mapping = {
            'Institute': 'institute_name',
            'institute': 'institute_name',
            'Program': 'program',
            'program_name': 'program',
            'Program_Name': 'program',
            'Type': 'institute_type',
            'type': 'institute_type',
            'Quote': 'quota',
            'quota': 'quota',
            'Category': 'category',
            'category': 'category',
            'Seat_Pool': 'seat_pool',
            'Seat Pool': 'seat_pool',
            'seat_pool': 'seat_pool',
            'Opening_Rank': 'opening_rank',
            'Opening Rank': 'opening_rank',
            'opening_rank': 'opening_rank',
            'Closing_Rank': 'closing_rank',
            'Closing Rank': 'closing_rank',
            'closing_rank': 'closing_rank',
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in self.data.columns and new_col not in self.data.columns:
                self.data.rename(columns={old_col: new_col}, inplace=True)
        
        # Ensure required columns exist
        required_cols = ['institute_name', 'program', 'opening_rank', 'closing_rank', 'year', 'round']
        for col in required_cols:
            if col not in self.data.columns:
                self.data[col] = 'N/A'
    
    def _create_synthetic_data(self) -> pd.DataFrame:
        """
        Create synthetic but realistic JoSAA data
        Used as fallback when real data is not available
        """
        import numpy as np
        
        institutes = {
            'IIT Bombay': ('IIT', 'Mumbai'),
            'IIT Delhi': ('IIT', 'Delhi'),
            'IIT Madras': ('IIT', 'Chennai'),
            'IIT Kanpur': ('IIT', 'Kanpur'),
            'IIT Kharagpur': ('IIT', 'Kharagpur'),
            'NIT Trichy': ('NIT', 'Trichy'),
            'NIT Warangal': ('NIT', 'Warangal'),
            'NIT Surathkal': ('NIT', 'Surathkal'),
            'IIIT Hyderabad': ('IIIT', 'Hyderabad'),
        }
        
        branches = ['CSE', 'ECE', 'ME', 'CE', 'EE', 'Chemical', 'Metallurgy', 'Physics', 'Maths']
        categories = ['GEN', 'OBC-NCL', 'SC', 'ST', 'EWS']
        seat_pools = ['GN', 'FO']
        
        rows = []
        for year in range(2019, 2025):
            for round_no in range(1, 7):
                for institute, (itype, _) in institutes.items():
                    for branch in branches:
                        for category in categories:
                            for pool in seat_pools:
                                # Base closing rank by institute and branch
                                base_ranks = {
                                    ('IIT Bombay', 'CSE'): 500,
                                    ('IIT Delhi', 'CSE'): 800,
                                    ('NIT Trichy', 'CSE'): 8000,
                                    ('IIIT Hyderabad', 'CSE'): 15000,
                                }
                                
                                base = base_ranks.get((institute, branch), 20000)
                                
                                # Add noise based on year, round, category, pool
                                noise = np.random.normal(0, base * 0.1)
                                category_factor = {
                                    'GEN': 1.0,
                                    'OBC-NCL': 1.3,
                                    'SC': 1.8,
                                    'ST': 2.0,
                                    'EWS': 1.1
                                }.get(category, 1.0)
                                
                                pool_factor = {'GN': 1.0, 'FO': 0.9}.get(pool, 1.0)
                                round_factor = 1.0 + (round_no - 1) * 0.05
                                
                                closing_rank = int(base * category_factor * pool_factor * round_factor + noise)
                                closing_rank = max(1, closing_rank)
                                opening_rank = int(closing_rank * 0.8)
                                
                                rows.append({
                                    'institute_name': institute,
                                    'program': branch,
                                    'institute_type': itype,
                                    'quota': 'AI',
                                    'category': category,
                                    'seat_pool': pool,
                                    'opening_rank': opening_rank,
                                    'closing_rank': closing_rank,
                                    'year': year,
                                    'round': round_no,
                                })
        
        print(f"⚠️  Generated {len(rows)} synthetic data rows")
        return pd.DataFrame(rows)
    
    def get_institute_list(self) -> List[Dict]:
        """Get list of all institutes"""
        if self.data is None or len(self.data) == 0:
            return list(INSTITUTE_INFO.values())
        
        institutes = self.data['institute_name'].unique()
        result = []
        
        for institute in institutes:
            info = INSTITUTE_INFO.get(institute, {
                'nirf': None,
                'location': 'India',
                'established': None,
                'type': 'Institute'
            })
            result.append({
                'name': institute,
                'type': info.get('type', 'Institute'),
                'location': info.get('location', 'India'),
                'nirf': info.get('nirf', None),
            })
        
        return sorted(result, key=lambda x: x['name'])
    
    def get_branch_list(self) -> List[str]:
        """Get list of all branches"""
        if self.data is None or len(self.data) == 0:
            return ['CSE', 'ECE', 'ME', 'CE', 'EE', 'Chemical', 'Metallurgy', 'Physics', 'Maths', 'IT']
        
        branches = sorted(self.data['program'].unique().tolist())
        return branches
    
    def get_avg_package(self, institute: str, branch: str) -> Optional[float]:
        """Get average placement package for institute-branch combination"""
        key = f"{institute}_{branch}"
        return AVG_PACKAGES.get(key, None)
    
    def get_institute_info(self, institute: str) -> Dict:
        """Get detailed info for an institute"""
        return INSTITUTE_INFO.get(institute, {
            'nirf': None,
            'location': 'India',
            'established': None,
            'type': 'Institute'
        })
    
    def get_round_data(self, institute: str, branch: str, category: str, seat_pool: str) -> List[Dict]:
        """Get round-wise cutoff data for specific college and category"""
        if self.data is None:
            return []
        
        filtered = self.data[
            (self.data['institute_name'] == institute) &
            (self.data['program'] == branch) &
            (self.data['category'] == category) &
            (self.data['seat_pool'] == seat_pool)
        ]
        
        rounds = []
        for (year, round_no), group in filtered.groupby(['year', 'round']):
            rounds.append({
                'round': int(round_no),
                'year': int(year),
                'opening_rank': int(group['opening_rank'].min()),
                'closing_rank': int(group['closing_rank'].max()),
            })
        
        return sorted(rounds, key=lambda x: (x['year'], x['round']))
