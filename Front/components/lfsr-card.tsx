'use client'

import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

interface LFSRCardProps {
  title: string
  labels: string[]
  defaultState: number[]
  defaultTaps: number[]
  onGenerate: (state: any) => void
}

export default function LFSRCard({
  title,
  labels,
  defaultState,
  defaultTaps,
  onGenerate,
}: LFSRCardProps) {
  const [state, setState] = useState<number[]>(defaultState)
  const [taps, setTaps] = useState<Set<number>>(new Set(defaultTaps))
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [copied, setCopied] = useState(false)
  const [showStateTable, setShowStateTable] = useState(false)
  const [visibleRows, setVisibleRows] = useState(10) // ← number of rows shown in table

  const toggleTap = (index: number) => {
    const newTaps = new Set(taps)
    if (newTaps.has(index)) {
      newTaps.delete(index)
    } else {
      newTaps.add(index)
    }
    setTaps(newTaps)
  }

  const toggleBit = (index: number) => {
    const newState = [...state]
    newState[index] = 1 - newState[index]
    setState(newState)
  }

  const generateLFSR = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:5000/generate_lfsr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          init_state: state,
          taps: Array.from(taps).sort((a, b) => a - b),
        }),
      })
      const data = await response.json()
      setResult(data)
      onGenerate(data)

      // reset visible rows when new result is generated
      setVisibleRows(10)
    } catch (error) {
      console.error('Error generating LFSR:', error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    const text = result.outputs.join('')
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="bg-purple-900/20 backdrop-blur-sm border border-purple-500/30 rounded-lg p-6 space-y-6 hover:border-purple-400/50 transition-colors">
      <h2 className="text-xl font-semibold text-purple-100">{title}</h2>

      {/* Tap Position Buttons */}
      <div className="space-y-2">
        <p className="text-sm text-purple-300/70">Tap Positions</p>
        <div className="flex flex-wrap gap-2">
          {labels.map((label, i) => (
            <button
              key={i}
              onClick={() => toggleTap(i)}
              className={`px-3 py-2 rounded-md text-sm font-medium transition-all ${
                taps.has(i)
                  ? 'bg-purple-500 text-white shadow-lg shadow-purple-500/50'
                  : 'bg-purple-800/30 text-purple-300 hover:bg-purple-800/50'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Initial State Toggles */}
      <div className="space-y-2">
        <p className="text-sm text-purple-300/70">Initial State</p>
        <div className="flex gap-2">
          {state.map((bit, i) => (
            <button
              key={i}
              onClick={() => toggleBit(i)}
              className={`w-10 h-10 rounded-md font-semibold transition-all ${
                bit === 1
                  ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                  : 'bg-slate-700/30 text-slate-400 hover:bg-slate-700/50'
              }`}
            >
              {bit}
            </button>
          ))}
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={generateLFSR}
        disabled={loading}
        className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:opacity-50 text-white font-semibold py-3 rounded-md transition-all shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50"
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {result && (
        <div className="space-y-4 border-t border-purple-500/20 pt-4">
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="bg-purple-800/20 p-3 rounded-md">
              <p className="text-purple-300/70 text-xs">Practical Period</p>
              <p className="text-lg font-semibold text-purple-100">{result.period}</p>
            </div>
            <div className="bg-blue-800/20 p-3 rounded-md">
              <p className="text-blue-300/70 text-xs">Theoretical Period</p>
              <p className="text-lg font-semibold text-blue-100">{result.theoretical_period}</p>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <p className="text-sm text-purple-300/70">Output Sequence (first 50 bits)</p>
              <button
                onClick={copyToClipboard}
                className="text-purple-400 hover:text-purple-300 transition-colors"
              >
                {copied ? <Check size={16} /> : <Copy size={16} />}
              </button>
            </div>
            <code className="block bg-slate-900/50 p-3 rounded-md text-xs text-cyan-400 overflow-x-auto break-all font-mono">
              {result.outputs.slice(0, 50).join('')}
            </code>
          </div>

          <button
            onClick={() => setShowStateTable(!showStateTable)}
            className="text-sm text-purple-400 hover:text-purple-300 transition-colors"
          >
            {showStateTable ? 'Hide' : 'Show'} State Table
          </button>

          {showStateTable && (
            <div className="bg-slate-900/30 rounded-md overflow-x-auto">
              <table className="w-full text-xs text-purple-200">
                <thead className="bg-purple-900/50 border-b border-purple-500/20">
                  <tr>
                    <th className="px-3 py-2 text-left">Step</th>
                    <th className="px-3 py-2 text-left">State</th>
                    <th className="px-3 py-2 text-left">Output</th>
                  </tr>
                </thead>
                <tbody>
                  {result.states.slice(0, visibleRows).map((s: number[], i: number) => (
                    <tr
                      key={i}
                      className="border-b border-purple-500/10 hover:bg-purple-900/20"
                    >
                      <td className="px-3 py-2">{i}</td>
                      <td className="px-3 py-2 font-mono">[{s.join(', ')}]</td>
                      <td className="px-3 py-2 text-cyan-400">{result.outputs[i]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Load 10 more button */}
              {visibleRows < result.states.length && (
                <button
                  onClick={() => setVisibleRows(prev => prev + 10)}
                  className="mt-3 mb-2 text-sm text-blue-400 hover:text-blue-300 transition-colors"
                >
                  Load 10 more
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
