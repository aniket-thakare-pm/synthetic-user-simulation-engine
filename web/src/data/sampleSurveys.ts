import { SurveyStudy } from "../types";
import { runSimulation } from "../services/simulationEngine";

export const INITIAL_STUDIES: SurveyStudy[] = [
  {
    id: "study_01_pricing",
    title: "Q4 Subscription Tier & Feature Packaging Study",
    description: "Evaluating consumer trade-offs around annual pre-payments, AI add-on value perception, and ad-tier acceptance.",
    market: "US",
    category: "Digital Subscriptions",
    createdAt: "Today",
    questions: [
      {
        id: "q_01_annual",
        questionText: "Would you switch from a flexible $19/month plan to an annual $180/year plan (saving $48/year, 21% discount) if billed in a single lump sum today?",
        actionA: "Pay $180 upfront to lock in the 21% annual savings",
        baselineB: "Keep paying $19 monthly for flexibility and cash-flow control",
        expectedOutcomes: "Measures liquidity preservation vs discount arbitrage",
        simulatedResult: runSimulation({
          question: "Would you switch from a flexible $19/month plan to an annual $180/year plan (saving $48/year, 21% discount) if billed in a single lump sum today?",
          market: "US",
          actionA: "Pay $180 upfront to lock in the 21% annual savings",
          baselineB: "Keep paying $19 monthly for flexibility and cash-flow control",
        }),
      },
      {
        id: "q_02_ai_addon",
        questionText: "If an automated AI assistant add-on is offered for an extra $5/month to automate your weekly status summaries, would you pay for it or manually write them?",
        actionA: "Pay the extra $5/month for the automated AI summary add-on",
        baselineB: "Skip the add-on and continue writing summaries manually for free",
        expectedOutcomes: "Tests willingness to pay for System 2 cognitive offloading",
      },
      {
        id: "q_03_ad_tier",
        questionText: "Would you accept 30-second occasional commercial breaks in exchange for slashing your monthly subscription cost from $15 down to $7?",
        actionA: "Downgrade to the $7 ad-supported tier to cut monthly costs",
        baselineB: "Keep paying $15 for a completely clean, ad-free experience",
        expectedOutcomes: "Identifies ad-tolerance threshold vs pure convenience",
      },
    ],
  },
  {
    id: "study_02_india_fintech",
    title: "India UPI Credit Line & Daily Micro-Savings Study",
    description: "Testing merchant and consumer adoption of pre-approved UPI credit lines and automated round-up investments.",
    market: "IN",
    category: "Fintech & Credit",
    createdAt: "Yesterday",
    questions: [
      {
        id: "q_in_01_credit_line",
        questionText: "Would you use an instant pre-approved UPI Credit Line for your everyday ₹2,000 - ₹5,000 monthly grocery and shop spends if 0% interest is charged for the first 30 days?",
        actionA: "Use the 30-day 0% interest UPI Credit Line to protect liquid bank balance",
        baselineB: "Keep paying directly via savings bank debit on UPI to avoid any credit line",
        expectedOutcomes: "Tests debt aversion vs working capital smoothing",
        simulatedResult: runSimulation({
          question: "Would you use an instant pre-approved UPI Credit Line for your everyday ₹2,000 - ₹5,000 monthly grocery and shop spends if 0% interest is charged for the first 30 days?",
          market: "IN",
          actionA: "Use the 30-day 0% interest UPI Credit Line to protect liquid bank balance",
          baselineB: "Keep paying directly via savings bank debit on UPI to avoid any credit line",
        }),
      },
      {
        id: "q_in_02_refund_guarantee",
        questionText: "Would you pay a small ₹99 annual subscription fee for a guaranteed 10-second instant refund on all failed or stuck UPI transactions?",
        actionA: "Pay ₹99/year for instant refund guarantee on stuck UPI payments",
        baselineB: "Refuse the fee and wait standard 3-5 bank days for bank auto-reversal",
        expectedOutcomes: "Evaluates anxiety around digital payment failure",
      },
    ],
  },
];
