"use client";

import React, { useState } from "react";
import { US_PERSONAS, IN_PERSONAS } from "../data/personas";
import { Market, Persona } from "../types";
import { Users, ShieldAlert } from "lucide-react";

interface PersonaLibraryViewProps {
  currentMarket: Market;
}

export function PersonaLibraryView({ currentMarket }: PersonaLibraryViewProps) {
  const [selectedMarket, setSelectedMarket] = useState<Market>(currentMarket);
  const personas = selectedMarket === "IN" ? IN_PERSONAS : US_PERSONAS;

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="bg-white border border-stone-200 rounded-xl p-5 sm:p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-md flex items-center space-x-1">
              <Users className="w-3.5 h-3.5 text-stone-600" />
              <span>MECE Regional Panels</span>
            </span>
            <span className="text-xs text-stone-500">Grounded in Census & Consumer Behavioral Studies</span>
          </div>
          <h2 className="text-lg sm:text-xl font-bold text-stone-900 mt-1.5">
            Calibrated Persona Library (N=10)
          </h2>
          <p className="text-xs sm:text-sm text-stone-600 mt-1 max-w-2xl">
            Each persona is mathematically configured with Kahneman-Tversky loss aversion ($\lambda$), 
            Thaler mental accounting parameters, and strict negative guardrails to prevent sycophancy.
          </p>
        </div>

        {/* Market Toggle Button */}
        <div className="flex items-center bg-stone-100 p-1 rounded-lg border border-stone-200 shrink-0">
          <button
            onClick={() => setSelectedMarket("US")}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              selectedMarket === "US"
                ? "bg-white text-stone-900 shadow-xs border border-stone-200"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            🇺🇸 US Panel (5 MECE)
          </button>
          <button
            onClick={() => setSelectedMarket("IN")}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              selectedMarket === "IN"
                ? "bg-white text-stone-900 shadow-xs border border-stone-200"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            🇮🇳 India Panel (5 MECE)
          </button>
        </div>
      </div>

      {/* Personas Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {personas.map((p) => (
          <div
            key={p.id}
            className="bg-white border border-stone-200 rounded-xl p-5 shadow-xs hover:border-stone-300 transition flex flex-col justify-between"
          >
            <div>
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <div className="w-10 h-10 rounded-lg bg-stone-800 text-white flex items-center justify-center font-bold text-sm shadow-xs">
                    {p.avatarInitial}
                  </div>
                  <div>
                    <h3 className="font-bold text-stone-900 text-base">{p.name}</h3>
                    <p className="text-xs text-stone-600 font-medium">{p.demographics.occupation}</p>
                    <div className="flex items-center space-x-2 text-[11px] text-stone-400 mt-0.5">
                      <span>Age: {p.demographics.age}</span>
                      <span>•</span>
                      <span>Income: {p.demographics.incomeBracket}</span>
                      {p.demographics.cityTier && (
                        <>
                          <span>•</span>
                          <span>{p.demographics.cityTier}</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-[11px] font-semibold bg-stone-100 text-stone-700 border border-stone-200 px-2 py-0.5 rounded">
                    Weight: {Math.round(p.populationWeight * 100)}% (W<sub>i</sub>)
                  </span>
                  <div className="text-[11px] text-stone-500 mt-1">
                    Cap: {selectedMarket === "IN" ? `₹${p.psychographics.priceCeilingMonthly}` : `$${p.psychographics.priceCeilingMonthly}`}/mo
                  </div>
                </div>
              </div>

              {/* Core Pain Point */}
              <div className="mt-3.5 bg-[#FAF9F5] p-3 rounded-lg border border-stone-200 text-xs">
                <span className="text-[10px] uppercase font-semibold text-stone-500 block">
                  Primary Consumer Frustration:
                </span>
                <p className="text-stone-800 italic mt-0.5">&ldquo;{p.psychographics.primaryPainPoint}&rdquo;</p>
              </div>

              {/* Behavioral Economics Parameters Grid */}
              <div className="grid grid-cols-4 gap-2 mt-3 text-center">
                <div className="bg-[#FAF9F5] p-2 rounded border border-stone-200">
                  <div className="text-[10px] text-stone-500">Loss Aversion</div>
                  <div className="font-bold text-xs text-stone-900 mt-0.5">λ = {p.psychographics.lossAversionBias}</div>
                </div>
                <div className="bg-[#FAF9F5] p-2 rounded border border-stone-200">
                  <div className="text-[10px] text-stone-500">Inertia</div>
                  <div className="font-bold text-xs text-stone-900 mt-0.5">{p.psychographics.statusQuoInertia} / 10</div>
                </div>
                <div className="bg-[#FAF9F5] p-2 rounded border border-stone-200">
                  <div className="text-[10px] text-stone-500">Tech Lit.</div>
                  <div className="font-bold text-xs text-stone-900 mt-0.5">{p.demographics.techLiteracy} / 10</div>
                </div>
                <div className="bg-[#FAF9F5] p-2 rounded border border-stone-200">
                  <div className="text-[10px] text-stone-500">Fin. Lit.</div>
                  <div className="font-bold text-xs text-stone-900 mt-0.5">{p.psychographics.financialLiteracy} / 10</div>
                </div>
              </div>

              {/* Capabilities & Auth */}
              <div className="mt-3 flex flex-wrap gap-1.5 text-[11px] text-stone-500">
                <span className="bg-stone-100 px-2 py-0.5 rounded text-stone-700">
                  💳 {p.capabilities.primaryPayment}
                </span>
                <span className="bg-stone-100 px-2 py-0.5 rounded text-stone-700">
                  🔐 {p.capabilities.digitalAuth}
                </span>
                <span className="bg-stone-100 px-2 py-0.5 rounded text-stone-700">
                  📱 {p.capabilities.deviceTier}
                </span>
              </div>
            </div>

            {/* Anti-Sycophancy Guardrails */}
            <div className="mt-4 pt-3 border-t border-stone-100">
              <div className="text-[11px] font-semibold text-stone-800 flex items-center space-x-1 mb-1">
                <ShieldAlert className="w-3.5 h-3.5 text-stone-600" />
                <span>Deterministic Anti-Sycophancy Guardrails:</span>
              </div>
              <ul className="space-y-1">
                {p.guardrailRules.map((rule, idx) => (
                  <li key={idx} className="text-[11px] text-stone-600 flex items-start space-x-1.5">
                    <span className="text-stone-400 font-bold">•</span>
                    <span className="leading-tight">{rule}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
