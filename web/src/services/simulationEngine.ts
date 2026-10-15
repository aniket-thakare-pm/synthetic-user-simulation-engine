import {
  Market,
  Persona,
  PersonaSimulationResult,
  SimulationResult,
  ZoomedSubPersona,
} from "../types";
import { US_PERSONAS, IN_PERSONAS } from "../data/personas";
import { SCENARIO_PRESETS } from "../data/scenarios";

// Empirical reference base rates and log-odds
interface EmpiricalRef {
  key: string;
  name: string;
  pRef: number;
  v0: number;
  lossLambda: number;
  frictionScale: number;
}

const EMPIRICAL_REFS: Record<string, EmpiricalRef> = {
  STREAMING_PRICE_HIKE: {
    key: "STREAMING_PRICE_HIKE",
    name: "Subscription Price Hike Churn",
    pRef: 0.61,
    v0: 0.4473,
    lossLambda: 1.95,
    frictionScale: 1.0,
  },
  STREAMING_SERIAL_CHURN: {
    key: "STREAMING_SERIAL_CHURN",
    name: "Show Hopping / Serial Churn",
    pRef: 0.47,
    v0: -0.1201,
    lossLambda: 1.55,
    frictionScale: 0.65,
  },
  CHECKOUT_SURPRISE_FEE: {
    key: "CHECKOUT_SURPRISE_FEE",
    name: "Unexpected Extra Fees at Checkout",
    pRef: 0.48,
    v0: -0.08,
    lossLambda: 2.35,
    frictionScale: 1.0,
  },
  GREEN_PREMIUM_PARADOX: {
    key: "GREEN_PREMIUM_PARADOX",
    name: "Say-Do Green Premium Dilemma",
    pRef: 0.18,
    v0: -1.5163,
    lossLambda: 2.4,
    frictionScale: 0.9,
  },
  BAG_FEE_LOSS_AVERSION: {
    key: "BAG_FEE_LOSS_AVERSION",
    name: "10-Cent Plastic Bag Fee Penalty",
    pRef: 0.81,
    v0: 1.45,
    lossLambda: 2.3,
    frictionScale: 0.7,
  },
  INDIA_FINTECH_EMI: {
    key: "INDIA_FINTECH_EMI",
    name: "0% No-Cost EMI Cash Flow Protection",
    pRef: 0.62,
    v0: 0.4895,
    lossLambda: 1.85,
    frictionScale: 0.8,
  },
  INDIA_HEALTH_TELEMED: {
    key: "INDIA_HEALTH_TELEMED",
    name: "Institutional Clinic Trust vs Telemed",
    pRef: 0.44,
    v0: -0.2412,
    lossLambda: 2.25,
    frictionScale: 1.0,
  },
  INDIA_MOBILITY_EV: {
    key: "INDIA_MOBILITY_EV",
    name: "EV Two-Wheeler Hardware Adoption",
    pRef: 0.54,
    v0: 0.1603,
    lossLambda: 2.1,
    frictionScale: 0.9,
  },
  GENERIC_INNOVATION: {
    key: "GENERIC_INNOVATION",
    name: "General Consumer Adoption Baseline",
    pRef: 0.42,
    v0: -0.3228,
    lossLambda: 2.0,
    frictionScale: 0.85,
  },
};

function detectEmpiricalArchetype(question: string): EmpiricalRef {
  const q = question.toLowerCase();
  if (q.includes("$5") || q.includes("price increase") || q.includes("price hike")) {
    return EMPIRICAL_REFS.STREAMING_PRICE_HIKE;
  }
  if (q.includes("specific movie") || q.includes("show hopping") || q.includes("binge")) {
    return EMPIRICAL_REFS.STREAMING_SERIAL_CHURN;
  }
  if (q.includes("eco-friendly") || q.includes("detergent") || q.includes("green")) {
    return EMPIRICAL_REFS.GREEN_PREMIUM_PARADOX;
  }
  if (q.includes("plastic bag") || q.includes("bag fee") || q.includes("10-cent")) {
    return EMPIRICAL_REFS.BAG_FEE_LOSS_AVERSION;
  }
  if (q.includes("checkout") || q.includes("shipping") || q.includes("extra cost") || q.includes("unexpected charge")) {
    return EMPIRICAL_REFS.CHECKOUT_SURPRISE_FEE;
  }
  if (q.includes("emi") || q.includes("bnpl") || q.includes("no-cost")) {
    return EMPIRICAL_REFS.INDIA_FINTECH_EMI;
  }
  if (q.includes("telemedicine") || q.includes("doctor") || q.includes("fever") || q.includes("clinic")) {
    return EMPIRICAL_REFS.INDIA_HEALTH_TELEMED;
  }
  if (q.includes("electric") || q.includes("scooter") || q.includes("ev ") || q.includes("2-wheeler")) {
    return EMPIRICAL_REFS.INDIA_MOBILITY_EV;
  }
  return EMPIRICAL_REFS.GENERIC_INNOVATION;
}

