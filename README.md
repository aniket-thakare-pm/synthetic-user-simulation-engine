# Synthetic User Simulation Engine (Phase 1 MVP)

A guardrailed, anti-sycophancy synthetic user interview engine built with Python and the Gemini API.

## Features
- **Persona Boxing & Guardrailing:** Multi-layer system prompt encapsulation preventing AI politeness and enforcing hard negative constraints.
- **Deterministic Pre-Checks:** Hard-rule checks (e.g. price ceilings, patience score caps, forced sales call rejection) evaluated before LLM generation.
- **Stateless Single-Turn Context:** Prevents context drift and sycophantic momentum across queries.
- **Panel Interview Execution:** Test any product pitch against 3 distinct personas simultaneously.

## How to Run

1. Navigate to the project directory:
   ```bash
   cd synthetic_user_engine
   ```

2. Set your Gemini API key (or enter it when prompted):
   ```bash
   set GEMINI_API_KEY=your_actual_key_here
   ```

3. Run the interactive simulation engine:
   ```bash
   python main.py
   ```

## Example Test Pitches

Try testing these 3 different pitches to see how the guardrails perform:

1. **Test Pitch 1 (Triggers Price & Sales Call Guardrail):**
   > *"We are building an AI invoice scanner that costs $49/month and requires a 30-minute sales call to onboard."*
   > *(Expected: Sarah & David reject immediately; Alex evaluates API access).*

2. **Test Pitch 2 (Triggers Jargon Guardrail):**
   > *"We built a vector database tool that syncs via Webhooks and REST API for $10/month."*
   > *(Expected: Alex loves it; David rejects due to jargon).*

3. **Test Pitch 3 (Passes Simple Value Pitch):**
   > *"A simple 1-click receipts app for $12/month with no sales call required."*
   > *(Expected: Sarah & David consider buying; high likelihood).*
