export default function Header() {
  return (
    <header className="border-b border-purple-500/20 bg-purple-950/30 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
          FSM Key Generator
        </h1>
        <p className="text-purple-200/70 mt-2 text-lg">
          Three LFSR-based Alternating-Step keystream generator
        </p>
      </div>
    </header>
  )
}
