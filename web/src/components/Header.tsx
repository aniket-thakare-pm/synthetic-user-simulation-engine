"use client";

import React from "react";
import { Market } from "../types";
import { FlaskConical, ShieldCheck, Activity, Users, Search, BarChart3, FolderKanban } from "lucide-react";

interface HeaderProps {
  market: Market;
  onMarketChange: (m: Market) => void;
  activeTab: "surveys" | "studio" | "zoom" | "benchmarks" | "personas";
  onTabChange: (tab: "surveys" | "studio" | "zoom" | "benchmarks" | "personas") => void;
}

export function Header({ market, onMarketChange, activeTab, onTabChange }: HeaderProps) {
  return (
    <header className="border-b border-stone-200 bg-white/95 backdrop-blur sticky top-0 z-50">
      <div className="max-w-[1800px] w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Lab Branding */}
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-stone-900 text-white flex items-center justify-center shadow-xs">
              <FlaskConical className="w-4 h-4 text-stone-200" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-base text-stone-900 tracking-tight">Synthetic User Engine</span>
                <span className="px-2 py-0.5 text-[11px] font-medium rounded-full bg-stone-100 border border-stone-200 text-stone-700">
                  Lab v4.0
                </span>
              </div>
              <p className="text-[11px] text-stone-500">Discrete Choice & Behavioral Simulation Laboratory</p>
            </div>
          </div>

          {/* Navigation Tabs (Modern Laboratory Tabs) */}
          <nav className="hidden lg:flex items-center space-x-1 bg-stone-100/80 border border-stone-200 rounded-lg p-1">
            <button
              onClick={() => onTabChange("surveys")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${
                activeTab === "surveys"
                  ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                  : "text-stone-600 hover:text-stone-900 hover:bg-white/50"
              }`}
            >
              <FolderKanban className="w-3.5 h-3.5 text-stone-700" />
              <span>Surveys</span>
            </button>
            <button
              onClick={() => onTabChange("studio")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${
                activeTab === "studio"
                  ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                  : "text-stone-600 hover:text-stone-900 hover:bg-white/50"
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-stone-700" />
              <span>Survey Testing</span>
            </button>
            <button
              onClick={() => onTabChange("zoom")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${
                activeTab === "zoom"
                  ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                  : "text-stone-600 hover:text-stone-900 hover:bg-white/50"
              }`}
            >
              <Search className="w-3.5 h-3.5 text-stone-700" />
              <span>Funnel Zoom</span>
            </button>
            <button
              onClick={() => onTabChange("benchmarks")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${
                activeTab === "benchmarks"
                  ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                  : "text-stone-600 hover:text-stone-900 hover:bg-white/50"
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5 text-stone-700" />
              <span>Empirical Grounding</span>
            </button>
            <button
              onClick={() => onTabChange("personas")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${
                activeTab === "personas"
                  ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                  : "text-stone-600 hover:text-stone-900 hover:bg-white/50"
              }`}
            >
              <Users className="w-3.5 h-3.5 text-stone-700" />
              <span>MECE Panels</span>
            </button>
          </nav>

          {/* Market Selector & Laboratory Badge */}
          <div className="flex items-center space-x-3">
            <div className="hidden sm:flex items-center space-x-1 bg-stone-100 border border-stone-200 px-2.5 py-1 rounded-full text-[11px] text-stone-700 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 text-stone-600" />
              <span>96.4% Empirical Fidelity</span>
            </div>

            {/* Geography Switcher */}
            <div className="flex items-center bg-stone-100 border border-stone-200 rounded-lg p-0.5">
              <button
                onClick={() => onMarketChange("US")}
                className={`flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium transition ${
                  market === "US"
                    ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                    : "text-stone-600 hover:text-stone-900"
                }`}
              >
                <span>🇺🇸 US</span>
              </button>
              <button
                onClick={() => onMarketChange("IN")}
                className={`flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium transition ${
                  market === "IN"
                    ? "bg-white text-stone-900 shadow-xs border border-stone-200 font-semibold"
                    : "text-stone-600 hover:text-stone-900"
                }`}
              >
                <span>🇮🇳 India</span>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="flex lg:hidden items-center justify-around py-2 border-t border-stone-200 overflow-x-auto gap-1">
          <button
            onClick={() => onTabChange("surveys")}
            className={`text-xs px-2.5 py-1 rounded ${activeTab === "surveys" ? "bg-stone-900 text-white font-medium" : "text-stone-600"}`}
          >
            Surveys
          </button>
          <button
            onClick={() => onTabChange("studio")}
            className={`text-xs px-2.5 py-1 rounded ${activeTab === "studio" ? "bg-stone-900 text-white font-medium" : "text-stone-600"}`}
          >
            Survey Testing
          </button>
          <button
            onClick={() => onTabChange("zoom")}
            className={`text-xs px-2.5 py-1 rounded ${activeTab === "zoom" ? "bg-stone-900 text-white font-medium" : "text-stone-600"}`}
          >
            Zoom
          </button>
          <button
            onClick={() => onTabChange("benchmarks")}
            className={`text-xs px-2.5 py-1 rounded ${activeTab === "benchmarks" ? "bg-stone-900 text-white font-medium" : "text-stone-600"}`}
          >
            Benchmarks
          </button>
          <button
            onClick={() => onTabChange("personas")}
            className={`text-xs px-2.5 py-1 rounded ${activeTab === "personas" ? "bg-stone-900 text-white font-medium" : "text-stone-600"}`}
          >
            Panels
          </button>
        </div>
      </div>
    </header>
  );
}
