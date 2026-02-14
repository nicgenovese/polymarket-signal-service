"""
Signal Generator
Converts market analysis into actionable trading signals
"""

from typing import Dict, List
from datetime import datetime
import json


class SignalGenerator:
    """Generates trading signals from market analysis"""
    
    def __init__(self, min_confidence: int = 60):
        self.min_confidence = min_confidence
        self.signals_generated = []
        
    def generate_signal(self, analysis: Dict) -> Dict:
        """Generate a trading signal from market analysis"""
        
        signal = {
            "signal_id": self._generate_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "market_id": analysis["market_id"],
            "market_question": analysis["question"],
            "action": "SKIP",
            "side": None,
            "confidence": 0,
            "entry_price": analysis["current_price"],
            "target_price": None,
            "stop_loss": None,
            "position_size": 0,
            "reasoning": analysis["reasoning"],
            "data": {
                "volume": analysis["volume"],
                "liquidity": analysis["liquidity"],
                "opportunity_score": analysis["opportunity_score"]
            }
        }
        
        # Convert opportunity score to confidence
        confidence = self._calculate_confidence(analysis)
        signal["confidence"] = confidence
        
        # Determine action
        if confidence >= self.min_confidence:
            signal["action"] = "TRADE"
            signal["side"] = self._determine_side(analysis)
            
            # Calculate targets
            current_price = analysis["current_price"]
            if signal["side"] == "YES":
                signal["target_price"] = min(current_price + 0.10, 0.95)
                signal["stop_loss"] = max(current_price - 0.05, 0.05)
            else:  # NO
                signal["target_price"] = max(current_price - 0.10, 0.05)
                signal["stop_loss"] = min(current_price + 0.05, 0.95)
            
            # Position sizing based on confidence
            signal["position_size"] = self._calculate_position_size(confidence)
        
        # Store signal
        self.signals_generated.append(signal)
        
        return signal
    
    def _calculate_confidence(self, analysis: Dict) -> int:
        """Calculate confidence score (0-100)"""
        score = analysis["opportunity_score"]
        
        # Adjust based on market characteristics
        volume = analysis["volume"]
        liquidity = analysis["liquidity"]
        
        # Bonus for high volume
        if volume > 5_000_000:
            score += 10
        elif volume > 2_000_000:
            score += 5
        
        # Bonus for high liquidity
        if liquidity > 500_000:
            score += 10
        elif liquidity > 200_000:
            score += 5
        
        # Cap at 100
        return min(int(score), 100)
    
    def _determine_side(self, analysis: Dict) -> str:
        """Determine whether to buy YES or NO"""
        price = analysis["current_price"]
        
        # If price is low, consider YES
        # If price is high, consider NO
        # Middle ground needs more analysis
        
        if price < 0.40:
            return "YES"
        elif price > 0.60:
            return "NO"
        else:
            # Analyze trend, volume, momentum
            # For now, default to YES
            return "YES"
    
    def _calculate_position_size(self, confidence: int) -> float:
        """Calculate position size based on confidence (% of bankroll)"""
        if confidence >= 90:
            return 0.10  # 10% of bankroll
        elif confidence >= 80:
            return 0.07
        elif confidence >= 70:
            return 0.05
        elif confidence >= 60:
            return 0.03
        else:
            return 0.01
    
    def _generate_id(self) -> str:
        """Generate unique signal ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        count = len(self.signals_generated)
        return f"SIG-{timestamp}-{count:04d}"
    
    def generate_batch(self, analyses: List[Dict], max_signals: int = 5) -> List[Dict]:
        """Generate multiple signals from analyses"""
        signals = []
        
        for analysis in analyses:
            signal = self.generate_signal(analysis)
            if signal["action"] == "TRADE":
                signals.append(signal)
                
                if len(signals) >= max_signals:
                    break
        
        return signals
    
    def format_for_twitter(self, signal: Dict) -> str:
        """Format signal for Twitter post"""
        emoji = "🟢" if signal["side"] == "YES" else "🔴"
        confidence_emoji = "🔥" if signal["confidence"] >= 80 else "⚡"
        
        text = f"""{emoji} POLYMARKET SIGNAL {confidence_emoji}

Market: {signal['market_question'][:100]}

Action: BUY {signal['side']}
Entry: {signal['entry_price']:.2f}
Target: {signal['target_price']:.2f}
Confidence: {signal['confidence']}%

Reasoning: {', '.join(signal['reasoning'][:2])}

#{signal['signal_id']}"""
        
        return text
    
    def save_signals(self, signals: List[Dict], filepath: str):
        """Save signals to JSON file"""
        with open(filepath, 'w') as f:
            json.dump({
                "generated_at": datetime.utcnow().isoformat(),
                "count": len(signals),
                "signals": signals
            }, f, indent=2)


if __name__ == "__main__":
    # Test signal generator
    from analyzer.market_analyzer import MarketAnalyzer
    
    print("Scanning markets and generating signals...")
    
    analyzer = MarketAnalyzer()
    opportunities = analyzer.scan_opportunities(min_score=50)
    
    generator = SignalGenerator(min_confidence=70)
    signals = generator.generate_batch(opportunities, max_signals=3)
    
    print(f"\nGenerated {len(signals)} signals:\n")
    
    for signal in signals:
        print(f"\n{generator.format_for_twitter(signal)}")
        print("=" * 80)
