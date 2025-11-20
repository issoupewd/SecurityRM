import Link from 'next/link'

export default function DecryptionPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-950 via-purple-950/40 to-slate-950 px-4">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold text-gray-400">
          Message Decryption
        </h1>
        <p className="text-lg text-gray-500">
          Coming soon
        </p>
        <Link href="/" className="inline-block text-purple-400 hover:text-purple-300 transition-colors">
          ← Back to Home
        </Link>
      </div>
    </main>
  )
}
