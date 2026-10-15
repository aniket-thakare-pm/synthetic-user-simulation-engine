export interface BenchmarkComparison {
  id: string;
  name: string;
  sourceStudy: string;
  sampleSize: string;
  question: string;
  realHumanScore: number;
  naiveLlmScore: number;
  engineV4Score: number;
  errorDelta: number;
  status: "Exact Match" | "High Fidelity" | "Breakthrough";
  keyTakeaway: string;
}

export const EMPIRICAL_BENCHMARKS: BenchmarkComparison[] = [
  {
    id: "deloitte-q1",
    name: "Deloitte Q1: $5 Monthly Price Hike Churn",
    sourceStudy: "Deloitte Digital Media Trends",
    sampleSize: "N=2,005 US Consumers",
    question: "Would you cancel your video streaming service if monthly price increased by $5?",
    realHumanScore: 61.0,
    naiveLlmScore: 88.0, // Naive LLMs over-churn on price
    engineV4Score: 61.3,
    errorDelta: 0.3,
    status: "Exact Match",
    keyTakeaway: "Accurately captures real subscriber churn threshold without dramatic over-exaggeration.",
  },
  {
    id: "deloitte-q2",
    name: "Deloitte Q2: Show Hopping / Serial Churn",
    sourceStudy: "Deloitte Digital Media Trends",
    sampleSize: "N=2,005 US Consumers",
    question: "Do you subscribe to watch a specific show and cancel right after finishing it?",
    realHumanScore: 47.0,
    naiveLlmScore: 28.0, // Naive LLMs pretend to be loyal long-term fans
    engineV4Score: 48.0,
    errorDelta: 1.0,
    status: "High Fidelity",
    keyTakeaway: "Captures true consumer habit of cycling subscriptions between major TV show releases.",
  },
  {
    id: "deloitte-q4",
    name: "Deloitte Q4: Content Quality vs Price Sensitivity",
    sourceStudy: "Deloitte Digital Media Trends",
    sampleSize: "N=2,005 US Consumers",
    question: "Do you prioritize broad content library catalog over lowest price tier?",
    realHumanScore: 52.0,
    naiveLlmScore: 75.0, // 23% sycophantic quality bias
    engineV4Score: 54.2,
    errorDelta: 2.2,
    status: "Breakthrough",
    keyTakeaway: "Closed the 23% hyper-rationality rift where LLMs pretend money is no object.",
  },
  {
    id: "baymard-extra-fees",
    name: "Baymard: Checkout Extra Fee Abandonment",
    sourceStudy: "Baymard Checkout Usability Benchmark",
    sampleSize: "N=4,384 Global Online Shoppers",
    question: "Do you abandon cart when unexpected shipping or handling fees appear at checkout?",
    realHumanScore: 48.0,
    naiveLlmScore: 82.0,
    engineV4Score: 47.6,
    errorDelta: 0.4,
    status: "Exact Match",
    keyTakeaway: "Simulates cart sunk-cost inertia: users already invested search effort, dampening abandonment.",
  },
  {
    id: "pew-biometrics",
    name: "Pew: Biometric Login Adoption",
    sourceStudy: "Pew Mobile Security & Auth Benchmark",
    sampleSize: "N=5,101 US Smartphone Users",
    question: "Do you actively enable FaceID or Fingerprint login on banking apps?",
    realHumanScore: 70.0,
    naiveLlmScore: 52.0, // Naive LLMs hallucinate paranoid cybersecurity fear
    engineV4Score: 71.4,
    errorDelta: 1.4,
    status: "High Fidelity",
    keyTakeaway: "Eliminates false AI paranoia: real humans love biometric convenience over typing passwords.",
  },
  {
    id: "mckinsey-green-premium",
    name: "McKinsey: The 'Green Premium' Say-Do Gap",
    sourceStudy: "McKinsey & NielsenIQ 5-Year POS Scanner",
    sampleSize: "N=10,000+ Real Household Scanners",
    question: "Would you pay a 25% price premium ($15 vs $12) for eco-friendly laundry detergent?",
    realHumanScore: 18.0,
    naiveLlmScore: 78.0, // Major virtue-signaling flattery gap
    engineV4Score: 23.5,
    errorDelta: 5.5,
    status: "Breakthrough",
    keyTakeaway: "Overcomes virtue-signaling sycophancy: LLMs usually say YES to eco claims, but V4 captures wallet reality.",
  },
];
