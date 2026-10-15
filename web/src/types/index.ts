export type Market = "US" | "IN";

export interface Demographics {
  age: number;
  occupation: string;
  incomeBracket: string;
  techLiteracy: number; // 1-10
  geography: string;
  cityTier?: string;
}

export interface Psychographics {
  patienceScore: number; // 1-10
  skepticismScore: number; // 1-10
  priceCeilingMonthly: number;
  primaryPainPoint: string;
  coreValues: string[];
  statusQuoInertia: number; // 1-10
  lossAversionBias: number; // e.g. 1.5 - 2.4
  system1HabitStrength: number; // 1-10
  financialLiteracy: number; // 1-10
  liquidityCashFlowPreference: number; // 1-10
}

export interface Capabilities {
  primaryPayment: string;
  digitalAuth: string;
  mobility: string;
  eCommerceFreq: number;
  languagePref: string;
  deviceTier: string;
}

export interface Persona {
  id: string;
  name: string;
  market: Market;
  populationWeight: number; // Wi (e.g. 0.25)
  demographics: Demographics;
  psychographics: Psychographics;
  capabilities: Capabilities;
  guardrailRules: string[];
  avatarBg: string;
  avatarInitial: string;
}

export interface ScenarioPreset {
  id: string;
  title: string;
  category: string;
  market: Market;
  question: string;
  actionA: string;
  baselineB: string;
  groundTruth?: number;
  studyCitation?: string;
  tag: string;
}

export interface PersonaSimulationResult {
  personaId: string;
  personaName: string;
  personaRole: string;
  weight: number;
  decisionStance: "YES" | "NO";
  personaShift: number; // -2.0 to +2.0
  rawFriction: number;
  effectiveFriction: number;
  scaledFriction: number;
  frictionPenalty: number;
  deltaV: number;
  targetMetricScore: number; // 0-100%
  responseText: string;
  primaryObjection: string;
  dominantBottleneck: string;
  empiricalArchetype: string;
  empiricalBaseRate: number;
}

export interface SimulationResult {
  scenarioId?: string;
  question: string;
  market: Market;
  category: string;
  actionA: string;
  baselineB: string;
  empiricalBaseRate: number;
  empiricalArchetype: string;
  groundTruth?: number;
  studyCitation?: string;
  weightedScore: number; // Post-stratified
  unweightedScore: number;
  totalWeight: number;
  personaResults: PersonaSimulationResult[];
  keyThemes: string[];
  timestamp: string;
}

export interface ZoomedSubPersona {
  id: string;
  name: string;
  role: string;
  populationWeight: number;
  archetype: string;
  expressedPainPoint: string;
  priceCeiling: number;
  predictedAcceptance: number;
  edgeCaseDealbreaker: string;
}

export interface SurveyQuestion {
  id: string;
  questionText: string;
  actionA?: string;
  baselineB?: string;
  expectedOutcomes?: string;
  simulatedResult?: SimulationResult;
}

export interface SurveyStudy {
  id: string;
  title: string;
  description: string;
  market: Market;
  category: string;
  createdAt: string;
  questions: SurveyQuestion[];
}