export function simulatePersonaResponse(
  persona: Persona,
  question: string,
  actionA: string,
  baselineB: string,
  ref: EmpiricalRef
): PersonaSimulationResult {
  const p = persona;
  const psy = p.psychographics;
  const demo = p.demographics;
  const q = question.toLowerCase();

  // 1. Calculate Persona Idiosyncratic Shift (Δvp in [-2.0, +2.0])
  let shift = 0.0;
  let rawFriction = 3.5;
  let responseText = "";
  let primaryObjection = "";
  let dominantBottleneck = "Setup & Habit Inertia";

  // Check specific domain scenarios
  if (ref.key === "STREAMING_PRICE_HIKE") {
    if (p.id === "p_us_01_sarah") {
      shift = -1.6;
      rawFriction = 2.0;
      dominantBottleneck = "Unannounced Budget Inflation";
      primaryObjection = "Hidden price creeps violate household spreadsheet limits.";
      responseText =
        "A $5 monthly hike across 12 months is $60 a year. I audit every digital recurring line item, and this pushes my streaming budget past my $25 ceiling. I am canceling immediately.";
    } else if (p.id === "p_us_02_alex") {
      shift = 1.2;
      rawFriction = 1.0;
      dominantBottleneck = "Time Loss over Money";
      primaryObjection = "None - high income absorbs minor fee delta.";
      responseText =
        "I honestly wouldn't even notice the five dollars on my autopay Apple Card. Canceling and figuring out where else to watch shows wastes more billable developer hours than $5.";
    } else if (p.id === "p_us_03_david") {
      shift = -1.8;
      rawFriction = 3.0;
      dominantBottleneck = "Fixed Income Breach";
      primaryObjection = "Sudden price jumps feel manipulative for retirees on fixed pensions.";
      responseText =
        "I live on a fixed retirement income. If companies can bump prices by five dollars whenever they please, they don't value loyal customers. I'll have my daughter help me cancel it.";
    } else if (p.id === "p_us_04_elena") {
      shift = -0.4;
      rawFriction = 4.0;
      dominantBottleneck = "Kids Daily Routine Disruption";
      primaryObjection = "Kids watch daily, but $5 pushes total entertainment bill above $50.";
      responseText =
        "I'd hesitate because the kids watch cartoons after school, but five dollars more is getting ridiculous. I would probably downgrade to their cheaper ad-supported tier instead of canceling outright.";
    } else if (p.id === "p_us_05_marcus") {
      shift = -1.9;
      rawFriction = 1.5;
      dominantBottleneck = "Zero Disposable Buffer";
      primaryObjection = "College student budget has zero tolerance for price hikes.";
      responseText =
        "Five bucks is an entire lunch on campus! The moment they hike it, I'm dropping the subscription and borrowing my roommate's login or switching back to YouTube.";
    }
  } else if (ref.key === "GREEN_PREMIUM_PARADOX") {
    if (p.id === "p_us_01_sarah") {
      shift = -1.8;
      rawFriction = 2.0;
      dominantBottleneck = "Budget Margin Defense";
      primaryObjection = "25% green premium is financially unjustified for a basic consumable.";
      responseText =
        "Paying 25% extra for detergent that does the exact same cleaning job is a gimmick. I care about the planet, but paying a corporate 'green markup' on laundry ruins my monthly margin.";
    } else if (p.id === "p_us_02_alex") {
      shift = 0.8;
      rawFriction = 2.0;
      dominantBottleneck = "Minimalist Packaging Preference";
      primaryObjection = "Minor cost difference; appreciates zero plastic.";
      responseText =
        "On a $130k salary, three dollars extra per month is negligible. I hate bulky plastic detergent jugs cluttering my apartment, so the compact eco-packaging is worth it to me.";
    } else if (p.id === "p_us_03_david") {
      shift = -1.7;
      rawFriction = 3.5;
      dominantBottleneck = "Unknown Chemical Efficacy Risk";
      primaryObjection = "Unproven cleaning power vs reliable legacy brand.";
      responseText =
        "I've used Tide for thirty years. Why would I pay three dollars more for a brand I've never heard of that might ruin my shirts in the wash?";
    } else if (p.id === "p_us_04_elena") {
      shift = -1.2;
      rawFriction = 2.5;
      dominantBottleneck = "High Volume Family Cost";
      primaryObjection = "Running 7 loads of laundry a week multiplies the premium.";
      responseText =
        "With two kids playing sports, I do laundry practically every single night. Three dollars extra per bottle adds up to $30 a month. I have to stick with the regular $12 brand.";
    } else if (p.id === "p_us_05_marcus") {
      shift = -1.9;
      rawFriction = 1.0;
      dominantBottleneck = "Immediate Cash Scarcity";
      primaryObjection = "Cannot afford luxury environmentalism on student budget.";
      responseText =
        "I want to support zero-plastic, but I have $40 left in my checking account this week. I'm buying the $12 detergent every single time.";
    }
  } else if (ref.key === "INDIA_FINTECH_EMI") {
    if (p.id === "p_in_01_ramesh") {
      shift = 1.5;
      rawFriction = 2.0;
      dominantBottleneck = "Preserving Kirana Cash Flow";
      primaryObjection = "Accepts enthusiastically ONLY if truly 0% zero processing fee.";
      responseText =
        "Agar sach me zero interest aur zero file charge hai, toh ₹25,000 ek saath kyu block karu? Shop me rotation ke liye cash chahiye. ₹4,166 har mahine PhonePe se aaram se de dunga.";
    } else if (p.id === "p_in_02_priya") {
      shift = 1.7;
      rawFriction = 1.0;
      dominantBottleneck = "Arbitrage & Credit Rewards";
      primaryObjection = "None - standard personal finance optimization.";
      responseText =
        "I always take genuine 0% No-Cost EMI on my HDFC card. Leaving ₹25,000 invested in my liquid mutual funds yields return while paying ₹4k a month with zero penalty.";
    } else if (p.id === "p_in_03_ananya") {
      shift = 1.8;
      rawFriction = 1.5;
      dominantBottleneck = "Affordability Gap";
      primaryObjection = "Can only purchase high-end design gadgets via monthly splits.";
      responseText =
        "I don't have ₹25,000 in my account right now! ₹4,100 a month from my freelance illustrations makes it instantly doable. Without EMI I wouldn't even be able to buy it.";
    } else if (p.id === "p_in_04_suresh") {
      shift = -1.6;
      rawFriction = 6.0;
      dominantBottleneck = "Debt Anxiety & Hidden Fine Print";
      primaryObjection = "Deep distrust of non-bank NBFC debt and recurring ECS mandates.";
      responseText =
        "Koshish karo ki udhaar par na jiyo. Ye No-Cost EMI bolte hain, baad me hidden GST aur processing fee kaat lete hain. Main ek baar me SBI debit card se full payment karunga.";
    } else if (p.id === "p_in_05_kavita") {
      shift = 0.4;
      rawFriction = 3.0;
      dominantBottleneck = "Statement Clutter";
      primaryObjection = "Only takes it if corporate card offers clean invoice reconciliation.";
      responseText =
        "I can pay upfront easily, but 0% EMI is good for cash flow smoothing. If the checkout invoice is clean and has no auto-debit hassle, I'll take the 6-month split.";
    }
  } else if (ref.key === "INDIA_HEALTH_TELEMED") {
    if (p.id === "p_in_01_ramesh") {
      shift = -1.6;
      rawFriction = 6.5;
      dominantBottleneck = "Physical Stethoscope & Hand Touch";
      primaryObjection = "Screen cannot physically touch or check chest/fever.";
      responseText =
        "Mobile screen pe doctor naadi kaise dekhega? Gala dekhne ke liye light chahiye, chest check karne ke liye stethoscope chahiye. ₹299 online waste karne se achha apne Sharma clinic jaunga.";
    } else if (p.id === "p_in_02_priya") {
      shift = 1.5;
      rawFriction = 1.5;
      dominantBottleneck = "Time Preservation";
      primaryObjection = "None for common fever; skips 2-hour traffic jams.";
      responseText =
        "For a simple recurring cold or fever, sitting in Bangalore traffic and waiting an hour in a clinic waiting room is madness. I'll take the 15-minute video consult and get meds delivered via Zepto.";
    } else if (p.id === "p_in_03_ananya") {
      shift = 1.1;
      rawFriction = 2.0;
      dominantBottleneck = "Clinic Waiting Friction";
      primaryObjection = "Hates awkward waiting room small talk.";
      responseText =
        "₹299 from my bed in pajamas is way better than walking to a clinic and sitting with twenty coughing patients. I'll do the video consult first.";
    } else if (p.id === "p_in_04_suresh") {
      shift = -1.9;
      rawFriction = 8.0;
      dominantBottleneck = "Clinical Accountability Failure";
      primaryObjection = "Zero legal recourse if an unknown video app doctor misdiagnoses.";
      responseText =
        "Swasthya ke mamle me online prayog nahi karna chahiye. Mera family doctor pichle 20 saal se hamari medical history jaanta hai. Online doctor galat dava likh dega toh kaun zimmedar hoga?";
    } else if (p.id === "p_in_05_kavita") {
      shift = -0.5;
      rawFriction = 4.5;
      dominantBottleneck = "Diagnostic Accuracy Doubt";
      primaryObjection = "Prefers video for prescription refill, but clinic for diagnosis.";
      responseText =
        "If it's just a routine throat infection, video consult is convenient. But if the fever is recurring, you need a proper blood test and throat swab. I lean toward the clinic for peace of mind.";
    }
  } else {
    // Dynamic synthesis for custom questions
    const isSkeptic = psy.skepticismScore >= 7;
    const isImpatient = psy.patienceScore <= 3;
    const isHighTech = demo.techLiteracy >= 7;
    const isBudgetConstrained = psy.priceCeilingMonthly < 30 || demo.incomeBracket.includes("Low");

    if (q.includes("free") || q.includes("discount") || q.includes("save")) {
      shift = isBudgetConstrained ? 1.4 : 0.4;
      rawFriction = isHighTech ? 1.5 : 4.0;
      dominantBottleneck = "Setup Friction vs Financial Upside";
      primaryObjection = "Needs to ensure no hidden fine-print or trial auto-debits.";
      responseText = `As ${p.name}, I am receptive to genuine cost savings, but I am auditing whether the hassle of switching or learning a new system outweighs the few dollars saved.`;
    } else if (q.includes("ai") || q.includes("automatic") || q.includes("algorithm")) {
      shift = isHighTech ? 1.2 : -1.5;
      rawFriction = isHighTech ? 2.0 : 7.0;
      dominantBottleneck = isHighTech ? "Algorithm Transparency" : "Human Recourse Need";
      primaryObjection = isHighTech ? "Speed matters most." : "Lack of human accountability when errors happen.";
      responseText = `I evaluate automated tools through my lens as ${demo.occupation}. ${isHighTech ? "I appreciate rapid automation as long as I have override control." : "I distrust black-box algorithms taking critical decisions without a live human to hold accountable."}`;
    } else {
      shift = isSkeptic ? -1.0 : (isImpatient ? 0.8 : 0.0);
      rawFriction = isHighTech ? 2.5 : 5.5;
      dominantBottleneck = "Behavioral Inertia & Routine";
      primaryObjection = psy.primaryPainPoint;
      responseText = `In my day-to-day routine as ${demo.occupation}, my default is to stick with what already works. Unless this clearly solves my frustration around "${psy.primaryPainPoint}", I'm not changing my habits.`;
    }
  }

  // 2. Mental Accounting Effective Friction (F_eff)
  const fScaled = rawFriction * ref.frictionScale;
  const frictionPenalty = (fScaled / 10.0) * ref.lossLambda;

  // 3. McFadden Logit Utility Formulation (k = 1.0, beta = 0.25)
  // deltaV = V_0 + (beta * shift) - (F_scaled / 10.0 * 0.15 * lambda)
  const beta = 0.25;
  const scaledPenalty = (fScaled / 10.0) * 0.15 * ref.lossLambda;
  const deltaV = ref.v0 + (beta * shift) - scaledPenalty;

  // Probability via Logit Choice
  const prob = (1.0 / (1.0 + Math.exp(-1.0 * deltaV))) * 100.0;
  const clampedProb = Math.round(Math.max(5.0, Math.min(95.0, prob)) * 10) / 10;
  const stance: "YES" | "NO" = clampedProb >= 50.0 ? "YES" : "NO";

  return {
    personaId: p.id,
    personaName: p.name,
    personaRole: p.demographics.occupation,
    weight: p.populationWeight,
    decisionStance: stance,
    personaShift: Math.round(shift * 10) / 10,
    rawFriction,
    effectiveFriction: Math.round(rawFriction * 10) / 10,
    scaledFriction: Math.round(fScaled * 10) / 10,
    frictionPenalty: Math.round(frictionPenalty * 100) / 100,
    deltaV: Math.round(deltaV * 100) / 100,
    targetMetricScore: clampedProb,
    responseText,
    primaryObjection,
    dominantBottleneck,
    empiricalArchetype: ref.key,
    empiricalBaseRate: Math.round(ref.pRef * 1000) / 10,
  };
}

