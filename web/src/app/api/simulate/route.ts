import { NextRequest, NextResponse } from "next/server";
import { runSimulation } from "@/services/simulationEngine";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { question, market, category, actionA, baselineB, presetId } = body;

    if (!question || typeof question !== "string") {
      return NextResponse.json({ error: "Missing 'question' parameter" }, { status: 400 });
    }

    const result = runSimulation({
      question,
      market,
      category,
      actionA,
      baselineB,
      presetId,
    });

    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json({ error: error?.message || "Internal server error" }, { status: 500 });
  }
}
