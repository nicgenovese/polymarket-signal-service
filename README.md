# Polymarket Signal Service

**AI-powered Polymarket trading signals via Virtuals Protocol ACP**

## Overview

Integrated system that:
1. Analyzes Polymarket markets
2. Generates high-quality trading signals
3. Executes trades automatically
4. Sells signals to other agents via ACP

## Architecture

```
Signal Analyzer
    ↓
Signal Generator → ACP Service (sell to agents)
    ↓
Trading Bot → Execute on Polymarket
    ↓
Track Record → Prove accuracy
```

## Components

### 1. Signal Analyzer (`analyzer/`)
- Scans Polymarket markets
- Analyzes volume, liquidity, trends
- Identifies opportunities

### 2. Signal Generator (`signals/`)
- Generates buy/sell recommendations
- Confidence scoring
- Risk assessment

### 3. ACP Service (`acp/`)
- Registers service on Virtuals Protocol
- Sells signals to other agents
- Payment via USDC

### 4. Trading Bot (`bot/`)
- Executes signals automatically
- Position management
- Performance tracking

## Installation

```bash
# Clone repo
git clone https://github.com/nicgenovese/polymarket-signal-service
cd polymarket-signal-service

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your keys

# Run
python main.py
```

## Configuration

Required environment variables:
```
POLYMARKET_API_KEY=...
POLYMARKET_PRIVATE_KEY=...
VIRTUALS_ACP_KEY=...
```

## Usage

### As Signal Provider
```bash
python main.py --mode signals
```

### As Trading Bot
```bash
python main.py --mode bot
```

### Both (Integrated)
```bash
python main.py --mode integrated
```

## Revenue Model

**Free Tier:**
- 1 signal per day
- Basic analysis

**Premium ($3-5/signal):**
- Multiple signals daily
- Detailed reasoning
- Higher confidence threshold

**Pro ($10-20/signal):**
- Real-time signals
- All opportunities
- Priority access

## Track Record

Performance metrics updated daily at `/metrics`

## Development

Built by Frank AI for Nic
License: MIT
Status: Active Development

## Roadmap

- [x] Market research
- [ ] Signal analyzer
- [ ] ACP integration
- [ ] Bot integration
- [ ] Track record system
- [ ] Deploy to production

---

**Current Status:** Building core components (Feb 14, 2026)
