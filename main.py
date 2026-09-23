import os
import sys
from sample_personas import SAMPLE_PERSONAS
from persona_generator import generate_dynamic_mece_panel, generate_zoomed_subpanel
from interview_engine import interview_persona_stateless

def main():
    print("=" * 75)
    print(" 🚀 SYNTHETIC USER SIMULATION ENGINE (HYBRID FUNNEL ZOOMING)")
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
        print(f"  {idx}. {p.name:<20} | Role: {p.demographics.occupation:<32} | Budget: ${p.psychographics.price_ceiling_monthly:<5}/mo")
        
    print("\n" + "-" * 75)
    print("💡 TIPS: Type your question to interview the panel.")
    print("💡 Type 'zoom' at any time to drop non-buyers & expand interested personas into 5 sub-personas!")
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
                print(" 🔍 FUNNEL ZOOMING: SUB-SEGMENTATION SELECTION")
                print("=" * 75)
                print("Current Panel Personas:")
                for idx, p in enumerate(active_panel, 1):
                    print(f"  {idx}. {p.name} ({p.demographics.occupation}) - Budget: ${p.psychographics.price_ceiling_monthly}/mo")
                    
                default_selection = [1, 2] if len(active_panel) >= 2 else [1]
                default_str = ", ".join(map(str, default_selection))
                
                sel_input = input(f"\nEnter persona numbers to zoom into (Press ENTER for default [{default_str}]): ").strip()
                
                selected_indices = default_selection
                if sel_input:
                    try:
                        parsed = [int(x.strip()) for x in sel_input.replace(",", " ").split() if x.strip().isdigit()]
                        valid = [i for i in parsed if 1 <= i <= len(active_panel)]
                        if valid:
                            selected_indices = valid
                    except Exception:
                        print("Invalid selection. Using default selection.")
                        
                selected_personas = [active_panel[i - 1] for i in selected_indices]
                selected_names = ", ".join([p.name for p in selected_personas])
                
                print(f"\n🎯 Zooming into target segment: [{selected_names}]")
                print(f"🔮 Generating 5 Micro-MECE Sub-Personas for '{product_context}'...")
                
                try:
                    zoomed_panel = generate_zoomed_subpanel(selected_personas, product_context, api_key, num_subpersonas=5)
                    active_panel = zoomed_panel
                    print(f"✅ Successfully expanded into 5 Micro-MECE Sub-Personas!")
                    print("\nNew Active Zoomed Sub-Panel:")
                    for idx, p in enumerate(active_panel, 1):
                        print(f"  {idx}. {p.name:<20} | Role: {p.demographics.occupation:<32} | Budget: ${p.psychographics.price_ceiling_monthly:<5}/mo")
                except Exception as e:
                    print(f"❌ Error generating zoomed panel: {e}")
                    
                print("-" * 75)
                continue
                
            print("\n" + "=" * 75)
            print(f" PANEL RESPONSES (N={len(active_panel)})")
            print("=" * 75)
            
            for persona in active_panel:
                print(f"\n👤 [{persona.name}] — {persona.demographics.occupation}")
                
                try:
                    response = interview_persona_stateless(persona, user_input, api_key)
                    
                    if response.deterministic_rule_triggered:
                        print(f"⚡ {response.deterministic_rule_triggered}")
                        
                    print(f"   \"{response.response_text}\"")
                    
                    if response.primary_objection:
                        print(f"   🚩 Concern: {response.primary_objection}")
                        
                except Exception as e:
                    print(f"❌ Error interviewing {persona.name}: {e}")
                    
                print("-" * 75)
                
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
