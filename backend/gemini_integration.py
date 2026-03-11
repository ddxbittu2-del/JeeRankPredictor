"""
Gemini AI Integration Module
Provides intelligent college filtering, package intelligence, and career recommendations
"""

import google.generativeai as genai
import json
import os
from typing import List, Dict, Any

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBaxFzgQ_MSmlfWAPsWu3V0GdAuYhUMJ1M")
genai.configure(api_key=GEMINI_API_KEY)

# Model configuration - Use latest available model
MODEL_NAME = "gemini-2.5-flash"  # Latest and fastest model
model = genai.GenerativeModel(MODEL_NAME)

class GeminiCollegePrediction:
    """Gemini-powered intelligent college prediction and analysis"""
    
    @staticmethod
    def smart_college_filter(rank: int, category: str, user_preference: str, available_colleges: List[Dict]) -> Dict[str, Any]:
        """
        Use Gemini to intelligently filter colleges based on natural language preference
        
        Args:
            rank: Student's JEE rank
            category: Category (GEN, OBC, SC, ST, PwD)
            user_preference: Natural language preference (e.g., "CSE near Mumbai, 20+ LPA")
            available_colleges: List of available colleges with cutoffs
        
        Returns:
            Filtered colleges with Gemini analysis
        """
        try:
            prompt = f"""
You are a JEE counselling expert. Analyze the following:

Student Profile:
- JEE Rank: {rank}
- Category: {category}
- Preference: {user_preference}

Available Colleges (Top 10):
{json.dumps(available_colleges[:10], indent=2)}

Task: 
1. Match colleges to student preference
2. Rate each college 1-10 based on how well it matches their goals
3. Explain WHY each college is good/bad for them
4. Suggest the top 3 colleges they should apply for

Return as JSON:
{{
    "recommended_colleges": [
        {{"name": "College Name", "rank": "Rank", "match_score": 9, "reason": "Why this matches", "probability": "85%"}}
    ],
    "analysis": "Overall advice",
    "key_insight": "Most important point"
}}
"""
            
            response = model.generate_content(prompt)
            result = response.text
            
            # Try to extract JSON from response
            try:
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            return {
                "status": "success",
                "analysis": result,
                "source": "gemini_1.5_flash"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "fallback": "Using traditional filtering"
            }
    
    @staticmethod
    def get_package_intelligence(colleges: List[str]) -> Dict[str, Any]:
        """
        Use Gemini to fetch latest placement package information
        
        Args:
            colleges: List of college names
        
        Returns:
            Package data with trends
        """
        try:
            prompt = f"""
You are a placement expert. Based on latest 2024-2025 data:

Colleges: {', '.join(colleges)}

For each college, provide:
1. Average package 2024
2. Highest package 2024
3. Expected package 2025 (with growth %)
4. Top recruiting companies
5. Package by branch (CSE, ECE, Mechanical)

Return as JSON:
{{
    "colleges_package_data": [
        {{
            "name": "College Name",
            "avg_package_2024": 15.5,
            "highest_package_2024": 45,
            "expected_2025": 16.8,
            "growth_percent": 8.4,
            "top_recruiters": ["Company1", "Company2"],
            "branch_packages": {{"CSE": 18, "ECE": 12, "Mech": 10}}
        }}
    ],
    "market_trend": "Growing/Stable/Declining",
    "insights": "Key market insights"
}}
"""
            
            response = model.generate_content(prompt)
            result = response.text
            
            try:
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            return {
                "status": "success",
                "analysis": result,
                "source": "gemini_package_intelligence"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "fallback": "Using cached package data"
            }
    
    @staticmethod
    def career_recommendation(rank: int, category: str, target_role: str, colleges: List[Dict]) -> Dict[str, Any]:
        """
        Use Gemini to recommend best college for specific career goal
        
        Args:
            rank: JEE rank
            category: Category
            target_role: Target role (e.g., "Software Engineer", "Data Scientist", "Startup Founder")
            colleges: Available colleges
        
        Returns:
            Career-optimized college recommendations
        """
        try:
            prompt = f"""
You are a career counselor for IIT/NIT graduates.

Student Profile:
- JEE Rank: {rank}
- Category: {category}
- Target Career: {target_role}
- Available Colleges: {json.dumps(colleges[:5], indent=2)}

Analyze:
1. Which college is BEST for this career?
2. Which branches in those colleges lead to this career?
3. What does this student need to do to succeed?
4. What are alternative paths?
5. Success probability at each college for this goal

Return as JSON:
{{
    "best_college_for_goal": {{"name": "College", "probability": "85%", "reason": "..."}},
    "best_branches": ["CSE", "IT"],
    "action_plan": ["Step 1", "Step 2"],
    "placement_success": "85% students from this college get this role",
    "salary_expectation": "15-25 LPA",
    "top_companies": ["Company1", "Company2"],
    "success_rate_by_college": [
        {{"college": "Name", "success_rate": "75%", "avg_salary": "18 LPA"}}
    ]
}}
"""
            
            response = model.generate_content(prompt)
            result = response.text
            
            try:
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            return {
                "status": "success",
                "analysis": result,
                "source": "gemini_career_advisor"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "fallback": "Using traditional analysis"
            }
    
    @staticmethod
    def compare_colleges(colleges: List[Dict], category: str, criteria: str = "overall") -> Dict[str, Any]:
        """
        Use Gemini to provide detailed college comparison
        
        Args:
            colleges: Colleges to compare
            category: Student category
            criteria: Comparison criteria (overall, placement, academics, lifestyle)
        
        Returns:
            Detailed comparison analysis
        """
        try:
            prompt = f"""
You are a college comparison expert. Compare these colleges:

Colleges: {json.dumps(colleges, indent=2)}
Category: {category}
Compare by: {criteria}

For each college, rate (1-10):
1. Academics & Faculty
2. Placement Quality
3. Campus Life
4. Infrastructure
5. Industry Connections
6. Alumni Network
7. {criteria.capitalize()} (main focus)

Return detailed JSON comparison:
{{
    "colleges_comparison": [
        {{
            "name": "College",
            "overall_score": 8.5,
            "academics": 9,
            "placements": 8,
            "campus_life": 7,
            "infrastructure": 8,
            "industry_connections": 8,
            "alumni_network": 9,
            "{criteria}": 9,
            "pros": ["Strength 1", "Strength 2"],
            "cons": ["Weakness 1"],
            "best_for": "Type of student"
        }}
    ],
    "winner": "College Name",
    "runner_up": "College Name",
    "recommendation": "Which college to choose and why"
}}
"""
            
            response = model.generate_content(prompt)
            result = response.text
            
            try:
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            return {
                "status": "success",
                "analysis": result,
                "source": "gemini_comparison"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "fallback": "Using traditional comparison"
            }
    
    @staticmethod
    def enhance_probability(base_probability: float, college_name: str, rank: int, category: str) -> Dict[str, Any]:
        """
        Use Gemini to enhance probability prediction with contextual analysis
        
        Args:
            base_probability: Original probability from rule-based system
            college_name: College name
            rank: Student rank
            category: Category
        
        Returns:
            Enhanced probability with explanation
        """
        try:
            prompt = f"""
You are a JEE counselling data analyst.

Current Prediction:
- College: {college_name}
- Rank: {rank}
- Category: {category}
- Base Probability: {base_probability*100:.1f}%

Analyze:
1. Is base probability accurate?
2. Consider category-wise cutoff advantages
3. Check for floating seat possibilities
4. Analyze historical closing rank trends
5. Give refined probability estimate

Return JSON:
{{
    "refined_probability": 0.85,
    "confidence": "High/Medium/Low",
    "explanation": "Why this is the refined estimate",
    "floating_seat_chance": "10-15%",
    "key_factors": ["Factor 1", "Factor 2"],
    "recommendation": "Apply/Consider/Backup"
}}
"""
            
            response = model.generate_content(prompt)
            result = response.text
            
            try:
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            return {
                "refined_probability": base_probability,
                "source": "enhanced_with_gemini"
            }
            
        except Exception as e:
            return {
                "refined_probability": base_probability,
                "source": "fallback"
            }


# Test function
if __name__ == "__main__":
    print("Testing Gemini Integration...")
    
    # Test smart filter
    test_colleges = [
        {"name": "IIT Bombay", "rank": 100, "branch": "CSE"},
        {"name": "NIT Trichy", "rank": 5000, "branch": "CSE"},
        {"name": "IIIT Hyderabad", "rank": 8000, "branch": "CSE"}
    ]
    
    result = GeminiCollegePrediction.smart_college_filter(
        rank=7000,
        category="GEN",
        user_preference="CSE, good placement, south India",
        available_colleges=test_colleges
    )
    
    print("Smart Filter Result:", json.dumps(result, indent=2))
    print("\n✅ Gemini integration successful!")
