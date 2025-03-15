'use client'
import { useState, useEffect } from "react"
import Link from "next/link"

export default function Home() {
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-black text-white">
      <div className="text-center space-y-6 mb-12">
        <h1 className="text-[#00FF00] text-5xl md:text-6xl font-bold">
          AI Stock Trading
          <br />
          Agent
        </h1>
        <p className="text-lg md:text-xl max-w-2xl">
          Advanced AI-powered predictions for smarter trading decisions
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
        <Link href="/login" className="w-full">
          <button className="w-full py-4 px-6 bg-[#00FF00] text-black rounded-full hover:bg-[#00FF00]/90 transition-all duration-200 font-bold">
            Login
          </button>
        </Link>
        <Link href="/register" className="w-full">
          <button className="w-full py-4 px-6 bg-transparent border border-[#00FF00] text-[#00FF00] rounded-full hover:bg-[#00FF00]/10 transition-all duration-200 font-bold">
            Register
          </button>
        </Link>
      </div>

      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl">
        <FeatureCard title="Live Market Data" description="Real-time data from Binance and CoinGecko APIs" />
        <FeatureCard title="AI Predictions" description="LSTM and Transformer models for accurate forecasting" />
        <FeatureCard title="Custom Strategies" description="Create and backtest your own trading strategies" />
      </div>
    </div>
  )
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 border border-[#333] rounded-2xl hover:border-[#00FF00] transition-all duration-200">
      <h3 className="text-xl text-[#00FF00] mb-3 font-semibold">{title}</h3>
      <p>{description}</p>
    </div>
  )
}