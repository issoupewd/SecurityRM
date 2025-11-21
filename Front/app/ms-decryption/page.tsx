"use client"

import { useState } from "react"
import Link from "next/link"
import { Copy, Check, Download } from "lucide-react"

interface PerKeyResult {
  key_index: number
  key: number[]
  decoded_text: string
  score: number
}

interface DecryptionResponse {
  per_key: PerKeyResult[]
  best: {
    key_index: number
    decoded_text: string
    score: number
  }
}

// Default cipher bits from backend
const DEFAULT_CIPHER_BITS = [
  1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1,
  1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
]

export default function MSDecryptionPage() {
  const [cipherText, setCipherText] = useState<string>(DEFAULT_CIPHER_BITS.join(""))
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<DecryptionResponse | null>(null)
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const runDecryption = async () => {
    setLoading(true)
    try {
      // Convert cipher text to array of bits
      const cipherBits = cipherText
        .split("")
        .map((c) => Number.parseInt(c) || 0)
        .filter((b) => b === 0 || b === 1)

      const response = await fetch("http://127.0.0.1:5000/ms_decryption", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cipher_bits: cipherBits,
        }),
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("Error running decryption:", error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const exportCSV = () => {
    if (!result) return

    let csv = "key_index,key,decoded_text,score\n"
    result.per_key.forEach((row) => {
      const keyStr = row.key.join("")
      csv += `${row.key_index},"${keyStr}","${row.decoded_text}",${row.score}\n`
    })

    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "ms_decryption_results.csv"
    a.click()
  }

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
            Message Decryption
          </h1>
          <p className="text-gray-400">
            Decrypt messages using multiple keys and find the best result based on dictionary scoring.
          </p>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8 space-y-8">
        {/* Cipher input */}
        <div className="bg-purple-900/20 backdrop-blur-sm border border-purple-500/30 rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold text-purple-100">Cipher Text (binary)</h2>
          <p className="text-sm text-purple-300/70">
            Enter or paste the ciphertext as a binary string (0s and 1s). Example shown below uses the default backend
            cipher.
          </p>
          <textarea
            value={cipherText}
            onChange={(e) => setCipherText(e.target.value)}
            className="w-full h-32 bg-slate-800/50 border border-purple-500/30 rounded-md px-4 py-3 text-purple-100 placeholder-slate-500 focus:outline-none focus:border-purple-400/50 font-mono text-xs"
            placeholder="Enter binary cipher text (0s and 1s only)"
          />
          <div className="text-xs text-purple-300/50">
            Bits: {cipherText.split("").filter((c) => c === "0" || c === "1").length}
          </div>
        </div>

        {/* Run button */}
        <button
          onClick={runDecryption}
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:opacity-50 text-white font-semibold py-3 rounded-md transition-all shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50"
        >
          {loading ? "Decrypting..." : "Run Decryption"}
        </button>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Best result highlight */}
            <div className="bg-gradient-to-r from-green-900/30 to-emerald-900/30 border-2 border-green-500/50 rounded-lg p-6 space-y-3">
              <h3 className="text-lg font-semibold text-green-100">Best Result (Key #{result.best.key_index})</h3>
              <p className="text-2xl font-bold text-green-200 break-all text-balance">{result.best.decoded_text}</p>
              <p className="text-sm text-green-300/70">
                Dictionary Match Score: <span className="font-bold text-green-200">{result.best.score}</span>
              </p>
            </div>

            {/* Per-key results table */}
            <div className="bg-purple-900/20 backdrop-blur-sm border border-purple-500/30 rounded-lg p-6 space-y-4 overflow-x-auto">
              <h3 className="text-lg font-semibold text-purple-100">All Decryption Results</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-purple-200">
                  <thead className="bg-purple-900/50 border-b border-purple-500/20">
                    <tr>
                      <th className="px-4 py-2 text-left">Key #</th>
                      <th className="px-4 py-2 text-left">Key (bits)</th>
                      <th className="px-4 py-2 text-left">Decoded Text</th>
                      <th className="px-4 py-2 text-left">Score</th>
                      <th className="px-4 py-2 text-center">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.per_key.map((row, idx) => (
                      <tr
                        key={idx}
                        className={`border-b border-purple-500/10 hover:bg-purple-900/30 transition-colors ${
                          row.key_index === result.best.key_index ? "bg-green-900/20" : ""
                        }`}
                      >
                        <td className="px-4 py-2 font-semibold text-purple-100">{row.key_index}</td>
                        <td className="px-4 py-2 font-mono text-xs text-cyan-400 truncate">{row.key.join("")}</td>
                        <td className="px-4 py-2 font-semibold text-purple-100 break-all max-w-xs">
                          {row.decoded_text}
                        </td>
                        <td className="px-4 py-2 font-bold text-purple-300">{row.score}</td>
                        <td className="px-4 py-2 text-center">
                          <button
                            onClick={() => copyToClipboard(row.decoded_text, row.key_index)}
                            className="text-purple-400 hover:text-purple-300 transition-colors inline-flex"
                          >
                            {copiedIndex === row.key_index ? <Check size={16} /> : <Copy size={16} />}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Export button */}
              <button
                onClick={exportCSV}
                className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white font-semibold py-2 rounded-md transition-all shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 mt-4"
              >
                <Download size={18} />
                Export Results as CSV
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-purple-500/20 bg-purple-950/30 backdrop-blur-sm mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-sm text-gray-400">
          Message decryption using multiple keys with dictionary-based scoring for educational security applications.
        </div>
      </div>
    </main>
  )
}
