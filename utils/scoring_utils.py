from typing import Dict, Any

def calculate_category_score(matches: int, total: int) -> float:
    """
    Calculate a category score based on matches.
    
    Args:
        matches (int): Number of matches
        total (int): Total possible matches
        
    Returns:
        float: Score between 0 and 1
    """
    if total == 0:
        return 1.0  # Perfect score if no requirements
    
    return min(matches / total, 1.0)

def normalize_score(score: float) -> float:
    """
    Normalize a score to 0-100 scale.
    
    Args:
        score (float): Raw score (0-1)
        
    Returns:
        float: Normalized score (0-100)
    """
    return min(max(score * 100, 0), 100)

def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate a weighted score from category scores.
    
    Args:
        scores (Dict[str, float]): Category scores
        weights (Dict[str, float]): Category weights
        
    Returns:
        float: Weighted score
    """
    weighted_score = 0
    
    for category, score in scores.items():
        weight = weights.get(category, 0)
        weighted_score += score * weight
    
    return weighted_score

def calculate_confidence_interval(scores: Dict[str, float], weights: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate confidence interval for a score.
    
    Args:
        scores (Dict[str, float]): Category scores
        weights (Dict[str, float]): Category weights
        
    Returns:
        Dict[str, float]: Confidence interval (lower, upper)
    """
    # Calculate variance based on category scores
    weighted_scores = [score * weights.get(category, 0) for category, score in scores.items()]
    mean_score = sum(weighted_scores) / sum(weights.values())
    variance = sum(weights.get(category, 0) * (score - mean_score) ** 2 for category, score in scores.items()) / sum(weights.values())
    std_dev = variance ** 0.5
    
    # Calculate 95% confidence interval
    margin = 1.96 * std_dev
    lower = max(0, mean_score - margin)
    upper = min(100, mean_score + margin)
    
    return {"lower": lower, "upper": upper}