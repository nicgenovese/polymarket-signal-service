"""
Polymarket Market Analyzer
Scans and analyzes Polymarket markets for trading opportunities
"""

import requests
from typing import List, Dict
from datetime import datetime


class MarketAnalyzer:
    """Analyzes Polymarket markets to identify trading opportunities"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://gamma-api.polymarket.com"
        
    def get_trending_markets(self, limit: int = 50) -> List[Dict]:
        """Fetch trending markets sorted by volume"""
        endpoint = f"{self.base_url}/markets"
        params = {
            "_sort": "volume",
            "_limit": limit
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
    
    def analyze_market(self, market: Dict) -> Dict:
        """Analyze a single market for opportunity"""
        analysis = {
            "market_id": market.get("id"),
            "question": market.get("question"),
            "volume": float(market.get("volume", 0)),
            "liquidity": float(market.get("liquidity", 0)),
            "current_price": self._get_current_price(market),
            "opportunity_score": 0.0,
            "recommendation": "SKIP",
            "reasoning": []
        }
        
        # Calculate opportunity score
        score = 0.0
        
        # High volume = more liquid
        if analysis["volume"] > 1_000_000:
            score += 30
            analysis["reasoning"].append("High volume market")
        
        # Good liquidity
        if analysis["liquidity"] > 100_000:
            score += 20
            analysis["reasoning"].append("Good liquidity")
        
        # Price analysis
        price = analysis["current_price"]
        if price and 0.40 <= price <= 0.60:
            score += 25
            analysis["reasoning"].append("Fair pricing, room for movement")
        
        # Time to resolution
        ends_at = market.get("end_date_iso")
        if ends_at:
            days_left = self._days_until(ends_at)
            if 7 <= days_left <= 90:
                score += 15
                analysis["reasoning"].append(f"Good timeframe ({days_left} days)")
        
        analysis["opportunity_score"] = score
        
        # Generate recommendation
        if score >= 70:
            analysis["recommendation"] = "STRONG BUY"
        elif score >= 50:
            analysis["recommendation"] = "BUY"
        elif score >= 30:
            analysis["recommendation"] = "WATCH"
        
        return analysis
    
    def _get_current_price(self, market: Dict) -> float:
        """Extract current YES price from market"""
        try:
            # Polymarket API structure varies, adjust as needed
            outcomes = market.get("outcomes", [])
            if outcomes:
                return float(outcomes[0].get("price", 0))
            return 0.0
        except:
            return 0.0
    
    def _days_until(self, iso_date: str) -> int:
        """Calculate days until date"""
        try:
            end_date = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
            now = datetime.now(end_date.tzinfo)
            return (end_date - now).days
        except:
            return 0
    
    def scan_opportunities(self, min_score: int = 50) -> List[Dict]:
        """Scan all markets and return opportunities above threshold"""
        markets = self.get_trending_markets()
        opportunities = []
        
        for market in markets:
            analysis = self.analyze_market(market)
            if analysis["opportunity_score"] >= min_score:
                opportunities.append(analysis)
        
        # Sort by score descending
        opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return opportunities


if __name__ == "__main__":
    # Test the analyzer
    analyzer = MarketAnalyzer()
    print("Scanning Polymarket for opportunities...")
    
    opportunities = analyzer.scan_opportunities(min_score=30)
    
    print(f"\nFound {len(opportunities)} opportunities:\n")
    
    for opp in opportunities[:10]:  # Top 10
        print(f"Score: {opp['opportunity_score']:.0f} | {opp['recommendation']}")
        print(f"Market: {opp['question']}")
        print(f"Volume: ${opp['volume']:,.0f} | Price: {opp['current_price']:.2f}")
        print(f"Reasoning: {', '.join(opp['reasoning'])}")
        print("-" * 80)
