'use client'

import { useState } from 'react'
import { Download } from 'lucide-react'

interface FSMCardProps {
  r1: any
  r2: any
  r3: any
}

export default function FSMCard({ r1, r2, r3 }: FSMCardProps) {
  const [bMinus1, setBMinus1] = useState(0)
  const [cMinus1, setCMinus1] = useState(0)
  const [steps, setSteps] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const runFSM = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:5000/run_fsm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          r1: r1.outputs,
          r2: r2.outputs,
          r3: r3.outputs,
          b_minus1: bMinus1,
          c_minus1: cMinus1,
          steps: steps ? parseInt(steps) : undefined,
        }),
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error running FSM:', error)
    } finally {
      setLoading(false)
    }
  }

  const exportCSV = () => {
    if (!result) return
    
    // Build CSV from backend data: step, R1, R2, R3, FSM
    let csv = 'step,R1,R2,R3,FSM\n'
    const maxLen = Math.max(r1.outputs.length, r2.outputs.length, r3.outputs.length, result.fsm.length)
    
    for (let i = 0; i < maxLen; i++) {
      const r1Bit = r1.outputs[i] !== undefined ? r1.outputs[i] : ''
      const r2Bit = r2.outputs[i] !== undefined ? r2.outputs[i] : ''
      const r3Bit = r3.outputs[i] !== undefined ? r3.outputs[i] : ''
      const fsmBit = result.fsm[i] !== undefined ? result.fsm[i] : ''
      csv += `${i},${r1Bit},${r2Bit},${r3Bit},${fsmBit}\n`
    }

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'fsm_keystream.csv'
    a.click()
  }

  return (
    <div className="bg-blue-900/20 backdrop-blur-sm border border-blue-500/30 rounded-lg p-6 space-y-6 hover:border-blue-400/50 transition-colors">
      <h2 className="text-2xl font-semibold text-blue-100">Alternating-Step FSM</h2>

      {/* Input summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm bg-blue-950/30 p-4 rounded-md border border-blue-500/20">
        <div>
          <p className="text-blue-300/70 text-xs">R1 Period</p>
          <p className="font-semibold text-blue-100">{r1.period}</p>
        </div>
        <div>
          <p className="text-blue-300/70 text-xs">R2 Period</p>
          <p className="font-semibold text-blue-100">{r2.period}</p>
        </div>
        <div>
          <p className="text-blue-300/70 text-xs">R3 Period</p>
          <p className="font-semibold text-blue-100">{r3.period}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm text-blue-300/70">b₋₁ (Initial R2 bit)</label>
          <div className="flex gap-2">
            {[0, 1].map((val) => (
              <button
                key={val}
                onClick={() => setBMinus1(val)}
                className={`flex-1 py-2 rounded-md font-semibold transition-all ${
                  bMinus1 === val
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-slate-700/30 text-slate-400 hover:bg-slate-700/50'
                }`}
              >
                {val}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-blue-300/70">c₋₁ (Initial R3 bit)</label>
          <div className="flex gap-2">
            {[0, 1].map((val) => (
              <button
                key={val}
                onClick={() => setCMinus1(val)}
                className={`flex-1 py-2 rounded-md font-semibold transition-all ${
                  cMinus1 === val
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-slate-700/30 text-slate-400 hover:bg-slate-700/50'
                }`}
              >
                {val}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-blue-300/70">Steps (optional)</label>
          <input
            type="number"
            value={steps}
            onChange={(e) => setSteps(e.target.value)}
            placeholder="Leave empty for default"
            className="w-full bg-slate-800/50 border border-blue-500/30 rounded-md px-3 py-2 text-blue-100 placeholder-slate-500 focus:outline-none focus:border-blue-400/50"
          />
        </div>
      </div>

      <button
        onClick={runFSM}
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 text-white font-semibold py-3 rounded-md transition-all shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50"
      >
        {loading ? 'Running FSM...' : 'Run FSM'}
      </button>

      {result && (
        <div className="space-y-4 border-t border-blue-500/20 pt-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
            <div className="bg-blue-800/20 p-3 rounded-md">
              <p className="text-blue-300/70 text-xs">Steps</p>
              <p className="text-lg font-semibold text-blue-100">{result.stats.steps}</p>
            </div>
            <div className="bg-blue-800/20 p-3 rounded-md">
              <p className="text-blue-300/70 text-xs">Ones</p>
              <p className="text-lg font-semibold text-blue-100">{result.stats.ones}</p>
            </div>
            <div className="bg-blue-800/20 p-3 rounded-md">
              <p className="text-blue-300/70 text-xs">Zeros</p>
              <p className="text-lg font-semibold text-blue-100">{result.stats.zeros}</p>
            </div>
            <div className="bg-blue-800/20 p-3 rounded-md">
              <p className="text-blue-300/70 text-xs">Practical Period</p>
              <p className="text-lg font-semibold text-blue-100">{result.stats.practical_period}</p>
            </div>
          </div>

          <div className="bg-cyan-800/20 p-4 rounded-md">
            <p className="text-cyan-300/70 text-xs">Theoretical Period</p>
            <p className="text-xl font-semibold text-cyan-100">{result.stats.theoretical_period}</p>
          </div>

          <div className="space-y-2">
            <p className="text-sm text-blue-300/70">FSM Output (first 100 bits)</p>
            <code className="block bg-slate-900/50 p-4 rounded-md text-sm text-cyan-400 overflow-x-auto break-all font-mono">
              {result.fsm.slice(0, 100).join('')}
            </code>
          </div>

          <button
            onClick={exportCSV}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white font-semibold py-3 rounded-md transition-all shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50"
          >
            <Download size={18} />
            Export FSM as CSV
          </button>
        </div>
      )}
    </div>
  )
}
