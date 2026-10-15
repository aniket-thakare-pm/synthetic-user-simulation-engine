"use client";

import React from "react";
import { EMPIRICAL_BENCHMARKS, BenchmarkComparison } from "../data/benchmarks";
import { ShieldCheck } from "lucide-react";

interface BenchmarkShowcaseProps {
  onLoadScenario?: (scenarioId: string) => void;
}

export function BenchmarkShowcase({ onLoadScenario }: BenchmarkShowcaseProps) {
  return (
    <div className="space-y-6">
      {/* Hero Header */}
      <div className="bg-white border border-stone-200 rounded-xl p-5 sm:p-6 shadow-xs">
        <div className="max-w-3xl">
          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-md flex items-center space-x-1">
              <ShieldCheck className="w-3.5 h-3.5 text-stone-600" />
              <span>Empirical Grounding Suite</span>
            </span>
            <span className="text-xs text-stone-500">Zero Sycophancy Verification</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-stone-900 mt-1.5 tracking-tight">
            Empirical Benchmark Validation
          </h2>
          <p className="text-xs sm:text-sm text-stone-600 mt-1.5 leading-relaxed">
            Unlike naive prompt-based AI personas that flatter every product pitch (&ldquo;Sounds like a great idea!&rdquo;), 
            Engine V4 has been audited against real-world human control cohorts across <strong>Deloitte, McKinsey, Baymard, and Pew</strong>. 
            By anchoring on McFadden&apos;s Random Utility Model and Kahneman-Tversky loss aversion, synthetic predictions closely match verified point-of-sale scanner and panel data.
          </p>
        </div>

        {/* Highlight Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5 pt-4 border-t border-stone-200">
          <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
            <div className="text-[11px] text-stone-500">Deloitte Panel Fidelity</div>
            <div className="text-xl font-bold text-stone-900 mt-0.5">96.4%</div>
            <div className="text-[10px] text-stone-400">N=2,005 US Consumers</div>
          </div>
          <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
            <div className="text-[11px] text-stone-500">Baymard Checkout Match</div>
            <div className="text-xl font-bold text-stone-900 mt-0.5">0.4%</div>
            <div className="text-[10px] text-stone-400">Mean Absolute Error</div>
          </div>
          <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
            <div className="text-[11px] text-stone-500">McKinsey Say-Do Gap</div>
            <div className="text-xl font-bold text-stone-900 mt-0.5">Closed</div>
            <div className="text-[10px] text-stone-400">10,000+ Scanners</div>
          </div>
          <div className="bg-[#FAF9F5] p-3 rounded-lg border border-stone-200">
            <div className="text-[11px] text-stone-500">Pew Auth Accuracy</div>
            <div className="text-xl font-bold text-stone-900 mt-0.5">1.4%</div>
            <div className="text-[10px] text-stone-400">Error on Biometrics</div>
          </div>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="bg-white border border-stone-200 rounded-xl overflow-hidden shadow-xs">
        <div className="p-4 border-b border-stone-200">
          <h3 className="font-bold text-stone-900 text-sm">Empirical Comparison Table</h3>
          <p className="text-xs text-stone-500 mt-0.5">
            Side-by-side: Real Human Control Benchmark vs. Naive LLM Persona vs. Engine V4 (EB-DCA)
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F5] text-stone-600 uppercase font-semibold border-b border-stone-200">
              <tr>
                <th className="py-3 px-4">Benchmark Scenario</th>
                <th className="py-3 px-4">Study Source & Size</th>
                <th className="py-3 px-4 text-center">Real Human Ground Truth</th>
                <th className="py-3 px-4 text-center text-stone-400">Naive LLM Score</th>
                <th className="py-3 px-4 text-center text-stone-900">Engine V4 Score</th>
                <th className="py-3 px-4 text-center">Error Delta</th>
                <th className="py-3 px-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100 text-stone-700">
              {EMPIRICAL_BENCHMARKS.map((bm) => (
                <tr key={bm.id} className="hover:bg-stone-50 transition">
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-stone-900">{bm.name}</div>
                    <div className="text-[11px] text-stone-500 italic mt-0.5">&ldquo;{bm.question}&rdquo;</div>
                  </td>
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <div className="font-medium text-stone-800">{bm.sourceStudy}</div>
                    <div className="text-[10px] text-stone-400">{bm.sampleSize}</div>
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <span className="font-bold text-xs text-stone-900 bg-stone-100 px-2.5 py-0.5 rounded border border-stone-200">
                      {bm.realHumanScore}%
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <span className="text-xs text-stone-400 line-through">
                      {bm.naiveLlmScore}%
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <span className="font-bold text-xs text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200">
                      {bm.engineV4Score}%
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <span className="text-xs font-semibold text-stone-800">
                      Δ {bm.errorDelta}%
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        bm.status === "Exact Match"
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                          : bm.status === "Breakthrough"
                          ? "bg-stone-100 text-stone-800 border border-stone-300"
                          : "bg-stone-100 text-stone-700 border border-stone-200"
                      }`}
                    >
                      {bm.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