export function runSimulation(params: {
  question: string;
  market?: Market;
  category?: string;
  actionA?: string;
  baselineB?: string;
  presetId?: string;
}): SimulationResult {
  const { question, presetId } = params;
  const preset = presetId ? SCENARIO_PRESETS.find((s) => s.id === presetId) : undefined;

  // Resolve Market (US or India)
  let market: Market = params.market || "US";
  if (!params.market) {
    const qLower = question.toLowerCase();
    if (
      qLower.includes("₹") ||
      qLower.includes("rupee") ||
      qLower.includes("upi") ||
      qLower.includes("phonepe") ||
      qLower.includes("paytm") ||
      qLower.includes("india") ||
      qLower.includes("tier-") ||
      qLower.includes("kirana")
    ) {
      market = "IN";
    }
  }

  const activePanel = market === "IN" ? IN_PERSONAS : US_PERSONAS;
  const empiricalRef = detectEmpiricalArchetype(question);

  const actionA = params.actionA || preset?.actionA || "Choose Option A (adopt innovation / take target action)";
  const baselineB = params.baselineB || preset?.baselineB || "Choose Option B (retain existing baseline / status quo)";

  const personaResults: PersonaSimulationResult[] = activePanel.map((p) =>
    simulatePersonaResponse(p, question, actionA, baselineB, empiricalRef)
  );

  // Compute Post-Stratified Weighted Score (Wi)
  let totalWeight = 0;
  let weightedSum = 0;
  let unweightedSum = 0;

  personaResults.forEach((r) => {
    weightedSum += r.targetMetricScore * r.weight;
    totalWeight += r.weight;
    unweightedSum += r.targetMetricScore;
  });

  const weightedScore = Math.round((weightedSum / (totalWeight || 1)) * 10) / 10;
  const unweightedScore = Math.round((unweightedSum / personaResults.length) * 10) / 10;

  // Extract Key Themes
  const themes = Array.from(
    new Set(personaResults.map((r) => r.dominantBottleneck).filter(Boolean))
  );

  return {
    scenarioId: preset?.id,
    question,
    market,
    category: params.category || preset?.category || "Consumer Decision",
    actionA,
    baselineB,
    empiricalBaseRate: Math.round(empiricalRef.pRef * 1000) / 10,
    empiricalArchetype: empiricalRef.name,
    groundTruth: preset?.groundTruth,
    studyCitation: preset?.studyCitation,
    weightedScore,
    unweightedScore,
    totalWeight: Math.round(totalWeight * 100) / 100,
    personaResults,
    keyThemes: themes,
    timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  };
}

