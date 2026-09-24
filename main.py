import os
import sys
from sample_personas import SAMPLE_PERSONAS
from persona_generator import generate_dynamic_mece_panel, generate_zoomed_subpanel
from interview_engine import interview_persona_stateless

def main():
    print("=" * 75)
    print(" 🚀 SYNTHETIC USER SIMULATION ENGINE (DIRECTIONAL VECTOR & LOGIT WEIGHTING)")
    print("=" * 75)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = input("\n🔑 Enter your Gemini API Key: ").strip()
        if not api_key:
            print("❌ Error: API Key is required.")
            sys.exit(1)
            
    print("\nSelect Persona Panel Setup Mode:")
    print("  1. Use Default 5 MECE General Panel (Accountant, Founder, Retailer, Compliance, Freelancer)")
    print("  2. Generate Custom MECE Persona Panel for ANY Domain / Product Category")
    
    choice = input("\nChoice (1 or 2, default 1): ").strip()
    
    active_panel = SAMPLE_PERSONAS
    product_context = "General B2B / Consumer Software"
    session_history = []
    
    if choice == "2":
        domain = input("\nEnter your target Domain / Product Category (e.g., 'Pet Health Tech', 'Meesho Creator Program'): ").strip()
        if domain:
            product_context = domain
            print(f"\n🔮 Generating 5 Domain-Specific MECE Personas for '{domain}'...")
            try:
                active_panel = generate_dynamic_mece_panel(domain, api_key, num_personas=5)
                print(f"✅ Successfully generated 5 tailored personas for '{domain}'!")
            except Exception as e:
                print(f"⚠️ Error generating dynamic panel: {e}. Falling back to default panel.")
                active_panel = SAMPLE_PERSONAS
                
    print(f"\n✅ Active MECE Persona Panel (N={len(active_panel)}):")
    for idx, p in enumerate(active_panel, 1):
        weight_str = f"Weight: {p.population_weight*100:.0f}%" if hasattr(p, 'population_weight') else "Weight: 20%"
        print(f"  {idx}. {p.name:<20} | Role: {p.demographics.occupation:<32} | Budget: ${p.psychographics.price_ceiling_monthly:<5}/mo | {weight_str}")
        
    print("\n" + "-" * 75)
    print("💡 TIPS: Ask problem-first discovery questions without pitching upfront!")
    print("💡 Type 'zoom' at any time to analyze expressed pain points & expand qualified personas!")
    print("-" * 75)
    
    while True:
        try:
            print("\nEnter question/pitch, 'zoom' to narrow target panel, or 'exit':")
            user_input = input("> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("Exiting engine. Goodbye!")
                break
                
            if user_input.lower() == 'zoom':
                print("\n" + "=" * 75)
                print(" 🔍 TRANSCRIPT-AWARE FUNNEL ZOOMING")
                print("=" * 75)
                print("Current Panel Personas:")
                for idx, p in enumerate(active_panel, 1):
                    print(f"  {idx}. {p.name} ({p.demographics.occupation}) - Budget: ${p.psychographics.price_ceiling_monthly}/mo")
                    
                default_selection = [1, 2] if len(active_panel) >= 2 else [1]
                default_str = ", ".join(map(str, default_selection))
                suggested_names = ", ".join([f"{i}. {active_panel[i-1].name}" for i in default_selection])
                
                print(f"\n🤖 AI Auto-Suggested Zoom Targets (Highest Pain/Fit): [{suggested_names}]")
                sel_input = input(f"Press ENTER to accept AI Auto-Suggestion [{default_str}], or enter custom numbers (e.g. 1 2 4 5 or [1, 2, 4, 5]): ").strip()
                
                # Sanitize input: remove brackets, commas, quotes
                clean_input = sel_input.replace("[", "").replace("]", "").replace(",", " ").replace("'", "").replace('"', "").strip()
                
                selected_indices = default_selection
                if clean_input:
                    try:
                        parsed = [int(x) for x in clean_input.split() if x.isdigit()]
                        valid = [i for i in parsed if 1 <= i <= len(active_panel)]
                        if valid:
                            selected_indices = valid
                    except Exception:
                        print("Invalid selection format. Using auto-suggested selection.")
                        
                selected_personas = [active_panel[i - 1] for i in selected_indices]
                selected_names = ", ".join([p.name for p in selected_personas])
                
                print(f"\n🎯 Zooming into target segment: [{selected_names}]")
                print(f"🧠 Analyzing session transcript ({len(session_history)} Q&A turns)...")
                print(f"🔮 Generating 5 Micro-MECE Sub-Personas grounded in expressed interview pain points...")
                
                try:
                    zoomed_panel = generate_zoomed_subpanel(
                        selected_personas, 
                        product_context, 
                        api_key, 
                        interview_history=session_history,
                        num_subpersonas=5
                    )
                    active_panel = zoomed_panel
                    print(f"✅ Successfully expanded into 5 Micro-MECE Sub-Personas grounded in interview responses!")
                    print("\nNew Active Zoomed Sub-Panel:")
                    for idx, p in enumerate(active_panel, 1):
                        print(f"  {idx}. {p.name:<20} | Role: {p.demographics.occupation:<32} | Budget: ${p.psychographics.price_ceiling_monthly:<5}/mo")
                except Exception as e:
                    print(f"❌ Error generating zoomed panel: {e}")
                    
                print("-" * 75)
                continue
                
            print("\n" + "=" * 75)
            print(f" PANEL RESPONSES (N={len(active_panel)}) — DIRECTIONAL VECTOR LOGIT MODEL ⚡")
            print("=" * 75)
            
            from concurrent.futures import ThreadPoolExecutor
            
            def process_persona(persona):
                try:
                    res = interview_persona_stateless(persona, user_input, api_key)
                    return (persona, res, None)
                except Exception as e:
                    return (persona, None, str(e))

            with ThreadPoolExecutor(max_workers=len(active_panel)) as executor:
                results = list(executor.map(process_persona, active_panel))

            valid_responses = []
            for persona, response, err in results:
                weight_pct = int(persona.population_weight * 100) if hasattr(persona, 'population_weight') else 20
                print(f"\n👤 [{persona.name}] — {persona.demographics.occupation} (Population Weight: {weight_pct}%)")
                if err:
                    print(f"❌ Error interviewing {persona.name}: {err}")
                else:
                    valid_responses.append(response)
                    if response.deterministic_rule_triggered:
                        print(f"⚡ {response.deterministic_rule_triggered}")
                        
                    print(f"   🔹 Majority Stance [{response.majority_percent}% {response.primary_action_direction}]: {response.majority_response}")
                    print(f"   🔸 Minority Stance [{response.minority_percent}%]: {response.minority_exception}")
                    print(f"   📉 Persona Normalized Churn/Rejection Rate: {response.churn_or_rejection_percent}%")
                    print(f"   💬 Persona Summary: \"{response.response_text}\"")
                    
                    if response.primary_objection:
                        print(f"   🚩 Concern: {response.primary_objection}")
                        
                    session_history.append({
                        "question": user_input,
                        "persona_name": persona.name,
                        "response_text": response.response_text,
                        "primary_objection": response.primary_objection,
                        "majority_percent": response.majority_percent,
                        "churn_or_rejection_percent": response.churn_or_rejection_percent
                    })
                    
                print("-" * 75)
                
            if valid_responses:
                total_w = sum(r.population_weight for r in valid_responses)
                unweighted_avg_churn = sum(r.churn_or_rejection_percent for r in valid_responses) / len(valid_responses)
                weighted_churn_score = sum(r.population_weight * r.churn_or_rejection_percent for r in valid_responses) / total_w if total_w > 0 else 0
                
                print(f"\n📊 POST-STRATIFIED WEIGHTED MARKET ANALYSIS (N={len(valid_responses)}):")
                print(f"   📉 Unweighted Average Churn/Rejection Rate: {unweighted_avg_churn:.1f}%")
                print(f"   🎯 Post-Stratified Weighted Churn/Rejection Score (Wi): {weighted_churn_score:.1f}%")
                print("=" * 75)
                
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
