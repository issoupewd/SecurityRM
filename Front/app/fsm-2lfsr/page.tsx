"use client"

import { useState } from "react"
import Link from "next/link"
import LFSRCard from "@/components/lfsr-card"
import FSM2LFSRCard from "@/components/fsm-2lfsr-card"

interface LFSRResult {
  outputs: number[]
  states: number[][]
  period: number
  theoretical_period?: number
}

export default function FSM2LFSRPage() {
  const [r1, setR1] = useState<LFSRResult | null>(null)
  const [r2, setR2] = useState<LFSRResult | null>(null)

  return (
    <main className="min-h-screen flex flex-col bg-gradient-to-b from-slate-950 via-purple-950/40 to-slate-950">
      {/* Back button and header */}
      <div className="border-b border-purple-500/20 bg-purple-950/30 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <Link
            href="/"
            className="text-purple-300 hover:text-purple-200 transition-colors text-sm flex items-center gap-2"
          >
            ← Back to Home
          </Link>
        </div>
      </div>

      {/* Page header */}
      <div className="border-b border-purple-500/20 bg-purple-900/20 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-blue-300 mb-2">
            FSM Key Generator (2 LFSR)
          </h1>
          <p className="text-gray-400">Two LFSRs combined by an FSM where R1 controls outputs and R2 supplies bits.</p>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8 space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <LFSRCard
            title="R1 (Controller - 3 bits)"
            labels={["S2", "S1", "S0"]}
            defaultState={[0, 0, 1]}
            defaultTaps={[0, 2]}
            onGenerate={setR1}
          />
          <LFSRCard
            title="R2 (Data Source - 5 bits)"
            labels={["S4", "S3", "S2", "S1", "S0"]}
            defaultState={[0, 0, 1, 0, 1]}
            defaultTaps={[2, 4]}
            onGenerate={setR2}
          />
        </div>

        {r1 && r2 && <FSM2LFSRCard r1={r1} r2={r2} />}
      </div>

      {/* Footer */}
      <div className="border-t border-purple-500/20 bg-purple-950/30 backdrop-blur-sm mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-sm text-gray-400">
          FSM keystream generator based on two LFSRs (R1 controls, R2 supplies) for educational security applications.
        </div>
      </div>
    </main>
  )
}
