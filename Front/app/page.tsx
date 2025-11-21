import Link from "next/link"

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-950 via-purple-950/40 to-slate-950 px-4">
      {/* Gradient overlay */}
      <div className="fixed inset-0 -z-10 bg-gradient-to-br from-purple-500/10 via-transparent to-blue-500/10"></div>

      <div className="text-center space-y-6 max-w-3xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-purple-300 to-blue-400">
          Security Application
        </h1>

        <p className="text-lg text-gray-300 leading-relaxed">
          Exercises and applications in cryptography: LFSRs, FSM-based keystreams, encryption/decryption tools.
        </p>

        {/* Navigation buttons grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
          {/* Message Decryption */}
          <Link href="/ms-decryption">
            <div className="group relative h-48 bg-gradient-to-br from-purple-600/40 to-purple-800/40 rounded-xl border border-purple-500/50 p-6 hover:border-purple-400/80 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/50 cursor-pointer">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 to-blue-500/0 group-hover:from-purple-500/10 group-hover:to-blue-500/10 rounded-xl transition-all duration-300"></div>
              <div className="relative z-10 h-full flex flex-col justify-between">
                <h2 className="text-2xl font-bold text-purple-200 group-hover:text-purple-100 transition-colors">
                  Message Decryption
                </h2>
                <p className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors text-left">
                  Decrypt messages using multiple keys and find the best result
                </p>
              </div>
              <div className="absolute inset-0 rounded-xl border border-purple-400/0 group-hover:border-purple-400/50 transition-all duration-300"></div>
            </div>
          </Link>

          {/* FSM Key Generator (2 LFSR) */}
          <Link href="/fsm-2lfsr">
            <div className="group relative h-48 bg-gradient-to-br from-purple-600/40 to-purple-800/40 rounded-xl border border-purple-500/50 p-6 hover:border-purple-400/80 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/50 cursor-pointer">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 to-blue-500/0 group-hover:from-purple-500/10 group-hover:to-blue-500/10 rounded-xl transition-all duration-300"></div>
              <div className="relative z-10 h-full flex flex-col justify-between">
                <h2 className="text-2xl font-bold text-purple-200 group-hover:text-purple-100 transition-colors">
                  FSM Key Generator (2 LFSR)
                </h2>
                <p className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors text-left">
                  Generate keystreams using 2 LFSRs with FSM combination
                </p>
              </div>
              <div className="absolute inset-0 rounded-xl border border-purple-400/0 group-hover:border-purple-400/50 transition-all duration-300"></div>
            </div>
          </Link>

          {/* FSM Key Generator (3 LFSR) */}
          <Link href="/fsm">
            <div className="group relative h-48 bg-gradient-to-br from-blue-600/40 to-blue-800/40 rounded-xl border border-blue-500/50 p-6 hover:border-blue-400/80 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/50 cursor-pointer">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 to-cyan-500/0 group-hover:from-blue-500/10 group-hover:to-cyan-500/10 rounded-xl transition-all duration-300"></div>
              <div className="relative z-10 h-full flex flex-col justify-between">
                <h2 className="text-2xl font-bold text-blue-200 group-hover:text-blue-100 transition-colors">
                  FSM Key Generator (3 LFSR)
                </h2>
                <p className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors text-left">
                  Generate keystreams using 3 LFSRs and an alternating-step FSM
                </p>
              </div>
              <div className="absolute inset-0 rounded-xl border border-blue-400/0 group-hover:border-blue-400/50 transition-all duration-300"></div>
            </div>
          </Link>

          {/* TBD */}
          <div className="group relative h-48 bg-gradient-to-br from-gray-600/20 to-gray-800/20 rounded-xl border border-gray-500/30 p-6 opacity-60">
            <div className="relative z-10 h-full flex flex-col justify-between">
              <h2 className="text-2xl font-bold text-gray-400">TBD</h2>
              <p className="text-sm text-gray-500 text-left">To be determined</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