export function generateZoomPanel(result: SimulationResult): ZoomedSubPersona[] {
  const isIndia = result.market === "IN";

  if (isIndia) {
    return [
      {
        id: "zp_01",
        name: "Vikram Mehta",
        role: "Multi-Store Wholesale Merchant",
        populationWeight: 0.25,
        archetype: "High-Volume Liquidity Maximizer",
        expressedPainPoint: "Needs instant reconciliation with tally accounting software.",
        priceCeiling: 2500,
        predictedAcceptance: 74.0,
        edgeCaseDealbreaker: "Any settlement delay exceeding 24 hours.",
      },
      {
        id: "zp_02",
        name: "Neha Kulkarni",
        role: "Fintech Growth Marketer",
        populationWeight: 0.25,
        archetype: "Frictionless Power User",
        expressedPainPoint: "Will drop app if KYC requires paper document upload.",
        priceCeiling: 4500,
        predictedAcceptance: 82.0,
        edgeCaseDealbreaker: "Manual video call verification during office hours.",
      },
      {
        id: "zp_03",
        name: "Deepak Sharma",
        role: "Independent Freelance Video Editor",
        populationWeight: 0.2,
        archetype: "Irregular Income Earner",
        expressedPainPoint: "Cannot commit to rigid calendar monthly deduction dates.",
        priceCeiling: 1200,
        predictedAcceptance: 58.0,
        edgeCaseDealbreaker: "Inflexible penalty charges if bank account dips below minimum.",
      },
      {
        id: "zp_04",
        name: "Sunita Agarwal",
        role: "Homemaker & Family Budget Planner",
        populationWeight: 0.15,
        archetype: "Household Joint Account Keeper",
        expressedPainPoint: "Requires joint SMS notification to husband for every debit.",
        priceCeiling: 800,
        predictedAcceptance: 42.0,
        edgeCaseDealbreaker: "Hidden processing fees or complex English terminology.",
      },
      {
        id: "zp_05",
        name: "Harshil Roy",
        role: "Tier-2 College Tech Lead",
        populationWeight: 0.15,
        archetype: "Discount Arbitrage Hunter",
        expressedPainPoint: "Actively stacks coupons, referral codes, and zero-fee hacks.",
        priceCeiling: 500,
        predictedAcceptance: 68.0,
        edgeCaseDealbreaker: "Paywalls that block access to core features.",
      },
    ];
  }

  return [
    {
      id: "zp_01",
      name: "Taylor Scott",
      role: "Operations Manager [Power User]",
      populationWeight: 0.25,
      archetype: "Workflow Efficiency Stickler",
      expressedPainPoint: "Hates having to switch between separate screens for status tracking.",
      priceCeiling: 45,
      predictedAcceptance: 68.0,
      edgeCaseDealbreaker: "Lack of exportable CSV / Google Sheets reports.",
    },
    {
      id: "zp_02",
      name: "Chloe Bennett",
      role: "Solo Creator & Remote Consultant",
      populationWeight: 0.2,
      archetype: "Zero-Overhead Minimalist",
      expressedPainPoint: "Cannot afford high tier monthly retainers during dry client months.",
      priceCeiling: 20,
      predictedAcceptance: 72.0,
      edgeCaseDealbreaker: "Annual-only billing locks without monthly opt-out.",
    },
    {
      id: "zp_03",
      name: "Robert Hughes",
      role: "Senior Enterprise Procurement Officer",
      populationWeight: 0.2,
      archetype: "Compliance & Security Auditor",
      expressedPainPoint: "Requires vendor SOC-2 verification before approving payment.",
      priceCeiling: 150,
      predictedAcceptance: 34.0,
      edgeCaseDealbreaker: "Unclear data retention and auto-renew clauses.",
    },
    {
      id: "zp_04",
      name: "Maya Lin",
      role: "Mobile-Only Remote Freelancer",
      populationWeight: 0.2,
      archetype: "Smartphone Native",
      expressedPainPoint: "Refuses to log in on desktop to execute basic tasks.",
      priceCeiling: 15,
      predictedAcceptance: 55.0,
      edgeCaseDealbreaker: "Unresponsive mobile web interface requiring zoom.",
    },
    {
      id: "zp_05",
      name: "Gordon Vance",
      role: "Frugal Small Business Owner",
      populationWeight: 0.15,
      archetype: "Bottom-Line Protector",
      expressedPainPoint: "Questions why software costs increase faster than inflation.",
      priceCeiling: 25,
      predictedAcceptance: 38.0,
      edgeCaseDealbreaker: "Sudden mandatory add-ons for customer support.",
    },
  ];
}
