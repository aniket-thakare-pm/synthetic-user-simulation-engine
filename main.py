import os
import sys
from sample_personas import SAMPLE_PERSONAS
from persona_generator import generate_dynamic_mece_panel
from interview_engine import interview_persona_stateless

def main():
    print("=" * 75)
    print(" 🚀 SYNTHETIC USER SIMULATION ENGINE (DYNAMIC MECE PANEL)")
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
    
    if choice == "2":
        domain = input("\nEnter your target Domain / Product Category (e.g., 'Pet Health Tech', 'Crypto Trading', 'Fitness'): ").strip()
        if domain:
            print(f"\n🔮 Generating 5 Domain-Specific MECE Personas for '{domain}'...")
            try:
                active_panel = generate_dynamic_mece_panel(domain, api_key, num_personas=5)
                print(f"✅ Successfully generated 5 tailored personas for '{domain}'!")
            except Exception as e:
                print(f"⚠️ Error generating dynamic panel: {e}. Falling back to default panel.")
                active_panel = SAMPLE_PERSONAS
                
    print(f"\n✅ Active MECE Persona Panel (N={len(active_panel)}):")
    for p in active_panel:
        print(f"  • {p.name:<20} | Role: {p.demographics.occupation:<30} | Budget Cap: ${p.psychographics.price_ceiling_monthly:<5}/mo | Skepticism: {p.psychographics.skepticism_score}/10")
        
    print("\n" + "-" * 75)
    
    while True:
        try:
            print("\nEnter any interview question or product pitch (or 'exit'):")
            user_input = input("> ").strip()
            
            if not user_input or user_input.lower() == 'exit':
                print("Exiting engine. Goodbye!")
                break
                
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
