"""
Polymarket Signal Service - Main Entry Point
Integrated signal generation, ACP service, and trading bot
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from analyzer.market_analyzer import MarketAnalyzer
from signals.signal_generator import SignalGenerator
from acp.service import ACPSignalService


def run_analyzer():
    """Run market analysis and generate signals"""
    print(f"[{datetime.now()}] Starting market analysis...")
    
    analyzer = MarketAnalyzer()
    opportunities = analyzer.scan_opportunities(min_score=50)
    
    print(f"Found {len(opportunities)} opportunities")
    
    generator = SignalGenerator(min_confidence=60)
    signals = generator.generate_batch(opportunities, max_signals=5)
    
    print(f"Generated {len(signals)} signals")
    
    # Save signals
    os.makedirs('data', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/signals_{timestamp}.json"
    generator.save_signals(signals, filepath)
    print(f"Saved to {filepath}")
    
    # Print signals
    for signal in signals:
        print("\n" + "="*80)
        print(generator.format_for_twitter(signal))
    
    return signals


def run_acp_service():
    """Run ACP service (server mode)"""
    print(f"[{datetime.now()}] Starting ACP service...")
    
    service = ACPSignalService()
    offering = service.create_offering()
    
    print("Service configuration:")
    print(f"  Name: {offering['name']}")
    print(f"  Description: {offering['description']}")
    print(f"  Tiers: {list(offering['pricing'].keys())}")
    
    print("\nACP service ready (integration with Virtuals Protocol pending)")
    print("To register: cd ~/.openclaw/skills/openclaw-acp && ./bin/acp.ts sell init polymarket-signals")


def run_bot():
    """Run trading bot (execute signals)"""
    print(f"[{datetime.now()}] Starting trading bot...")
    
    # Generate signals
    signals = run_analyzer()
    
    print("\n[Bot] Analyzing signals for execution...")
    
    for signal in signals:
        if signal["action"] == "TRADE" and signal["confidence"] >= 70:
            print(f"\n[Bot] Would execute: {signal['signal_id']}")
            print(f"      Market: {signal['market_question'][:60]}...")
            print(f"      Side: {signal['side']}")
            print(f"      Size: {signal['position_size']*100:.1f}% of bankroll")
            print(f"      Entry: {signal['entry_price']:.2f}")
            print(f"      Target: {signal['target_price']:.2f}")
    
    print("\n[Bot] Execution pending - integrate with Polymarket bot")


def run_integrated():
    """Run full integrated system"""
    print(f"[{datetime.now()}] Starting integrated system...")
    print("="*80)
    
    # 1. Analyze markets
    print("\n[1/3] Analyzing markets...")
    signals = run_analyzer()
    
    # 2. Start ACP service
    print("\n[2/3] Initializing ACP service...")
    service = ACPSignalService()
    print(f"      Service ready: {service.service_name}")
    
    # 3. Execute high-confidence signals
    print("\n[3/3] Trading bot evaluation...")
    high_conf = [s for s in signals if s["confidence"] >= 80]
    print(f"      {len(high_conf)} high-confidence signals")
    
    print("\n" + "="*80)
    print("Integrated system ready")
    print(f"Next steps:")
    print(f"  1. Register ACP service on Virtuals Protocol")
    print(f"  2. Connect to Polymarket bot for execution")
    print(f"  3. Post free signals to Twitter for track record")


def main():
    parser = argparse.ArgumentParser(description='Polymarket Signal Service')
    parser.add_argument('--mode', choices=['analyzer', 'acp', 'bot', 'integrated'], 
                        default='integrated',
                        help='Run mode: analyzer, acp, bot, or integrated')
    
    args = parser.parse_args()
    
    print("="*80)
    print("POLYMARKET SIGNAL SERVICE")
    print("AI-powered trading signals via Virtuals Protocol ACP")
    print("="*80)
    
    if args.mode == 'analyzer':
        run_analyzer()
    elif args.mode == 'acp':
        run_acp_service()
    elif args.mode == 'bot':
        run_bot()
    elif args.mode == 'integrated':
        run_integrated()


if __name__ == "__main__":
    main()
