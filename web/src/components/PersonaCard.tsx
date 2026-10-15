"use client";

import React, { useState } from "react";
import { PersonaSimulationResult, Persona } from "../types";
import { ChevronDown, ChevronUp, ShieldAlert } from "lucide-react";

interface PersonaCardProps {
  result: PersonaSimulationResult;
  personaProfile?: Persona;
}

export function PersonaCard({ result, personaProfile }: PersonaCardProps) {
  const [expanded, setExpanded] = useState(false);
  const isYes = result.decisionStance === "YES";
  const score = result.targetMetricScore;

  return (
    <article className="rounded-2xl border border-stone-200/90 transition shadow-2xs bg-white p-5 space-y-3.5 hover:border-stone-300">
      {/* Top Banner / Header */}
      <div className="flex items-start justify-between gap-3 pb-2.5 border-b border-stone-100">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 rounded-lg bg-stone-900 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs mt-0.5">
            {personaProfile?.avatarInitial || result.personaName.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <div className="flex items-baseline space-x-2">
              <h4 className="font-serif font-bold text-stone-900 text-sm leading-snug">{result.personaName}</h4>
              <span className="text-xs text-stone-400 font-sans">· {result.personaRole}</span>
            </div>
            {personaProfile && (
              <p className="text-[11px] text-stone-400 font-sans mt-0.5">
                {personaProfile.demographics.geography} · Budget: {personaProfile.market === "IN" ? `₹${personaProfile.psychographics.priceCeilingMonthly}` : `$${personaProfile.psychographics.priceCeilingMonthly}`}/mo · {Math.round(result.weight * 100)}% Weight
              </p>
            )}
          </div>
        </div>

        {/* Monospace Stance Pill & Choice Score */}
        <div className="text-right shrink-0">
          <span
            className={`font-mono text-xs font-bold px-2.5 py-1 rounded-md border inline-block ${
              isYes
                ? "bg-emerald-50 text-emerald-800 border-emerald-200/70"
                : "bg-amber-50 text-amber-900 border-amber-200/70"
            }`}
          >
            P(Adopt) = {(score / 100).toFixed(2)}
          </span>
          <div className="text-[10px] uppercase font-bold text-stone-400 mt-1">
            {isYes ? "Adopts (YES)" : "Rejects (NO)"}
          </div>
        </div>
      </div>

      {/* Verbatim Voice Pull-Quote in Editorial Serif */}
      <div className="py-1">
        <blockquote className="font-serif text-stone-800 text-[13.5px] sm:text-sm leading-relaxed pl-3.5 border-l-2 border-stone-300 italic py-0.5">
          “{result.responseText}”
        </blockquote>
      </div>

      {/* Primary Driver / Friction Summary & Drawer Trigger */}
      <div className="pt-2 border-t border-stone-100 flex items-center justify-between text-xs text-stone-600 gap-2">
        <div className="text-[11.5px] truncate">
          {isYes ? (
            <span>
              <strong className="font-semibold text-stone-900 font-sans">Primary Driver: </strong>
              <span className="text-stone-700">Perceived utility exceeds friction threshold</span>
            </span>
          ) : (
            <span>
              <strong className="font-semibold text-amber-950 font-sans">Primary Friction: </strong>
              <span className="text-stone-700">{result.primaryObjection || "Switching inertia exceeds utility gain"}</span>
            </span>
          )}
        </div>

        {personaProfile && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-[11px] font-sans font-semibold text-stone-600 hover:text-stone-900 shrink-0 flex items-center space-x-1 transition"
          >
            <span>{expanded ? "Hide Telemetry" : "Show Telemetry"}</span>
            {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>
        )}
      </div>

      {/* Expanded Psychometric Telemetry & Decision Footnote */}
      {expanded && personaProfile && (
        <div className="mt-2.5 p-3.5 bg-[#FAF9F5] border border-stone-200/80 rounded-xl space-y-3 text-xs text-stone-700 animate-fadeIn">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-[11px] font-mono">
            <div className="bg-white p-2 rounded-lg border border-stone-200/80">
              <div className="text-stone-400 text-[10px] font-sans">Net Utility (ΔV)</div>
              <div className="font-bold text-stone-900 mt-0.5">{result.deltaV >= 0 ? `+${result.deltaV}` : result.deltaV}</div>
            </div>
            <div className="bg-white p-2 rounded-lg border border-stone-200/80">
              <div className="text-stone-400 text-[10px] font-sans">Loss Aversion (λ)</div>
              <div className="font-bold text-stone-900 mt-0.5">{personaProfile.psychographics.lossAversionBias}</div>
            </div>
            <div className="bg-white p-2 rounded-lg border border-stone-200/80">
              <div className="text-stone-400 text-[10px] font-sans">Status Quo Inertia</div>
              <div className="font-bold text-stone-900 mt-0.5">{personaProfile.psychographics.statusQuoInertia} / 10</div>
            </div>
            <div className="bg-white p-2 rounded-lg border border-stone-200/80">
              <div className="text-stone-400 text-[10px] font-sans">Tech Literacy</div>
              <div className="font-bold text-stone-900 mt-0.5">{personaProfile.demographics.techLiteracy} / 10</div>
            </div>
          </div>

          {/* Guardrail Rules */}
          <div className="pt-2 border-t border-stone-200/60 text-[11px] font-sans">
            <span className="font-semibold text-stone-900 block mb-1">
              Anti-Sycophancy Negative Directives:
            </span>
            <ul className="list-disc list-inside space-y-0.5 text-stone-600">
              {personaProfile.guardrailRules.map((rule, idx) => (
                <li key={idx} className="leading-snug">
                  {rule}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </article>
  );
}
