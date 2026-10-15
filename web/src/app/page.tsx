"use client";

import React, { useState } from "react";
import { Market, SimulationResult } from "../types";
import { Header } from "../components/Header";
import { SurveyWorkspace } from "../components/SurveyWorkspace";
import { SimulationStudio } from "../components/SimulationStudio";
import { FunnelZoomView } from "../components/FunnelZoomView";
import { BenchmarkShowcase } from "../components/BenchmarkShowcase";
import { PersonaLibraryView } from "../components/PersonaLibraryView";

export default function Home() {
  const [market, setMarket] = useState<Market>("US");
  const [activeTab, setActiveTab] = useState<"surveys" | "studio" | "zoom" | "benchmarks" | "personas">("surveys");
  const [lastResult, setLastResult] = useState<SimulationResult | undefined>(undefined);

  const handleOpenZoom = (result: SimulationResult) => {
    setLastResult(result);
    setActiveTab("zoom");
  };

  return (
    <div className="min-h-screen bg-[#FBFBFA] text-stone-900 flex flex-col selection:bg-stone-200 selection:text-stone-900">
      {/* Top Navigation */}
      <Header
        market={market}
        onMarketChange={(m) => setMarket(m)}
        activeTab={activeTab}
        onTabChange={(tab) => setActiveTab(tab)}
      />

      {/* Main Content Area: Widescreen 16:9 dynamic layout container */}
      <main className="flex-1 max-w-[1800px] w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 py-6 sm:py-8">
        {activeTab === "surveys" && (
          <SurveyWorkspace currentMarket={market} />
        )}

        {activeTab === "studio" && (
          <SimulationStudio
            market={market}
            onOpenZoom={handleOpenZoom}
            lastResult={lastResult}
            setLastResult={setLastResult}
          />
        )}

        {activeTab === "zoom" && (
          <FunnelZoomView
            lastResult={lastResult}
            onBackToStudio={() => setActiveTab("surveys")}
          />
        )}

        {activeTab === "benchmarks" && (
          <BenchmarkShowcase
            onLoadScenario={(id) => {
              setActiveTab("studio");
            }}
          />
        )}

        {activeTab === "personas" && (
          <PersonaLibraryView currentMarket={market} />
        )}
      </main>

      {/* Modern Laboratory Paper Footer */}
      <footer className="border-t border-stone-200 bg-white py-8 text-xs text-stone-500 mt-12">
        <div className="max-w-[1800px] w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <span className="font-semibold text-stone-800">Synthetic User Engine</span>
            <span className="mx-2">•</span>
            <span>Empirical-Bayesian Discrete Choice Architecture (EB-DCA v4.0)</span>
          </div>
          <div className="flex flex-wrap items-center gap-4 text-stone-500">
            <span>McFadden Random Utility (1974)</span>
            <span>•</span>
            <span>Kahneman-Tversky Prospect Theory (1979)</span>
            <span>•</span>
            <span>Thaler Mental Accounting (1985)</span>
            <span>•</span>
            <span>Deloitte N=2,005 / Baymard N=4,384</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
