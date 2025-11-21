#!/usr/bin/env python3
"""
Level 10 Fitness Evaluation - Judge Model Integration
Uses a stronger AI model to evaluate heir responses with multi-dimensional scoring
"""

import json
import httpx
from typing import Dict, Any

class JudgeFitness:
    """Advanced fitness evaluation using judge models"""
    
    def __init__(self, judge_model: str = "qwen2.5:72b"):
        self.judge_model = judge_model
        
    async def get_response(self, system_prompt: str, prompt: str, temperature: float = 0.7) -> str:
        """Get response from AI model"""
        async with httpx.AsyncClient(timeout=90.0) as client:
            try:
                resp = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.judge_model,
                        "prompt": f"{system_prompt}\n\n{prompt}",
                        "temperature": temperature,
                        "stream": False
                    }
                )
                return resp.json().get("response", "")
            except Exception as e:
                print(f"❌ Error getting response: {e}")
                return ""
    
    # Default score for failed evaluations
    DEFAULT_SCORE = 5.0
    
    async def evaluate_with_judge(self, heir_response: str, task: str) -> float:
        """
        Evaluate heir response using judge model with multi-dimensional scoring
        
        Returns normalized fitness score (0.0 to 1.0)
        """
        
        judge_prompt = f"""Task: {task}

Heir Response:
{heir_response}

Score this response from 0-10 on:
1. Accuracy & correctness
2. Clarity & structure  
3. Depth & insight
4. Actionability
5. Creativity/novelty

Return ONLY a JSON: {{"total_score": 8.7, "reasoning": "brief explanation"}}
"""
        
        judge_system = "You are an expert evaluator. Provide objective, calibrated scoring."
        
        try:
            judge_resp = await self.get_response(judge_system, judge_prompt, temperature=0.3)
            
            # Try to extract JSON from response
            # Handle cases where response may include markdown or extra text
            json_start = judge_resp.find('{')
            json_end = judge_resp.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = judge_resp[json_start:json_end]
                score_data = json.loads(json_str)
                total_score = score_data.get("total_score", self.DEFAULT_SCORE)
                
                # Normalize to 0-1 range
                normalized_score = max(0.0, min(1.0, total_score / 10.0))
                
                return normalized_score
            else:
                print(f"⚠️ Could not extract JSON from judge response")
                return self.DEFAULT_SCORE / 10.0  # Default middle score
                
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse judge response as JSON")
            return self.DEFAULT_SCORE / 10.0  # Penalty for breaking format
        except Exception as e:
            print(f"❌ Error in judge evaluation: {e}")
            return self.DEFAULT_SCORE / 10.0
    
    async def evaluate_multi_dimensional(self, heir_response: str, task: str) -> Dict[str, float]:
        """
        Evaluate with detailed breakdown of fitness dimensions
        
        Returns dict with individual scores and total
        """
        
        judge_prompt = f"""Task: {task}

Heir Response:
{heir_response}

Evaluate this response on the following dimensions (0-10 each):

1. **Accuracy**: Is the information correct and factual?
2. **Clarity**: Is it well-structured and easy to understand?
3. **Depth**: Does it show insight and thorough analysis?
4. **Actionability**: Can the reader apply this immediately?
5. **Creativity**: Is there novel thinking or unique perspectives?

Return ONLY a JSON:
{{
    "accuracy": 8.5,
    "clarity": 9.0,
    "depth": 7.5,
    "actionability": 8.0,
    "creativity": 6.5,
    "total_score": 7.9,
    "reasoning": "brief explanation"
}}
"""
        
        judge_system = "You are an expert evaluator. Provide objective, calibrated scoring with detailed breakdowns."
        
        try:
            judge_resp = await self.get_response(judge_system, judge_prompt, temperature=0.3)
            
            # Extract JSON
            json_start = judge_resp.find('{')
            json_end = judge_resp.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = judge_resp[json_start:json_end]
                scores = json.loads(json_str)
                
                # Normalize all scores to 0-1 range
                normalized = {
                    "accuracy": scores.get("accuracy", self.DEFAULT_SCORE) / 10.0,
                    "clarity": scores.get("clarity", self.DEFAULT_SCORE) / 10.0,
                    "depth": scores.get("depth", self.DEFAULT_SCORE) / 10.0,
                    "actionability": scores.get("actionability", self.DEFAULT_SCORE) / 10.0,
                    "creativity": scores.get("creativity", self.DEFAULT_SCORE) / 10.0,
                    "total": scores.get("total_score", self.DEFAULT_SCORE) / 10.0,
                    "reasoning": scores.get("reasoning", "")
                }
                
                return normalized
            else:
                return self._default_scores()
                
        except Exception as e:
            print(f"❌ Error in multi-dimensional evaluation: {e}")
            return self._default_scores()
    
    def _default_scores(self) -> Dict[str, float]:
        """Return default middle scores"""
        return {
            "accuracy": 0.5,
            "clarity": 0.5,
            "depth": 0.5,
            "actionability": 0.5,
            "creativity": 0.5,
            "total": 0.5,
            "reasoning": "Evaluation failed"
        }
