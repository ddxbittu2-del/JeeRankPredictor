#!/usr/bin/env python3
"""
ML Model Training Script
Trains rank and college prediction models
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report, roc_auc_score
import joblib
from pathlib import Path

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

# ===== RANK MODEL TRAINING =====

def train_rank_model():
    """
    Train GradientBoostingRegressor for rank prediction
    Features: score, year, category
    Target: rank
    """
    print_info("Training Rank Prediction Model...")
    
    # Generate training data from score-rank mapping
    from rank_formula import SCORE_RANK_2024, SCORE_RANK_2023, SCORE_RANK_2022
    
    X = []
    y = []
    
    for year, table in [(2024, SCORE_RANK_2024), (2023, SCORE_RANK_2023), (2022, SCORE_RANK_2022)]:
        for score, rank in table.items():
            for category_id, category in enumerate(['GEN', 'OBC-NCL', 'SC', 'ST', 'EWS']):
                X.append([score, year, category_id])
                y.append(rank)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"Training data: {len(X)} samples")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        min_samples_leaf=5,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MAE: {mae:.0f}")
    print(f"R² Score: {r2:.4f}")
    
    # Sample predictions
    print("\nSample predictions:")
    for i in range(min(3, len(X_test))):
        print(f"  Score: {X_test[i][0]}, Year: {int(X_test[i][1])}, Category: {int(X_test[i][2])}")
        print(f"  True Rank: {y_test[i]:.0f}, Predicted: {y_pred[i]:.0f}")
    
    # Save model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'rank_model.pkl')
    joblib.dump(model, model_path)
    print_success(f"Rank model saved: {model_path}")
    
    return model

# ===== COLLEGE MODEL TRAINING =====

def train_college_model():
    """
    Train RandomForestClassifier for college admission prediction
    Features: rank, opening_rank, closing_rank, category, seat_pool, institute_type, quota, year, round
    Target: admission (binary)
    """
    print_info("Training College Admission Model...")
    
    # Load data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data')
    csv_path = os.path.join(data_dir, 'josaa_all.csv')
    
    if not os.path.exists(csv_path):
        print_warning(f"Data file not found: {csv_path}")
        print_warning("Skipping college model training. Using fallback logic in predictor.py")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"Loaded data: {len(df)} rows")
    
    # Standardize columns
    column_mapping = {
        'Institute': 'institute_name',
        'Program': 'program',
        'Type': 'institute_type',
        'Category': 'category',
        'Seat_Pool': 'seat_pool',
        'Opening_Rank': 'opening_rank',
        'Closing_Rank': 'closing_rank',
        'Year': 'year',
        'Round': 'round',
        'Quote': 'quota',
    }
    
    for old, new in column_mapping.items():
        if old in df.columns and new not in df.columns:
            df.rename(columns={old: new}, inplace=True)
    
    # Create target: 1 if rank <= closing_rank, 0 otherwise
    df['admitted'] = (df['opening_rank'] <= df['closing_rank']).astype(int)
    
    # Feature engineering
    df['rank_gap'] = df['closing_rank'] - df['opening_rank']
    df['rank_ratio'] = (df['opening_rank'] / df['closing_rank']).fillna(1.0)
    
    # Encode categorical variables
    encoders = {}
    categorical_cols = ['category', 'seat_pool', 'institute_type', 'quota']
    
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[f'{col}_enc'] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    
    # Prepare features
    feature_cols = [
        'opening_rank',
        'closing_rank',
        'rank_gap',
        'rank_ratio',
        'year',
        'round',
    ]
    feature_cols += [f'{col}_enc' for col in categorical_cols if col in df.columns]
    
    X = df[feature_cols].fillna(0).values
    y = df['admitted'].values
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution: {np.bincount(y)}")
    
    # Train-test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Admitted', 'Admitted']))
    
    # ROC-AUC
    try:
        y_proba = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_proba)
        print(f"ROC-AUC: {roc_auc:.4f}")
    except:
        pass
    
    # Save model and encoders
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'college_model.pkl')
    encoders_path = os.path.join(models_dir, 'encoders.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(encoders, encoders_path)
    
    print_success(f"College model saved: {model_path}")
    print_success(f"Encoders saved: {encoders_path}")
    
    return model

# ===== FEATURE IMPORTANCE =====

def print_feature_importance(model, feature_names):
    """Print feature importance"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        print("\nFeature Importance:")
        for i in range(min(10, len(importances))):
            idx = indices[i]
            print(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")

# ===== MAIN =====

if __name__ == "__main__":
    print("\n" + "="*60)
    print(BOLD + "JEE RANK PREDICTOR — MODEL TRAINING" + RESET)
    print("="*60 + "\n")
    
    try:
        print("Step 1: Training Rank Prediction Model")
        print("-" * 60)
        rank_model = train_rank_model()
        print()
    except Exception as e:
        print_error(f"Rank model training failed: {e}")
    
    try:
        print("Step 2: Training College Admission Model")
        print("-" * 60)
        college_model = train_college_model()
        print()
    except Exception as e:
        print_warning(f"College model training failed: {e}")
        print_info("Using fallback rule-based logic")
    
    print("="*60)
    print_success("Model training complete!")
    print("="*60 + "\n")
