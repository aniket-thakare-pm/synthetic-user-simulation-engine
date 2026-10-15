"use client";

import React from "react";
import { SimulationResult } from "../types";
import { ShieldCheck, TrendingUp, AlertTriangle, Scale, Target, ArrowRight } from "lucide-react";

interface MacroMetricsViewProps {
  result: SimulationResult;
  onOpenZoom: () => void;
}

export function MacroMetricsView({ result, onOpenZoom }: MacroMetricsViewProps) {
  const hasGroundTruth = typeof result.groundTruth === "number";
  const errorDelta = hasGroundTruth ? Math.abs(result.weightedScore - (result.groundTruth || 0)) : null;

  return (
    <div className="bg-white border border-stone-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-5">
      {/* Top Header / Meta */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-stone-200 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-md">
              {result.category}
            </span>
            <span className="text-xs text-stone-500">
              Region: <strong className="text-stone-800">{result.market === "IN" ? "India (NPCI/PwC)" : "US (Census/Pew)"}</strong>
            </span>
            <span className="text-xs text-stone-400">• {result.timestamp}</span>
          </div>
          <h2 className="text-base sm:text-lg font-bold text-stone-900 mt-1.5 leading-snug">
            &ldquo;{result.question}&rdquo;
          </h2>
        </div>

        {/* Action Button: Trigger Funnel Zoom */}
        <button
          onClick={onOpenZoom}
          className="shrink-0 flex items-center justify-center space-x-2 bg-stone-900 hover:bg-stone-800 text-white font-medium text-xs sm:text-sm px-4 py-2.5 rounded-lg shadow-xs transition active:scale-95"
        >
          <span>Funnel Zoom into Segment</span>
          <ArrowRight className="w-4 h-4 text-stone-300" />
        </button>
      </div>

      {/* Discrete Choice Formulation (Action A vs Baseline B) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
        <div className="flex items-start space-x-2">
          <div className="w-5 h-5 rounded-md bg-emerald-100 text-emerald-800 border border-emerald-200 flex items-center justify-center font-bold shrink-0 mt-0.5">
            A
          </div>
          <div>
            <span className="font-semibold text-stone-900">Action A (Target Innovation):</span>
            <p className="text-stone-600 mt-0.5">{result.actionA}</p>
          </div>
        </div>
        <div className="flex items-start space-x-2">
          <div className="w-5 h-5 rounded-md bg-stone-100 text-stone-600 border border-stone-200 flex items-center justify-center font-bold shrink-0 mt-0.5">
            B
          </div>
          <div>
            <span className="font-semibold text-stone-700">Baseline B (Status Quo Counterfactual):</span>
            <p className="text-stone-500 mt-0.5">{result.baselineB}</p>
          </div>
        </div>
      </div>

      {/* Core Quantitative Scorecards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        {/* Card 1: Post-Stratified Weighted Score */}
        <div className="bg-[#FAF9F5] border border-stone-300 rounded-lg p-3.5 shadow-xs">
          <div className="flex items-center justify-between text-stone-500 text-xs">
            <span>Post-Stratified Score (W<sub>i</sub>)</span>
            <Scale className="w-4 h-4 text-stone-600" />
          </div>
          <div className="mt-1.5 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-stone-900">{result.weightedScore}%</span>
            <span className="text-[11px] font-semibold text-emerald-700">Calibrated</span>
          </div>
          <p className="text-[10px] text-stone-500 mt-0.5">
            Weighted across population shares (sum W<sub>i</sub> = {result.totalWeight * 100}%).
          </p>
        </div>

        {/* Card 2: Unweighted Naive LLM Comparison */}
        <div className="bg-white border border-stone-200 rounded-lg p-3.5">
          <div className="flex items-center justify-between text-stone-500 text-xs">
            <span>Naive Unweighted Average</span>
            <TrendingUp className="w-4 h-4 text-stone-400" />
          </div>
          <div className="mt-1.5 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-stone-700">{result.unweightedScore}%</span>
            <span className="text-[11px] text-stone-400">
              Δ {(result.unweightedScore - result.weightedScore).toFixed(1)}%
            </span>
          </div>
          <p className="text-[10px] text-stone-400 mt-0.5">
            Raw average before post-stratification.
          </p>
        </div>

        {/* Card 3: Empirical Prior Base Rate (V0) */}
        <div className="bg-white border border-stone-200 rounded-lg p-3.5">
          <div className="flex items-center justify-between text-stone-500 text-xs">
            <span>Literature Prior (P<sub>ref</sub>)</span>
            <Target className="w-4 h-4 text-stone-400" />
          </div>
          <div className="mt-1.5 flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-stone-800">{result.empiricalBaseRate}%</span>
            <span className="text-[11px] text-stone-500">Benchmark</span>
          </div>
          <p className="text-[10px] text-stone-400 mt-0.5 truncate" title={result.empiricalArchetype}>
            {result.empiricalArchetype}
          </p>
        </div>

        {/* Card 4: Ground Truth Empirical Comparison (if preset) */}
        {hasGroundTruth ? (
          <div className="bg-emerald-50/60 border border-emerald-200 rounded-lg p-3.5">
            <div className="flex items-center justify-between text-emerald-900 text-xs">
              <span>Real Human Benchmark</span>
              <ShieldCheck className="w-4 h-4 text-emerald-700" />
            </div>
            <div className="mt-1.5 flex items-baseline space-x-2">
              <span className="text-3xl font-extrabold text-stone-900">{result.groundTruth}%</span>
              <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300">
                Δ {errorDelta?.toFixed(1)}% Error
              </span>
            </div>
            <p className="text-[10px] text-emerald-800/80 mt-0.5 truncate" title={result.studyCitation}>
              {result.studyCitation}
            </p>
          </div>
        ) : (
          <div className="bg-white border border-stone-200 rounded-lg p-3.5">
            <div className="flex items-center justify-between text-stone-500 text-xs">
              <span>Adoption Distribution</span>
              <Scale className="w-4 h-4 text-stone-400" />
            </div>
            <div className="mt-3">
              <div className="w-full bg-stone-100 h-2.5 rounded-full overflow-hidden flex border border-stone-200">
                <div
                  className="bg-emerald-600 h-full transition-all duration-300"
                  style={{ width: `${result.weightedScore}%` }}
                />
              </div>
              <div className="flex justify-between text-[10px] mt-1 text-stone-500">
                <span className="text-emerald-700 font-semibold">{result.weightedScore}% Adopt</span>
                <span className="text-stone-600 font-semibold">{(100 - result.weightedScore).toFixed(1)}% Reject</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Clustered Objections & Friction Themes */}
      {result.keyThemes.length > 0 && (
        <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
          <div className="text-xs font-semibold text-stone-700 flex items-center space-x-1.5 mb-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            <span>Dominant Bottlenecks Clustered by Mental Accounting:</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {result.keyThemes.map((theme, idx) => (
              <span
                key={idx}
                className="text-[11px] bg-white text-stone-700 border border-stone-200 px-2.5 py-0.5 rounded-md font-medium"
              >
                {theme}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
