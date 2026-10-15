"use client";

import React, { useState } from "react";
import { Market, Persona, SimulationResult, ScenarioPreset } from "../types";
import { SCENARIO_PRESETS } from "../data/scenarios";
import { US_PERSONAS, IN_PERSONAS } from "../data/personas";
import { runSimulation } from "../services/simulationEngine";
import { PersonaCard } from "./PersonaCard";
import { MacroMetricsView } from "./MacroMetricsView";
import { Play, Sparkles, RefreshCw, SlidersHorizontal, BookOpen } from "lucide-react";

interface SimulationStudioProps {
  market: Market;
  onOpenZoom: (result: SimulationResult) => void;
  lastResult?: SimulationResult;
  setLastResult: (res: SimulationResult) => void;
}

export function SimulationStudio({ market, onOpenZoom, lastResult, setLastResult }: SimulationStudioProps) {
  const [selectedPresetId, setSelectedPresetId] = useState<string>("deloitte-q1");
  const [customQuestion, setCustomQuestion] = useState<string>(
    "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month, and why?"
  );
  const [customActionA, setCustomActionA] = useState<string>("Cancel subscription immediately due to $5/mo hike");
  const [customBaselineB, setCustomBaselineB] = useState<string>("Absorb the $5 increase and keep streaming service");
  const [showAdvancedInputs, setShowAdvancedInputs] = useState<boolean>(false);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [simulationStepText, setSimulationStepText] = useState<string>("");

  const activePersonas: Persona[] = market === "IN" ? IN_PERSONAS : US_PERSONAS;
  const filteredPresets: ScenarioPreset[] = SCENARIO_PRESETS.filter((p) => p.market === market);

  // Initialize result if not present
  React.useEffect(() => {
    if (!lastResult) {
      const initial = runSimulation({
        question: customQuestion,
        market,
        presetId: selectedPresetId,
        actionA: customActionA,
        baselineB: customBaselineB,
      });
      setLastResult(initial);
    }
  }, []);

  const handleSelectPreset = (preset: ScenarioPreset) => {
    setSelectedPresetId(preset.id);
    setCustomQuestion(preset.question);
    setCustomActionA(preset.actionA);
    setCustomBaselineB(preset.baselineB);
  };

  const handleExecuteSimulation = () => {
    setIsSimulating(true);
    setSimulationStepText("Resolving Thaler mental account category...");

    setTimeout(() => {
      setSimulationStepText("Anchoring on Psych-101 literature base rates (V_0)...");
    }, 400);

    setTimeout(() => {
      setSimulationStepText("Calculating Dominant Bottleneck RMS friction & loss aversion (λ)...");
    }, 800);

    setTimeout(() => {
      setSimulationStepText("Executing McFadden Logit utility equations across 5 MECE personas...");
    }, 1200);

    setTimeout(() => {
      const res = runSimulation({
        question: customQuestion,
        market,
        actionA: customActionA,
        baselineB: customBaselineB,
        presetId: selectedPresetId,
      });
      setLastResult(res);
      setIsSimulating(false);
    }, 1600);
  };

  return (
    <div className="space-y-6">
      {/* Studio Control Console */}
      <div className="bg-white border border-stone-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div>
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-md flex items-center space-x-1">
              <Sparkles className="w-3.5 h-3.5 text-stone-600" />
              <span>Survey Testing Sandbox</span>
            </span>
            <span className="text-xs text-stone-500">
              Active Cohort: <strong className="text-stone-800">{market === "IN" ? "India Mass Market" : "US National Cohort"}</strong>
            </span>
          </div>
          <h2 className="text-lg sm:text-xl font-bold text-stone-900 mt-1.5">
            Rapid Single-Question Sandbox & Benchmark Verification
          </h2>
          <p className="text-xs text-stone-500 mt-0.5">
            Test published benchmark scenarios or run quick single-turn discovery questions through the EB-DCA choice model.
          </p>
        </div>

        {/* Preset Selector Chips */}
        <div>
          <div className="text-xs font-semibold text-stone-700 mb-2 flex items-center space-x-1.5">
            <BookOpen className="w-3.5 h-3.5 text-stone-600" />
            <span>Benchmark Presets ({market === "IN" ? "India Studies" : "US / Global Studies"}):</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {filteredPresets.map((preset) => (
              <button
                key={preset.id}
                onClick={() => handleSelectPreset(preset)}
                className={`text-xs px-3 py-1.5 rounded-lg font-medium transition flex items-center space-x-1.5 border ${
                  selectedPresetId === preset.id
                    ? "bg-stone-900 border-stone-900 text-white shadow-xs"
                    : "bg-white text-stone-700 border-stone-200 hover:border-stone-300"
                }`}
              >
                <span>{preset.title}</span>
                {preset.groundTruth && (
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold border ${
                    selectedPresetId === preset.id
                      ? "bg-stone-800 text-stone-200 border-stone-700"
                      : "bg-stone-100 text-stone-700 border-stone-200"
                  }`}>
                    {preset.groundTruth}%
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Input Question Area */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-stone-700 flex items-center justify-between">
            <span>Question or Feature / Pricing Pitch:</span>
            <button
              onClick={() => setShowAdvancedInputs(!showAdvancedInputs)}
              className="text-xs text-stone-600 hover:text-stone-900 font-medium flex items-center space-x-1"
            >
              <SlidersHorizontal className="w-3 h-3" />
              <span>{showAdvancedInputs ? "Hide Action A/B Framing" : "Customize Action A / Baseline B"}</span>
            </button>
          </label>
          <div className="relative">
            <textarea
              rows={3}
              value={customQuestion}
              onChange={(e) => {
                setCustomQuestion(e.target.value);
                setSelectedPresetId("");
              }}
              placeholder="e.g. Would you switch to an annual plan for a 20% discount or stay on monthly?"
              className="w-full bg-[#FAF9F5] border border-stone-300 rounded-lg p-3 text-xs text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-500 transition"
            />
          </div>
        </div>

        {/* Advanced Inputs: Discrete Choice Action Framing */}
        {showAdvancedInputs && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 p-3 bg-[#F7F6F2] rounded-lg border border-stone-200 text-xs">
            <div>
              <label className="font-semibold text-stone-900 block mb-1">
                Action A (The Behavior or Innovation Being Tested):
              </label>
              <input
                type="text"
                value={customActionA}
                onChange={(e) => setCustomActionA(e.target.value)}
                className="w-full bg-white border border-stone-200 rounded-md p-2 text-stone-900 text-xs focus:outline-none focus:border-stone-500"
              />
            </div>
            <div>
              <label className="font-semibold text-stone-700 block mb-1">
                Baseline B (Status Quo / Counterfactual Default):
              </label>
              <input
                type="text"
                value={customBaselineB}
                onChange={(e) => setCustomBaselineB(e.target.value)}
                className="w-full bg-white border border-stone-200 rounded-md p-2 text-stone-900 text-xs focus:outline-none focus:border-stone-500"
              />
            </div>
          </div>
        )}

        {/* Execute Simulation Button */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-1">
          <div className="text-xs text-stone-500 flex items-center space-x-2">
            <div className="flex -space-x-1.5 overflow-hidden">
              {activePersonas.map((p) => (
                <div
                  key={p.id}
                  className="inline-block h-6 w-6 rounded-full ring-2 ring-white text-[10px] font-bold text-white bg-stone-800 flex items-center justify-center"
                  title={`${p.name} (${p.demographics.occupation})`}
                >
                  {p.avatarInitial}
                </div>
              ))}
            </div>
            <span>Evaluating across 5 MECE personas</span>
          </div>

          <button
            onClick={handleExecuteSimulation}
            disabled={isSimulating || !customQuestion.trim()}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-stone-900 hover:bg-stone-800 disabled:opacity-50 text-white font-medium text-xs px-6 py-2.5 rounded-lg shadow-xs transition active:scale-95"
          >
            {isSimulating ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Simulating...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
                <span>Run Sandbox Simulation</span>
              </>
            )}
          </button>
        </div>

        {/* Animated Progress Indicator */}
        {isSimulating && (
          <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-300 text-xs text-stone-800 flex items-center space-x-2 animate-pulse">
            <Sparkles className="w-3.5 h-3.5 text-stone-600 shrink-0" />
            <span>{simulationStepText}</span>
          </div>
        )}
      </div>

      {/* Results View */}
      {lastResult && (
        <div className="space-y-6">
          {/* Macro Population Analytics */}
          <MacroMetricsView result={lastResult} onOpenZoom={() => onOpenZoom(lastResult)} />

          {/* Individual Persona Responses Grid */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-base font-bold text-stone-900">Individual Persona Responses (N=5 MECE)</h3>
                <p className="text-xs text-stone-500">
                  Each persona evaluates personal shift, switching friction, and utility without sycophancy.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {lastResult.personaResults.map((pResult) => {
                const profile = activePersonas.find((p) => p.id === pResult.personaId);
                return <PersonaCard key={pResult.personaId} result={pResult} personaProfile={profile} />;
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
