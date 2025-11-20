export default function Footer() {
  return (
    <footer className="border-t border-purple-500/20 bg-purple-950/30 backdrop-blur-md mt-12">
      <div className="max-w-6xl mx-auto px-4 py-6 text-center">
        <p className="text-purple-200/60 text-sm">
          FSM keystream generator based on three LFSRs (two controlled by one).
        </p>
      </div>
    </footer>
  )
}
