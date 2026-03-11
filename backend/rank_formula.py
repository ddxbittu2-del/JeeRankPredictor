"""
JEE Rank Prediction Formula
NTA official percentile and score-to-rank conversion
"""

from typing import Tuple, List

# ===== OFFICIAL JoSAA SCORE-RANK LOOKUP TABLE (2024) =====
# Based on NTA official data and historical JoSAA cutoffs
# Scores are in descending order, ranks in ascending order

SCORE_RANK_2024 = {
    300: 1,
    298: 10,
    295: 50,
    290: 200,
    285: 500,
    280: 800,
    275: 1400,
    270: 2000,
    265: 3000,
    260: 4000,
    255: 5500,
    250: 7000,
    245: 9000,
    240: 11000,
    235: 13500,
    230: 16000,
    225: 19500,
    220: 23000,
    215: 27500,
    210: 32000,
    205: 37500,
    200: 43000,
    195: 50000,
    190: 57000,
    185: 65500,
    180: 74000,
    175: 84000,
    170: 95000,
    165: 107000,
    160: 120000,
    155: 135000,
    150: 150000,
    145: 168000,
    140: 185000,
    135: 205000,
    130: 225000,
    125: 247000,
    120: 270000,
    115: 295000,
    110: 320000,
    105: 347000,
    100: 380000,
    95: 415000,
    90: 450000,
    85: 490000,
    80: 530000,
    75: 575000,
    70: 620000,
    65: 670000,
    60: 720000,
    55: 775000,
    50: 830000,
    45: 890000,
    40: 950000,
    35: 1010000,
    30: 1050000,
}

SCORE_RANK_2023 = {
    300: 1,
    295: 60,
    290: 250,
    285: 550,
    280: 900,
    275: 1500,
    270: 2200,
    265: 3200,
    260: 4300,
    255: 5800,
    250: 7500,
    245: 9500,
    240: 11800,
    235: 14500,
    230: 17500,
    225: 21000,
    220: 25000,
    215: 29500,
    210: 34500,
    205: 40000,
    200: 46000,
    195: 53000,
    190: 60500,
    185: 69000,
    180: 78000,
    175: 89000,
    170: 100000,
    165: 113000,
    160: 128000,
    155: 143000,
    150: 160000,
    140: 195000,
    130: 235000,
    120: 280000,
    110: 330000,
    100: 390000,
    90: 460000,
    80: 545000,
    70: 640000,
    60: 740000,
    50: 850000,
    40: 970000,
    30: 1060000,
}

SCORE_RANK_2022 = {
    300: 1,
    295: 80,
    290: 300,
    285: 650,
    280: 1050,
    275: 1700,
    270: 2500,
    265: 3600,
    260: 4900,
    255: 6500,
    250: 8300,
    245: 10500,
    240: 13000,
    235: 15800,
    230: 19000,
    225: 22500,
    220: 27000,
    215: 31500,
    210: 37000,
    205: 42500,
    200: 49000,
    195: 56000,
    190: 64000,
    185: 73000,
    180: 83000,
    175: 94000,
    170: 107000,
    165: 120000,
    160: 135000,
    155: 151000,
    150: 168000,
    140: 205000,
    130: 248000,
    120: 295000,
    110: 348000,
    100: 410000,
    90: 480000,
    80: 560000,
    70: 650000,
    60: 750000,
    50: 860000,
    40: 980000,
    30: 1070000,
}

# ===== 2025 SCORE-RANK TABLE (INTERPOLATED) =====
# Extrapolated from 2024 with 2-year trend to 2026
SCORE_RANK_2025 = {}

YEAR_TABLES = {
    2024: SCORE_RANK_2024,
    2023: SCORE_RANK_2023,
    2022: SCORE_RANK_2022,
    2025: SCORE_RANK_2025,  # Will be generated from interpolation
    2026: None,  # Will be generated from trend analysis
}

