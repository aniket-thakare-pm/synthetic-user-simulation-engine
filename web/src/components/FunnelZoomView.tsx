"use client";

import React from "react";
import { ZoomedSubPersona, SimulationResult } from "../types";
import { generateZoomPanel } from "../services/simulationEngine";
import { Search, ArrowLeft, ShieldAlert } from "lucide-react";

interface FunnelZoomViewProps {
  lastResult?: SimulationResult;
  onBackToStudio: () => void;
}

export function FunnelZoomView({ lastResult, onBackToStudio }: FunnelZoomViewProps) {
  const dummyResult: SimulationResult = lastResult || {
    question: "Would you pay a $5 monthly price hike or cancel your streaming subscription?",
    market: "US",
    category: "Digital Subscriptions",
    actionA: "Cancel immediately",
    baselineB: "Keep service",
    empiricalBaseRate: 61.0,
    empiricalArchetype: "Subscription Price Hike Churn",
    weightedScore: 61.3,
    unweightedScore: 62.0,
    totalWeight: 1.0,
    personaResults: [],
    keyThemes: ["Budget Inflation", "Habit Inertia"],
    timestamp: "Just now",
  };

  const subPersonas: ZoomedSubPersona[] = generateZoomPanel(dummyResult);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white border border-stone-200 rounded-xl p-5 sm:p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-md">
                Phase 2 Research
              </span>
              <span className="text-xs text-stone-500">Transcript-Aware Sub-Audience Expansion</span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-stone-900 mt-1.5 flex items-center space-x-2">
              <Search className="w-5 h-5 text-stone-700" />
              <span>Funnel Zoom: 5 Micro-MECE Sub-Personas</span>
            </h2>
            <p className="text-xs sm:text-sm text-stone-600 mt-1 max-w-3xl leading-relaxed">
              Instead of re-surveying uninterested dropouts, the engine zooms exclusively into your qualified target segment. 
              By parsing session transcript objections, it expands them into 5 distinct edge-case archetypes to test feature packaging, billing boundaries, and churn triggers.
            </p>
          </div>

          <button
            onClick={onBackToStudio}
            className="flex items-center space-x-2 bg-stone-900 hover:bg-stone-800 text-white text-xs font-medium px-4 py-2 rounded-lg transition shrink-0 shadow-xs"
          >
            <ArrowLeft className="w-4 h-4 text-stone-300" />
            <span>Return to Workspace</span>
          </button>
        </div>

        {/* Source Context Bar */}
        <div className="mt-4 pt-3 border-t border-stone-200 flex flex-wrap items-center justify-between text-xs text-stone-500 gap-2">
          <div>
            Targeted Audience from: <strong className="text-stone-800">&ldquo;{dummyResult.question.slice(0, 70)}...&rdquo;</strong>
          </div>
          <div>
            Market Segment: <strong className="text-stone-800">{dummyResult.market === "IN" ? "India Tier 1/2" : "US National"}</strong>
          </div>
        </div>
      </div>

      {/* Grid of 5 Micro-MECE Sub-Personas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3.5">
        {subPersonas.map((sp, idx) => (
          <div
            key={sp.id}
            className="bg-white border border-stone-200 hover:border-stone-300 rounded-xl p-4 shadow-xs transition flex flex-col justify-between"
          >
            <div>
              {/* Header */}
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-1.5">
                    <span className="w-5 h-5 rounded bg-stone-100 text-stone-700 border border-stone-200 flex items-center justify-center font-bold text-[10px]">
                      #{idx + 1}
                    </span>
                    <h3 className="font-bold text-stone-900 text-xs sm:text-sm">{sp.name}</h3>
                  </div>
                  <div className="text-[11px] text-stone-500 font-medium mt-0.5">{sp.role}</div>
                </div>
                <span className="text-[10px] font-semibold bg-stone-100 text-stone-600 px-2 py-0.5 rounded border border-stone-200">
                  {Math.round(sp.populationWeight * 100)}%
                </span>
              </div>

              {/* Behavioral Archetype Badge */}
              <div className="mt-2.5 inline-block text-[10px] font-medium bg-[#FAF9F5] text-stone-700 border border-stone-200 px-2 py-0.5 rounded">
                {sp.archetype}
              </div>

              {/* Expressed Pain Point */}
              <div className="mt-3 bg-[#FAF9F5] p-2.5 rounded-lg border border-stone-200 text-xs">
                <span className="text-stone-400 font-medium block text-[10px] uppercase">
                  Transcript Pain Point:
                </span>
                <p className="text-stone-800 italic mt-0.5 text-[11px] leading-snug">&ldquo;{sp.expressedPainPoint}&rdquo;</p>
              </div>

              {/* Edge Case Dealbreaker */}
              <div className="mt-2.5 flex items-start space-x-1.5 text-[11px] bg-rose-50 border border-rose-200 p-2 rounded-lg text-rose-800">
                <ShieldAlert className="w-3.5 h-3.5 text-rose-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-rose-900">Dealbreaker: </span>
                  {sp.edgeCaseDealbreaker}
                </div>
              </div>
            </div>

            {/* Bottom Metrics Footer */}
            <div className="mt-3 pt-2.5 border-t border-stone-100 flex items-center justify-between text-xs">
              <span className="text-[11px] text-stone-500">
                Cap:{" "}
                <strong className="text-stone-800">
                  {dummyResult.market === "IN" ? `₹${sp.priceCeiling}` : `$${sp.priceCeiling}`}
                </strong>
              </span>
              <div className="flex items-center space-x-1">
                <span className="text-[10px] text-stone-500">Accept:</span>
                <span className="font-bold text-emerald-800 text-xs bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                  {sp.predictedAcceptance}%
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
