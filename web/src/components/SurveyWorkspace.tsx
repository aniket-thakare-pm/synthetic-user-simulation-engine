"use client";

import React, { useState, useEffect } from "react";
import { SurveyStudy, SurveyQuestion, Market, Persona, SimulationResult, PersonaSimulationResult } from "../types";
import { INITIAL_STUDIES } from "../data/sampleSurveys";
import { US_PERSONAS, IN_PERSONAS } from "../data/personas";
import { runSimulation } from "../services/simulationEngine";
import { generateMarkdownReport, generateCsvReport, downloadFile } from "../utils/exportReport";
import {
  FolderPlus,
  Folder,
  Plus,
  Play,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  Download,
  Copy,
  Trash2,
  Edit2,
  CopyPlus,
  Check,
  CheckCircle2,
  Sparkles,
  FileText,
  RotateCcw,
  BookOpen,
} from "lucide-react";

const STORAGE_KEY = "synthetic_user_studies_v2";

interface SurveyWorkspaceProps {
  currentMarket: Market;
}

export function SurveyWorkspace({ currentMarket }: SurveyWorkspaceProps) {
  const [studies, setStudies] = useState<SurveyStudy[]>(INITIAL_STUDIES);
  const [activeStudyId, setActiveStudyId] = useState<string>("study_01_pricing");
  const [activeQuestionId, setActiveQuestionId] = useState<string>("q_01_annual");
  const [isLoaded, setIsLoaded] = useState<boolean>(false);

  // New Question Form state
  const [newQuestionText, setNewQuestionText] = useState<string>("");
  const [newActionA, setNewActionA] = useState<string>("");
  const [newBaselineB, setNewBaselineB] = useState<string>("");
  const [isAddingQuestion, setIsAddingQuestion] = useState<boolean>(false);

  // Editing Question state
  const [editingQuestionId, setEditingQuestionId] = useState<string | null>(null);
  const [editText, setEditText] = useState<string>("");
  const [editActionA, setEditActionA] = useState<string>("");
  const [editBaselineB, setEditBaselineB] = useState<string>("");

  // New Study Modal state
  const [showNewStudyModal, setShowNewStudyModal] = useState<boolean>(false);
  const [newStudyTitle, setNewStudyTitle] = useState<string>("");
  const [newStudyDesc, setNewStudyDesc] = useState<string>("");
  const [newStudyMarket, setNewStudyMarket] = useState<Market>(currentMarket);

  // Export Modal state
  const [showExportModal, setShowExportModal] = useState<boolean>(false);
  const [copiedStatus, setCopiedStatus] = useState<boolean>(false);

  // Simulation state
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [simulationLogText, setSimulationLogText] = useState<string>("");

  // Which persona cards have their math drawer open
  const [openMathDrawers, setOpenMathDrawers] = useState<Record<string, boolean>>({});

  // 1. Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setStudies(parsed);
          setActiveStudyId(parsed[0].id);
          setActiveQuestionId(parsed[0].questions[0]?.id || "");
        }
      }
    } catch (e) {
      console.warn("Failed to load studies from localStorage", e);
    }
    setIsLoaded(true);
  }, []);

  // 2. Auto-save to localStorage on change
  useEffect(() => {
    if (isLoaded) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(studies));
      } catch (e) {
        console.warn("Failed to persist studies to localStorage", e);
      }
    }
  }, [studies, isLoaded]);

  const activeStudy = studies.find((s) => s.id === activeStudyId) || studies[0];
  const activeQuestion = activeStudy?.questions.find((q) => q.id === activeQuestionId) || activeStudy?.questions[0];
  const activePanel: Persona[] = activeStudy?.market === "IN" ? IN_PERSONAS : US_PERSONAS;

  const toggleMathDrawer = (personaId: string) => {
    setOpenMathDrawers((prev) => ({
      ...prev,
      [personaId]: !prev[personaId],
    }));
  };

  // Reset to initial default studies
  const handleResetStudies = () => {
    if (window.confirm("Reset all studies and questions to default presets?")) {
      setStudies(INITIAL_STUDIES);
      setActiveStudyId(INITIAL_STUDIES[0].id);
      setActiveQuestionId(INITIAL_STUDIES[0].questions[0]?.id || "");
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  // Create new survey
  const handleCreateStudy = () => {
    if (!newStudyTitle.trim()) return;

    const newStudy: SurveyStudy = {
      id: `study_${Date.now()}`,
      title: newStudyTitle.trim(),
      description: newStudyDesc.trim() || "Customer discovery and trade-off research study.",
      market: newStudyMarket,
      category: "Product Discovery",
      createdAt: "Just now",
      questions: [
        {
          id: `q_${Date.now()}_1`,
          questionText: "How do you currently solve this problem in your routine, and would you pay for an automated alternative?",
          actionA: "Adopt the automated alternative",
          baselineB: "Stick with manual routine",
        },
      ],
    };

    setStudies([newStudy, ...studies]);
    setActiveStudyId(newStudy.id);
    setActiveQuestionId(newStudy.questions[0].id);
    setShowNewStudyModal(false);
    setNewStudyTitle("");
    setNewStudyDesc("");
  };

  // Add question to active survey
  const handleAddQuestion = () => {
    if (!newQuestionText.trim()) return;

    const newQ: SurveyQuestion = {
      id: `q_${Date.now()}`,
      questionText: newQuestionText.trim(),
      actionA: newActionA.trim() || "Adopt proposed solution / take action",
      baselineB: newBaselineB.trim() || "Retain status quo / counterfactual default",
    };

    const updatedStudies = studies.map((st) => {
      if (st.id === activeStudy.id) {
        return {
          ...st,
          questions: [...st.questions, newQ],
        };
      }
      return st;
    });

    setStudies(updatedStudies);
    setActiveQuestionId(newQ.id);
    setNewQuestionText("");
    setNewActionA("");
    setNewBaselineB("");
    setIsAddingQuestion(false);
  };

  // Start inline editing a question
  const handleStartEditQuestion = (q: SurveyQuestion) => {
    setEditingQuestionId(q.id);
    setEditText(q.questionText);
    setEditActionA(q.actionA || "");
    setEditBaselineB(q.baselineB || "");
  };

  // Save edited question
  const handleSaveEditQuestion = () => {
    if (!editingQuestionId || !editText.trim()) return;

    const updatedStudies = studies.map((st) => {
      if (st.id === activeStudy.id) {
        return {
          ...st,
          questions: st.questions.map((q) => {
            if (q.id === editingQuestionId) {
              return {
                ...q,
                questionText: editText.trim(),
                actionA: editActionA.trim() || "Adopt proposed solution",
                baselineB: editBaselineB.trim() || "Retain status quo",
              };
            }
            return q;
          }),
        };
      }
      return st;
    });

    setStudies(updatedStudies);
    setEditingQuestionId(null);
  };

  // Duplicate an existing question
  const handleDuplicateQuestion = (q: SurveyQuestion) => {
    const duplicated: SurveyQuestion = {
      id: `q_${Date.now()}`,
      questionText: `${q.questionText} (Copy)`,
      actionA: q.actionA,
      baselineB: q.baselineB,
      expectedOutcomes: q.expectedOutcomes,
    };

    const updatedStudies = studies.map((st) => {
      if (st.id === activeStudy.id) {
        return {
          ...st,
          questions: [...st.questions, duplicated],
        };
      }
      return st;
    });

    setStudies(updatedStudies);
    setActiveQuestionId(duplicated.id);
  };

  // Delete a question
  const handleDeleteQuestion = (qId: string) => {
    if (activeStudy.questions.length <= 1) {
      alert("A survey must contain at least one question.");
      return;
    }

    const updatedStudies = studies.map((st) => {
      if (st.id === activeStudy.id) {
        const filtered = st.questions.filter((q) => q.id !== qId);
        return { ...st, questions: filtered };
      }
      return st;
    });

    setStudies(updatedStudies);
    if (activeQuestionId === qId) {
      const remaining = activeStudy.questions.filter((q) => q.id !== qId);
      setActiveQuestionId(remaining[0]?.id || "");
    }
  };

  // Run simulation on active question
  const handleSimulateActiveQuestion = () => {
    if (!activeQuestion) return;

    setIsSimulating(true);
    setSimulationLogText("Mapping mental account & category directives...");

    setTimeout(() => {
      setSimulationLogText("Computing Dominant Bottleneck RMS friction & loss aversion (λ)...");
    }, 400);

    setTimeout(() => {
      setSimulationLogText("Evaluating McFadden discrete choice models across 5 personas...");
    }, 850);

    setTimeout(() => {
      const result = runSimulation({
        question: activeQuestion.questionText,
        market: activeStudy.market,
        actionA: activeQuestion.actionA,
        baselineB: activeQuestion.baselineB,
      });

      const updatedStudies = studies.map((st) => {
        if (st.id === activeStudy.id) {
          return {
            ...st,
            questions: st.questions.map((q) => {
              if (q.id === activeQuestion.id) {
                return { ...q, simulatedResult: result };
              }
              return q;
            }),
          };
        }
        return st;
      });

      setStudies(updatedStudies);
      setIsSimulating(false);
    }, 1300);
  };

  // Copy Markdown to Clipboard
  const handleCopyReport = () => {
    if (!activeStudy || !activeQuestion) return;
    const reportText = generateMarkdownReport(activeStudy, activeQuestion);
    navigator.clipboard.writeText(reportText);
    setCopiedStatus(true);
    setTimeout(() => setCopiedStatus(false), 2000);
  };

  // Download Markdown file
  const handleDownloadMarkdown = () => {
    if (!activeStudy || !activeQuestion) return;
    const reportText = generateMarkdownReport(activeStudy, activeQuestion);
    const filename = `${activeStudy.title.replace(/[^a-zA-Z0-9]/g, "_")}_report.md`;
    downloadFile(filename, reportText, "text/markdown");
  };

  // Download CSV spreadsheet
  const handleDownloadCsv = () => {
    if (!activeStudy || !activeQuestion) return;
    const csvText = generateCsvReport(activeStudy, activeQuestion);
    const filename = `${activeStudy.title.replace(/[^a-zA-Z0-9]/g, "_")}_personas.csv`;
    downloadFile(filename, csvText, "text/csv");
  };

  const currentResult: SimulationResult | undefined = activeQuestion?.simulatedResult;

  return (
    <div className="space-y-6">
      {/* Editorial Research Header & Study Notebook Bar */}
      <div className="bg-white border border-stone-200/90 rounded-2xl p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start space-x-3.5">
          <div className="w-9 h-9 rounded-xl bg-[#FAF9F5] border border-stone-200 text-stone-700 flex items-center justify-center font-medium shrink-0 mt-0.5">
            <BookOpen className="w-4 h-4 text-stone-700" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] font-mono uppercase tracking-wider text-stone-400">Research Notebook</span>
              <span className="text-stone-300">/</span>
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-stone-100 text-stone-700 border border-stone-200">
                {activeStudy.market === "IN" ? "India Regional Panel" : "US National Panel"}
              </span>
            </div>
            <h1 className="text-base font-serif font-bold text-stone-900 mt-0.5">{activeStudy.title}</h1>
            <p className="text-xs text-stone-500 font-sans mt-0.5 max-w-xl line-clamp-1">{activeStudy.description}</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0 flex-wrap">
          <select
            value={activeStudy.id}
            onChange={(e) => {
              const selected = studies.find((s) => s.id === e.target.value);
              if (selected) {
                setActiveStudyId(selected.id);
                setActiveQuestionId(selected.questions[0]?.id || "");
              }
            }}
            className="bg-[#FAF9F5] border border-stone-300/80 rounded-lg px-3 py-1.5 text-xs font-medium text-stone-800 focus:outline-none focus:border-stone-500 cursor-pointer"
          >
            {studies.map((st) => (
              <option key={st.id} value={st.id}>
                {st.title} ({st.questions.length} Inquiries)
              </option>
            ))}
          </select>

          <button
            onClick={() => setShowNewStudyModal(true)}
            className="flex items-center space-x-1.5 bg-stone-900 hover:bg-stone-800 text-white text-xs font-medium px-3 py-1.5 rounded-lg transition shadow-2xs"
          >
            <FolderPlus className="w-3.5 h-3.5" />
            <span>New Notebook</span>
          </button>

          {/* Export Report Trigger */}
          <button
            onClick={() => setShowExportModal(true)}
            className="flex items-center space-x-1.5 bg-[#FAF9F5] hover:bg-[#F3F2EC] border border-stone-300 text-stone-800 text-xs font-medium px-3 py-1.5 rounded-lg transition"
            title="Export findings as PRD / Markdown / CSV"
          >
            <Download className="w-3.5 h-3.5 text-stone-600" />
            <span>Export Notes</span>
          </button>

          {/* Reset button */}
          <button
            onClick={handleResetStudies}
            className="text-stone-400 hover:text-stone-700 p-1.5 rounded-lg transition"
            title="Reset to default preset studies"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* MAIN LEFT-RIGHT SPLIT WORKBENCH */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: INQUIRY OUTLINE (Sticky locked scrolling) */}
        <div className="lg:col-span-5 lg:sticky lg:top-20 lg:max-h-[calc(100vh-6.5rem)] lg:overflow-y-auto space-y-4 pr-1 pb-8">
          <div className="bg-white border border-stone-200/90 rounded-2xl p-5 shadow-2xs space-y-4">
            <div className="flex items-center justify-between border-b border-stone-100 pb-3">
              <div>
                <h2 className="text-sm font-bold text-stone-900 tracking-tight">
                  Inquiry Outline ({activeStudy.questions.length})
                </h2>
                <p className="text-xs text-stone-500 mt-0.5">Hypotheses tested against calibrated synthetic panels</p>
              </div>
              <span className="text-[11px] font-mono text-stone-400 bg-stone-50 px-2 py-0.5 rounded border border-stone-200">
                Auto-Saved
              </span>
            </div>

            {/* Questions List (Editorial Notebook Outline) */}
            <div className="space-y-2.5">
              {activeStudy.questions.map((q, idx) => {
                const isSelected = q.id === activeQuestion?.id;
                const hasResult = !!q.simulatedResult;
                const isEditing = editingQuestionId === q.id;

                if (isEditing) {
                  return (
                    <div key={q.id} className="bg-[#FAF9F5] border border-stone-400 rounded-xl p-4 space-y-3">
                      <div className="flex items-center justify-between text-xs font-bold text-stone-800">
                        <span>Editing Inquiry Section 1.{idx + 1}:</span>
                        <button
                          onClick={() => setEditingQuestionId(null)}
                          className="text-stone-400 hover:text-stone-700 text-[11px]"
                        >
                          Cancel
                        </button>
                      </div>
                      <textarea
                        rows={2}
                        value={editText}
                        onChange={(e) => setEditText(e.target.value)}
                        className="w-full bg-white border border-stone-300 rounded-lg p-2.5 text-xs text-stone-900 focus:outline-none focus:border-stone-500"
                      />
                      <div className="space-y-1.5 text-xs">
                        <input
                          type="text"
                          value={editActionA}
                          onChange={(e) => setEditActionA(e.target.value)}
                          placeholder="Action A (Target)"
                          className="w-full bg-white border border-stone-300 rounded-lg p-2 text-xs text-stone-900 focus:outline-none focus:border-stone-500"
                        />
                        <input
                          type="text"
                          value={editBaselineB}
                          onChange={(e) => setEditBaselineB(e.target.value)}
                          placeholder="Baseline B (Status Quo)"
                          className="w-full bg-white border border-stone-300 rounded-lg p-2 text-xs text-stone-900 focus:outline-none focus:border-stone-500"
                        />
                      </div>
                      <div className="flex justify-end pt-1">
                        <button
                          onClick={handleSaveEditQuestion}
                          className="bg-stone-900 text-white font-medium text-xs px-3.5 py-1.5 rounded-lg transition"
                        >
                          Save Changes
                        </button>
                      </div>
                    </div>
                  );
                }

                if (isSelected) {
                  return (
                    <div
                      key={q.id}
                      className="rounded-xl border border-stone-300/90 bg-[#F7F6F1] border-l-4 border-l-stone-900 transition p-4 space-y-3 shadow-2xs"
                    >
                      <div className="flex items-center justify-between text-[11px] text-stone-500 font-mono">
                        <span className="font-bold text-stone-900">Section 1.{idx + 1}</span>
                        {hasResult ? (
                          <span className="font-sans font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200/50">
                            Simulated • {q.simulatedResult?.weightedScore}% Adoption
                          </span>
                        ) : (
                          <span className="text-stone-400">Ready for Simulation</span>
                        )}
                      </div>

                      <p className="font-serif text-[13.5px] font-semibold text-stone-900 leading-snug">
                        {q.questionText}
                      </p>

                      {/* Action A vs Baseline B */}
                      <div className="text-[11px] text-stone-600 space-y-1 bg-white/80 p-2.5 rounded-lg border border-stone-200/60 font-sans">
                        <div>
                          <strong className="text-stone-900 font-medium">Action A: </strong>
                          <span>{q.actionA || "Choose Option A (Adopt innovation)"}</span>
                        </div>
                        <div>
                          <strong className="text-stone-500 font-medium">Baseline B: </strong>
                          <span>{q.baselineB || "Choose Option B (Retain status quo)"}</span>
                        </div>
                      </div>

                      {/* Inline Actions (Edit, Duplicate, Delete) */}
                      <div className="flex items-center justify-between pt-1 border-t border-stone-200/60 text-[11px] text-stone-500 font-sans">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => handleStartEditQuestion(q)}
                            className="flex items-center space-x-1 hover:text-stone-900 transition"
                          >
                            <Edit2 className="w-3 h-3" />
                            <span>Edit</span>
                          </button>
                          <span>·</span>
                          <button
                            onClick={() => handleDuplicateQuestion(q)}
                            className="flex items-center space-x-1 hover:text-stone-900 transition"
                          >
                            <CopyPlus className="w-3 h-3" />
                            <span>Duplicate</span>
                          </button>
                        </div>

                        <button
                          onClick={() => handleDeleteQuestion(q.id)}
                          className="flex items-center space-x-1 text-rose-600 hover:text-rose-800 transition"
                        >
                          <Trash2 className="w-3 h-3" />
                          <span>Delete</span>
                        </button>
                      </div>

                      {/* Simulate Button */}
                      <div className="pt-1">
                        <button
                          onClick={handleSimulateActiveQuestion}
                          disabled={isSimulating}
                          className="w-full flex items-center justify-center space-x-2 bg-stone-900 hover:bg-stone-800 disabled:opacity-50 text-white font-medium text-xs py-2.5 px-4 rounded-lg transition shadow-2xs"
                        >
                          {isSimulating ? (
                            <>
                              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                              <span>Simulating Panel...</span>
                            </>
                          ) : (
                            <>
                              <Play className="w-3 h-3 fill-white" />
                              <span>Simulate Section 1.{idx + 1}</span>
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  );
                }

                // Inactive Question in list
                return (
                  <div
                    key={q.id}
                    onClick={() => setActiveQuestionId(q.id)}
                    className="p-3.5 rounded-xl border border-stone-200/70 hover:border-stone-300 hover:bg-[#FAF9F5] bg-white transition cursor-pointer space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-[11px] text-stone-400 font-mono">
                      <span>Section 1.{idx + 1}</span>
                      {hasResult ? (
                        <span className="font-sans font-medium text-emerald-700">Simulated ({q.simulatedResult?.weightedScore}%)</span>
                      ) : (
                        <span className="text-stone-400">Ready</span>
                      )}
                    </div>
                    <p className="text-xs text-stone-700 leading-snug line-clamp-2">
                      {q.questionText}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* + Add New Inquiry Form */}
            <div className="pt-2 border-t border-stone-100">
              {!isAddingQuestion ? (
                <button
                  onClick={() => setIsAddingQuestion(true)}
                  className="w-full text-xs font-serif italic text-stone-500 hover:text-stone-900 py-2.5 px-3 rounded-xl border border-dashed border-stone-300/80 hover:border-stone-400 hover:bg-[#FAF9F5] transition flex items-center justify-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Insert new inquiry into study notebook...</span>
                </button>
              ) : (
                <div className="bg-[#FAF9F5] border border-stone-300 rounded-xl p-3.5 space-y-3">
                  <div className="flex items-center justify-between text-xs font-semibold text-stone-800">
                    <span>New Inquiry Prompt:</span>
                    <button
                      onClick={() => setIsAddingQuestion(false)}
                      className="text-stone-500 hover:text-stone-800 text-[11px]"
                    >
                      Cancel
                    </button>
                  </div>

                  <textarea
                    rows={2}
                    value={newQuestionText}
                    onChange={(e) => setNewQuestionText(e.target.value)}
                    placeholder="Type your discovery question or feature hypothesis..."
                    className="w-full bg-white border border-stone-300 rounded-lg p-2.5 text-xs text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-500"
                  />

                  <div className="space-y-1.5 text-xs">
                    <input
                      type="text"
                      value={newActionA}
                      onChange={(e) => setNewActionA(e.target.value)}
                      placeholder="Action A (e.g. Switch to new service)"
                      className="w-full bg-white border border-stone-300 rounded-lg p-2 text-xs text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-500"
                    />
                    <input
                      type="text"
                      value={newBaselineB}
                      onChange={(e) => setNewBaselineB(e.target.value)}
                      placeholder="Baseline B (e.g. Retain current routine)"
                      className="w-full bg-white border border-stone-300 rounded-lg p-2 text-xs text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-500"
                    />
                  </div>

                  <div className="flex justify-end pt-1">
                    <button
                      onClick={handleAddQuestion}
                      disabled={!newQuestionText.trim()}
                      className="flex items-center space-x-1.5 bg-stone-900 hover:bg-stone-800 disabled:opacity-50 text-white font-medium text-xs px-3.5 py-2 rounded-lg transition shadow-2xs"
                    >
                      <Plus className="w-3.5 h-3.5" />
                      <span>Append Inquiry</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: 5 PERSONA TRANSCRIPTS (Sticky locked scrolling) */}
        <div className="lg:col-span-7 lg:sticky lg:top-20 lg:max-h-[calc(100vh-6.5rem)] lg:overflow-y-auto space-y-4 pr-1 pb-8">
          {/* Header of Right Side: Context (NO MACRO SCORE) */}
          <div className="bg-white border border-stone-200/90 rounded-2xl p-4 shadow-2xs flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-stone-400">
                Field Notes &amp; Participant Transcripts
              </span>
              <h3 className="text-xs font-serif italic text-stone-800 line-clamp-1 mt-0.5" title={activeQuestion?.questionText}>
                “{activeQuestion?.questionText}”
              </h3>
            </div>
            <span className="text-xs font-mono font-medium px-2.5 py-1 rounded-md bg-[#FAF9F5] text-stone-700 border border-stone-200 shrink-0">
              {activeStudy.market === "IN" ? "🇮🇳 5 Indian Personas" : "🇺🇸 5 US Personas"}
            </span>
          </div>

          {/* Simulation in-progress Banner */}
          {isSimulating && (
            <div className="bg-[#FAF9F5] p-4 rounded-xl border border-stone-300 text-xs text-stone-800 flex items-center space-x-2.5 animate-pulse">
              <Sparkles className="w-4 h-4 text-stone-600 shrink-0" />
              <span className="font-medium font-serif italic">{simulationLogText}</span>
            </div>
          )}

          {/* 5 PERSONA TRANSCRIPTS (Editorial Field Notes) */}
          <div className="space-y-4">
            {activePanel.map((persona) => {
              const pResult: PersonaSimulationResult | undefined = currentResult?.personaResults.find(
                (r) => r.personaId === persona.id
              );

              const isSimulated = !!pResult;
              const isYes = pResult?.decisionStance === "YES";
              const score = pResult ? pResult.targetMetricScore : 50.0;
              const isMathOpen = !!openMathDrawers[persona.id];

              return (
                <article
                  key={persona.id}
                  className="bg-white border border-stone-200/90 rounded-2xl p-5 shadow-2xs space-y-3.5 transition hover:border-stone-300"
                >
                  {/* Top Bar: Avatar, Identity, Demographics, Probability */}
                  <div className="flex items-start justify-between gap-3 pb-2.5 border-b border-stone-100">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 rounded-lg bg-stone-900 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs mt-0.5">
                        {persona.avatarInitial}
                      </div>
                      <div>
                        <div className="flex items-baseline space-x-2">
                          <h4 className="font-serif font-bold text-stone-900 text-sm">{persona.name}</h4>
                          <span className="text-xs text-stone-400 font-sans">· {persona.demographics.occupation}</span>
                        </div>
                        <p className="text-[11px] text-stone-400 font-sans mt-0.5">
                          {persona.demographics.geography} · Budget: {persona.market === "IN" ? `₹${persona.psychographics.priceCeilingMonthly}` : `$${persona.psychographics.priceCeilingMonthly}`}/mo · {Math.round(persona.populationWeight * 100)}% Weight
                        </p>
                      </div>
                    </div>

                    {/* Stance Pill & Score in Monospace */}
                    {isSimulated ? (
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
                    ) : (
                      <span className="font-mono text-xs text-stone-400 bg-stone-50 px-2 py-0.5 rounded border border-stone-200">
                        Awaiting Run
                      </span>
                    )}
                  </div>

                  {/* 1. VERBATIM VOICE RESPONSE (Hero Pull-Quote in Editorial Serif) */}
                  <div className="py-1">
                    {isSimulated ? (
                      <blockquote className="font-serif text-stone-800 text-[13.5px] sm:text-sm leading-relaxed pl-3.5 border-l-2 border-stone-300 italic py-0.5">
                        “{pResult.responseText}”
                      </blockquote>
                    ) : (
                      <blockquote className="font-serif text-stone-400 text-xs sm:text-[13px] leading-relaxed pl-3.5 border-l-2 border-stone-200 italic py-0.5">
                        Run simulation on Section 1.{activeStudy.questions.findIndex((q) => q.id === activeQuestion?.id) + 1} to record {persona.name}’s verbatim reaction.
                      </blockquote>
                    )}
                  </div>

                  {/* 2. DRIVER / FRICTION & TELEMETRY TOGGLE */}
                  <div className="pt-2 border-t border-stone-100 flex items-center justify-between text-xs text-stone-600 gap-2">
                    <div className="text-[11.5px] truncate">
                      {isSimulated ? (
                        isYes ? (
                          <span>
                            <strong className="font-semibold text-stone-900 font-sans">Primary Driver: </strong>
                            <span className="text-stone-700">Expense ease &amp; perceived utility exceeding switching hurdle</span>
                          </span>
                        ) : (
                          <span>
                            <strong className="font-semibold text-amber-950 font-sans">Primary Friction: </strong>
                            <span className="text-stone-700">{pResult.primaryObjection || "Switching barrier exceeding utility gain"}</span>
                          </span>
                        )
                      ) : (
                        <span className="text-stone-400 font-sans">Decision parameters uncalibrated for active inquiry</span>
                      )}
                    </div>

                    <button
                      onClick={() => toggleMathDrawer(persona.id)}
                      className="text-[11px] font-sans font-semibold text-stone-600 hover:text-stone-900 shrink-0 flex items-center space-x-1 transition"
                    >
                      <span>{isMathOpen ? "Hide Telemetry" : "Show Telemetry"}</span>
                      {isMathOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </button>
                  </div>

                  {/* 3. EXPANDED PSYCHOMETRIC TELEMETRY & DECISION FOOTNOTE */}
                  {isMathOpen && (
                    <div className="mt-2.5 p-3.5 bg-[#FAF9F5] border border-stone-200/80 rounded-xl space-y-3 text-xs text-stone-700 animate-fadeIn">
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-[11px] font-mono">
                        <div className="bg-white p-2 rounded-lg border border-stone-200/80">
                          <div className="text-stone-400 text-[10px] font-sans">Net Utility (ΔV)</div>
                          <div className="font-bold text-stone-900 mt-0.5">
                            {pResult ? `${pResult.deltaV > 0 ? "+" : ""}${pResult.deltaV}` : "0.00"}
                          </div>
                        </div>
                        <div className="bg-white p-2 rounded-lg border border-stone-200/80">
                          <div className="text-stone-400 text-[10px] font-sans">Loss Aversion (λ)</div>
                          <div className="font-bold text-stone-900 mt-0.5">
                            {persona.psychographics.lossAversionBias}
                          </div>
                        </div>
                        <div className="bg-white p-2 rounded-lg border border-stone-200/80">
                          <div className="text-stone-400 text-[10px] font-sans">Friction (Feff)</div>
                          <div className="font-bold text-stone-900 mt-0.5">
                            {pResult ? `${pResult.effectiveFriction} / 10` : "3.0 / 10"}
                          </div>
                        </div>
                        <div className="bg-white p-2 rounded-lg border border-stone-200/80">
                          <div className="text-stone-400 text-[10px] font-sans">Persona Shift (Δvp)</div>
                          <div className="font-bold text-stone-900 mt-0.5">
                            {pResult ? `${pResult.personaShift > 0 ? "+" : ""}${pResult.personaShift}` : "0.0"}
                          </div>
                        </div>
                      </div>

                      {/* Anti-Sycophancy Negative Directives */}
                      <div className="pt-2 border-t border-stone-200/60 text-[11px] font-sans">
                        <span className="font-semibold text-stone-900 block mb-1">
                          Anti-Sycophancy Negative Directives:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5 text-stone-600">
                          {persona.guardrailRules.map((rule, rIdx) => (
                            <li key={rIdx}>{rule}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        </div>
      </div>

      {/* CREATE NEW STUDY MODAL (Warm Laboratory Paper Style) */}
      {showNewStudyModal && (
        <div className="fixed inset-0 bg-stone-900/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-stone-300 rounded-2xl max-w-lg w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-stone-200 pb-3">
              <h3 className="font-bold text-stone-900 text-base">Create New Survey / Study</h3>
              <button
                onClick={() => setShowNewStudyModal(false)}
                className="text-stone-400 hover:text-stone-700 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-stone-800 font-semibold block mb-1">Study / Survey Title:</label>
                <input
                  type="text"
                  value={newStudyTitle}
                  onChange={(e) => setNewStudyTitle(e.target.value)}
                  placeholder="e.g. Q1 Pricing Sensitivity & Feature Add-On Research"
                  className="w-full bg-[#FAF9F5] border border-stone-300 rounded-lg p-2.5 text-stone-900 focus:outline-none focus:border-stone-500"
                />
              </div>

              <div>
                <label className="text-stone-800 font-semibold block mb-1">Research Objective / Scope:</label>
                <textarea
                  rows={2}
                  value={newStudyDesc}
                  onChange={(e) => setNewStudyDesc(e.target.value)}
                  placeholder="Briefly state what behavioral trade-offs you want to measure..."
                  className="w-full bg-[#FAF9F5] border border-stone-300 rounded-lg p-2.5 text-stone-900 focus:outline-none focus:border-stone-500"
                />
              </div>

              <div>
                <label className="text-stone-800 font-semibold block mb-1">Target Geographic Cohort:</label>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={() => setNewStudyMarket("US")}
                    className={`flex-1 p-2 rounded-lg border font-semibold ${
                      newStudyMarket === "US"
                        ? "bg-stone-900 text-white border-stone-900"
                        : "bg-[#FAF9F5] border-stone-300 text-stone-700"
                    }`}
                  >
                    🇺🇸 US Consumer Panel
                  </button>
                  <button
                    type="button"
                    onClick={() => setNewStudyMarket("IN")}
                    className={`flex-1 p-2 rounded-lg border font-semibold ${
                      newStudyMarket === "IN"
                        ? "bg-stone-900 text-white border-stone-900"
                        : "bg-[#FAF9F5] border-stone-300 text-stone-700"
                    }`}
                  >
                    🇮🇳 India Consumer Panel
                  </button>
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-stone-200">
              <button
                onClick={() => setShowNewStudyModal(false)}
                className="px-4 py-2 rounded-lg text-xs font-semibold text-stone-500 hover:text-stone-900"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateStudy}
                disabled={!newStudyTitle.trim()}
                className="bg-stone-900 hover:bg-stone-800 disabled:opacity-50 text-white font-semibold text-xs px-5 py-2 rounded-lg transition"
              >
                Create Study
              </button>
            </div>
          </div>
        </div>
      )}

      {/* EXPORT FINDINGS MODAL */}
      {showExportModal && (
        <div className="fixed inset-0 bg-stone-900/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-stone-300 rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-stone-200 pb-3">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-stone-700" />
                <h3 className="font-bold text-stone-900 text-base">Export Research Findings</h3>
              </div>
              <button
                onClick={() => setShowExportModal(false)}
                className="text-stone-400 hover:text-stone-700 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-stone-600 leading-relaxed">
              Export persona verbatim responses, adoption splits, and objections for your PRD, Slack updates, or executive reviews.
            </p>

            <div className="space-y-2.5 pt-1">
              {/* Copy Markdown for Slack / Notion */}
              <button
                onClick={handleCopyReport}
                className="w-full flex items-center justify-between p-3 rounded-xl border border-stone-200 hover:border-stone-400 bg-[#FAF9F5] text-left transition"
              >
                <div className="flex items-center space-x-3">
                  <Copy className="w-4 h-4 text-stone-600" />
                  <div>
                    <div className="text-xs font-semibold text-stone-900">Copy Summary to Clipboard</div>
                    <div className="text-[10px] text-stone-500">Formatted Markdown for Notion, Linear, or Slack</div>
                  </div>
                </div>
                {copiedStatus ? (
                  <span className="text-xs font-bold text-emerald-700 flex items-center space-x-1">
                    <Check className="w-3.5 h-3.5" />
                    <span>Copied!</span>
                  </span>
                ) : (
                  <span className="text-xs font-semibold text-stone-600">Copy</span>
                )}
              </button>

              {/* Download Markdown PRD */}
              <button
                onClick={handleDownloadMarkdown}
                className="w-full flex items-center justify-between p-3 rounded-xl border border-stone-200 hover:border-stone-400 bg-white text-left transition"
              >
                <div className="flex items-center space-x-3">
                  <Download className="w-4 h-4 text-stone-600" />
                  <div>
                    <div className="text-xs font-semibold text-stone-900">Download Markdown Report (.md)</div>
                    <div className="text-[10px] text-stone-500">Complete structured research document</div>
                  </div>
                </div>
                <span className="text-xs font-semibold text-stone-600">.md</span>
              </button>

              {/* Download CSV spreadsheet */}
              <button
                onClick={handleDownloadCsv}
                className="w-full flex items-center justify-between p-3 rounded-xl border border-stone-200 hover:border-stone-400 bg-white text-left transition"
              >
                <div className="flex items-center space-x-3">
                  <Download className="w-4 h-4 text-stone-600" />
                  <div>
                    <div className="text-xs font-semibold text-stone-900">Download Raw Data (CSV)</div>
                    <div className="text-[10px] text-stone-500">Open in Excel or Google Sheets</div>
                  </div>
                </div>
                <span className="text-xs font-semibold text-stone-600">.csv</span>
              </button>
            </div>

            <div className="flex justify-end pt-2 border-t border-stone-200">
              <button
                onClick={() => setShowExportModal(false)}
                className="bg-stone-100 hover:bg-stone-200 text-stone-800 font-medium text-xs px-4 py-2 rounded-lg transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