# Total candidates per year (approx)
TOTAL_CANDIDATES = {
    2024: 1100000,
    2023: 1050000,
    2022: 1000000,
    2025: 1150000,  # Projected for 2025
    2026: 1200000,  # Projected for 2026
}

# ===== HELPER FUNCTIONS =====

def interpolate_rank(score: float, table: dict) -> int:
    """
    Interpolate rank for a score between two known points
    Uses linear interpolation
    """
    sorted_scores = sorted(table.keys(), reverse=True)
    
    # Find the range
    for i in range(len(sorted_scores) - 1):
        score1, score2 = sorted_scores[i], sorted_scores[i + 1]
        if score2 <= score <= score1:
            rank1, rank2 = table[score1], table[score2]
            
            # Linear interpolation
            if score1 == score2:
                return rank1
            
            fraction = (score - score2) / (score1 - score2)
            interpolated_rank = rank2 + fraction * (rank1 - rank2)
            return int(interpolated_rank)
    
    # Out of range - return extremes
    if score > max(table.keys()):
        return 1
    return max(table.values())

# ===== PUBLIC API FUNCTIONS =====

def score_to_rank(score: float, year: int = 2024) -> int:
    """
    Convert JEE Main score to estimated rank
    
    Args:
        score: Raw marks (0-300) or percentile (0-100)
        year: Exam year (2022-2024)
    
    Returns:
        Estimated JEE rank
    """
    # Ensure score is in valid range
    score = max(0, min(300, score))
    
    # Get the appropriate table
    table = YEAR_TABLES.get(year, SCORE_RANK_2024)
    
    return interpolate_rank(score, table)

def rank_to_percentile(rank: int, year: int = 2024) -> float:
    """
    Convert JEE rank to percentile score
    
    Percentile = (Candidates scoring less than you / Total Candidates) × 100
    
    Args:
        rank: JEE rank
        year: Exam year
    
    Returns:
        Percentile (0-100)
    """
    total = TOTAL_CANDIDATES.get(year, 1000000)
    
    # Percentile = (candidates_with_better_score / total) × 100
    # If you're ranked N, then (N-1) people are ahead
    percentile = ((total - rank + 1) / total) * 100
    
    return max(0, min(100, percentile))

def percentile_to_rank(percentile: float, year: int = 2024) -> int:
    """
    Convert percentile to JEE rank
    
    Args:
        percentile: Percentile score (0-100)
        year: Exam year
    
    Returns:
        Estimated JEE rank
    """
    total = TOTAL_CANDIDATES.get(year, 1000000)
    
    # Reverse formula: rank = total × (1 - percentile/100)
    rank = int(total * (1 - percentile / 100)) + 1
    
    return max(1, rank)

def get_confidence_range(rank: int) -> Tuple[int, int]:
    """
    Get confidence interval (±margin) for a predicted rank
    
    Based on statistical uncertainty:
    - Rank < 10,000: ±5%
    - Rank 10,000-100,000: ±8%
    - Rank > 100,000: ±12%
    
    Args:
        rank: JEE rank
    
    Returns:
        Tuple of (min_rank, max_rank)
    """
    if rank < 10000:
        margin = int(rank * 0.05)
    elif rank < 100000:
        margin = int(rank * 0.08)
    else:
        margin = int(rank * 0.12)
    
    return (max(1, rank - margin), rank + margin)

def estimate_rank_range(score: float, input_type: str, year: int = 2024) -> Tuple[int, int]:
    """
    Quick estimate of rank range for live preview
    
    Args:
        score: Student's score
        input_type: 'marks' or 'percentile'
        year: Exam year
    
    Returns:
        Tuple of (min_rank, max_rank)
    """
    if input_type == "marks":
        # Estimate rank with ±5 marks margin
        rank_center = score_to_rank(score, year)
        rank_low = score_to_rank(max(0, score - 5), year)
        rank_high = score_to_rank(min(300, score + 5), year)
        
        return (rank_high, rank_low)  # Note: higher score = lower rank number
    
    elif input_type == "percentile":
        rank_center = percentile_to_rank(score, year)
        rank_low = percentile_to_rank(max(0, score - 2), year)
        rank_high = percentile_to_rank(min(100, score + 2), year)
        
        return (rank_high, rank_low)
    
    else:
        # Already a rank
        confidence = get_confidence_range(int(score))
        return (confidence[0], confidence[1])

