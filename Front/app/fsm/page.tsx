'use client'

import { useState } from 'react'
import Link from 'next/link'
import Header from '@/components/header'
import Footer from '@/components/footer'
import LFSRCard from '@/components/lfsr-card'
import FSMCard from '@/components/fsm-card'

interface LFSRResult {
  outputs: number[]
  states: number[][]
  period: number
  theoretical_period?: number
}

export default function FSMPage() {
  const [r1, setR1] = useState<LFSRResult | null>(null)
  const [r2, setR2] = useState<LFSRResult | null>(null)
  const [r3, setR3] = useState<LFSRResult | null>(null)

  return (
    <main className="min-h-screen flex flex-col bg-gradient-to-b from-slate-950 via-purple-950/40 to-slate-950">
      {/* Back button and header */}
      <div className="border-b border-purple-500/20 bg-purple-950/30 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <Link href="/" className="text-purple-300 hover:text-purple-200 transition-colors text-sm flex items-center gap-2">
            ← Back to Home
          </Link>
        </div>
      </div>

      {/* Page header */}
      <div className="border-b border-purple-500/20 bg-purple-900/20 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-blue-300 mb-2">
            FSM Key Generator
          </h1>
          <p className="text-gray-400">
            Three LFSRs combined by an alternating-step FSM to produce a keystream.
          </p>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8 space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <LFSRCard
            title="R1 (Controller)"
            labels={['S2', 'S1', 'S0']}
            defaultState={[0, 0, 1]}
            defaultTaps={[0, 2]}
            onGenerate={setR1}
          />
          <LFSRCard
            title="R2"
            labels={['S3', 'S2', 'S1', 'S0']}
            defaultState={[1, 0, 1, 1]}
            defaultTaps={[0, 1]}
            onGenerate={setR2}
          />
          <LFSRCard
            title="R3"
            labels={['S4', 'S3', 'S2', 'S1', 'S0']}
            defaultState={[0, 1, 0, 0, 1]}
            defaultTaps={[0, 1, 2, 4]}
            onGenerate={setR3}
          />
        </div>

        {r1 && r2 && r3 && (
          <FSMCard r1={r1} r2={r2} r3={r3} />
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-purple-500/20 bg-purple-950/30 backdrop-blur-sm mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-sm text-gray-400">
          FSM keystream generator based on three LFSRs (two controlled by one) for educational security applications.
        </div>
      </div>
    </main>
  )
}
