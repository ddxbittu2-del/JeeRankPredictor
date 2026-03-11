"""
ML Predictor modules for rank and college predictions
"""

import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from typing import List, Dict, Optional

# ===== RANK PREDICTOR =====

class RankPredictor:
    """Predicts JEE rank from scores using gradient boosting"""
    
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load trained rank model from disk"""
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'rank_model.pkl')
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print("✅ Rank model loaded")
            except Exception as e:
                print(f"⚠️  Failed to load rank model: {e}")
                self.model = None
        else:
            print(f"⚠️  Rank model not found at {model_path}")
            self.model = None
    
    def predict(self, score: float, year: int = 2024, category: str = "GEN") -> Dict:
        """
        Predict rank from score
        
        Args:
            score: Student's score (0-300)
            year: Exam year
            category: Student category
        
        Returns:
            Dictionary with rank and percentile
        """
        from rank_formula import score_to_rank, rank_to_percentile, get_confidence_range
        
        # Use formula-based approach for immediate results
        rank = score_to_rank(score, year)
        percentile = rank_to_percentile(rank, year)
        confidence = get_confidence_range(rank)
        
        return {
            "predicted_rank": rank,
            "percentile": percentile,
            "confidence_range": confidence
        }

# ===== COLLEGE PREDICTOR =====

class CollegePredictor:
    """Predicts college admissions using random forest classification"""
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.data = None
        self.load_model()
    
    def load_model(self):
        """Load trained college model from disk"""
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'college_model.pkl')
        encoders_path = os.path.join(os.path.dirname(__file__), 'models', 'encoders.pkl')
        
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("✅ College model loaded")
            
            if os.path.exists(encoders_path):
                self.encoders = joblib.load(encoders_path)
                print("✅ Encoders loaded")
        except Exception as e:
            print(f"⚠️  Failed to load college model: {e}")
            self.model = None
            self.encoders = {}
    
    def predict(
        self,
        rank: int,
        category: str,
        seat_pool: str,
        home_state: str,
        institute_types: List[str],
        branches: List[str]
    ) -> List[Dict]:
        """
        Predict colleges where student can get admission
        
        Args:
            rank: Student's JEE rank
            category: Student category (GEN, OBC-NCL, SC, ST, EWS, etc.)
            seat_pool: 'GN' (Gender-Neutral) or 'FO' (Female-Only)
            home_state: Student's home state
            institute_types: List of institute types to consider (IIT, NIT, IIIT, GFTI, All)
            branches: List of preferred branches (CSE, ECE, ME, CE, EE, Chemical, Metallurgy, Physics, Maths, IT)
        
        Returns:
            List of colleges sorted by admission probability
        """
        # Load data
        from data_loader import DataLoader
        data_loader = DataLoader()
        
        # Filter data by institute type and branches
        filtered_data = data_loader.data.copy()
        
        if 'All' not in institute_types:
            filtered_data = filtered_data[filtered_data['institute_type'].isin(institute_types)]
        
        filtered_data = filtered_data[filtered_data['program'].isin(branches)]
        
        # Group by institute and program to get college entries
        colleges = []
        
        for (institute, program), group in filtered_data.groupby(['institute_name', 'program']):
            # Get the latest year data
            latest_data = group[group['year'] == group['year'].max()]
            
            # Get opening and closing ranks
            opening_rank = latest_data['opening_rank'].min()
            closing_rank = latest_data['closing_rank'].max()
            
            # Calculate admission probability
            probability = self._calculate_probability(rank, opening_rank, closing_rank)
            
            # Get average package
            avg_package = data_loader.get_avg_package(institute, program)
            
            # Get institute info
            institute_info = data_loader.get_institute_info(institute)
            
            # Get round-wise data
            rounds = []
            for (yr, rd), round_group in latest_data.groupby(['year', 'round']):
                rounds.append({
                    'round': int(rd),
                    'opening_rank': int(round_group['opening_rank'].min()),
                    'closing_rank': int(round_group['closing_rank'].max()),
                })
            
            colleges.append({
                'institute': institute,
                'program': program,
                'institute_type': latest_data['institute_type'].iloc[0],
                'quota': 'AI',  # All India quota
                'opening_rank': int(opening_rank),
                'closing_rank': int(closing_rank),
                'probability': probability,
                'avg_package_lpa': avg_package,
                'location': institute_info.get('location', 'N/A'),
                'nirf_rank': institute_info.get('nirf', None),
                'established': institute_info.get('established', None),
                'rounds': sorted(rounds, key=lambda x: x['round']),
            })
        
        # Sort by probability descending
        colleges.sort(key=lambda x: x['probability'], reverse=True)
        
        return colleges
    
    def _calculate_probability(self, student_rank: int, opening_rank: int, closing_rank: int) -> float:
        """
        Calculate admission probability using rule-based approach
        
        Based on official JoSAA data patterns:
        - If rank <= closing_rank * 0.9: ~90% probability
        - If rank <= closing_rank: ~70% probability
        - If rank <= closing_rank * 1.1: ~40% probability
        - If rank <= closing_rank * 1.3: ~15% probability
        - Otherwise: ~5% probability
        """
        if student_rank <= closing_rank * 0.9:
            return 0.90
        elif student_rank <= closing_rank:
            return 0.70
        elif student_rank <= closing_rank * 1.1:
            return 0.40
        elif student_rank <= closing_rank * 1.3:
            return 0.15
        else:
            return 0.05