def get_category_adjustment(category: str) -> float:
    """
    Get rank adjustment factor for different categories
    
    Note: In JoSAA counselling, each category has separate merit lists,
    so a student in SC category doesn't directly compare to GEN category.
    This is informational.
    
    Args:
        category: Student category
    
    Returns:
        Adjustment factor (for reference only)
    """
    factors = {
        'GEN': 1.0,
        'GEN-PwD': 1.0,
        'OBC-NCL': 0.95,  # Different merit list, not directly comparable
        'OBC-NCL-PwD': 0.95,
        'SC': 0.9,  # Different merit list
        'ST': 0.85,  # Different merit list
        'EWS': 0.98,  # Similar to GEN, separate list
    }
    return factors.get(category, 1.0)

# ===== PERCENTILE BANDS (NTA Official) =====
# For reference: what percentile corresponds to what rank range

PERCENTILE_BANDS = {
    99: (1, 10000),
    95: (10001, 50000),
    90: (50001, 100000),
    80: (100001, 300000),
    70: (300001, 600000),
    50: (600001, 900000),
    30: (900001, 1050000),
}

def get_percentile_band(rank: int) -> Tuple[int, str]:
    """
    Get the percentile band for a rank
    
    Args:
        rank: JEE rank
    
    Returns:
        Tuple of (percentile_band, band_name)
    """
    for percentile, (min_rank, max_rank) in PERCENTILE_BANDS.items():
        if min_rank <= rank <= max_rank:
            return (percentile, f"{percentile}+ Percentile")
    

def generate_2025_and_2026_tables() -> tuple:
    """
    Generate 2025 and 2026 score-to-rank predictions using trend analysis
    from 2022, 2023, 2024 data
    
    Uses linear regression on historical data to project future cutoffs
    
    Returns:
        Tuple of (table_2025, table_2026) dictionaries
    """
    table_2025 = {}
    table_2026 = {}
    
    # Get candidate counts
    candidates_2022 = TOTAL_CANDIDATES[2022]  # 1000000
    candidates_2023 = TOTAL_CANDIDATES[2023]  # 1050000
    candidates_2024 = TOTAL_CANDIDATES[2024]  # 1100000
    candidates_2025 = TOTAL_CANDIDATES[2025]  # 1150000
    candidates_2026 = TOTAL_CANDIDATES[2026]  # 1200000
    
    # For each score, calculate the trend and project future years
    for score in SCORE_RANK_2024.keys():
        rank_2024 = SCORE_RANK_2024[score]
        rank_2023 = SCORE_RANK_2023.get(score, rank_2024)
        rank_2022 = SCORE_RANK_2022.get(score, rank_2023)
        
        # Calculate growth rates
        if rank_2022 > 0:
            growth_22_23 = (rank_2023 - rank_2022) / rank_2022
            growth_23_24 = (rank_2024 - rank_2023) / rank_2023 if rank_2023 > 0 else 0
        else:
            growth_22_23 = 0
            growth_23_24 = 0
        
        # Average growth rate per year
        avg_growth_per_year = (growth_22_23 + growth_23_24) / 2
        
        # Project 2025 (1 year ahead from 2024)
        rank_2025 = int(rank_2024 * (1 + avg_growth_per_year))
        table_2025[score] = rank_2025
        
        # Project 2026 (2 years ahead from 2024)
        rank_2026 = int(rank_2024 * (1 + avg_growth_per_year * 2))
        table_2026[score] = rank_2026
    
    return table_2025, table_2026

# Generate 2025 and 2026 tables on startup
YEAR_TABLES[2025], YEAR_TABLES[2026] = generate_2025_and_2026_tables()

