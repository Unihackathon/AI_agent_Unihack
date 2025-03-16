"use client"

import { useEffect, useState } from "react"
import axios from "axios"
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card"

type MarketItem = {
  id: string
  name: string
  symbol: string
  current_price: number
  market_cap: number
  total_volume: number
  price_change_percentage_24h: number
  image: string
}

export default function Market() {
  const [market, setMarket] = useState<MarketItem[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchMarket = async () => {
      setIsLoading(true)
      try {
        const response = await axios.get("https://api.coingecko.com/api/v3/coins/markets", {
          params: {
            vs_currency: "usd",
            order: "market_cap_desc",
            per_page: 10,
            page: 1,
            sparkline: false,
          },
        })
        setMarket(response.data)
      } catch (error) {
        console.error("Error fetching market data:", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchMarket()
  }, [])

  return (
    <Card className="bg-black border border-[#00FF00]/30">
      <CardHeader>
        <CardTitle className="text-white">Market Data</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="text-white">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {market.map((item) => (
              <div key={item.id} className="p-4 bg-[#1a1a1a] rounded-lg border border-[#00FF00]/30">
                <div className="flex items-center space-x-4">
                  <img src={item.image} alt={item.name} className="w-10 h-10" />
                  <div>
                    <h3 className="text-lg font-bold text-white">{item.name}</h3>
                    <p className="text-sm text-gray-400">{item.symbol.toUpperCase()}</p>
                  </div>
                </div>
                <div className="mt-4">
                  <p className="text-white">Price: ${item.current_price.toLocaleString()}</p>
                  <p className="text-white">Market Cap: ${item.market_cap.toLocaleString()}</p>
                  <p className="text-white">Volume: ${item.total_volume.toLocaleString()}</p>
                  <p className={`text-white ${item.price_change_percentage_24h >= 0 ? "text-green-500" : "text-red-500"}`}>
                    24h Change: {item.price_change_percentage_24h.toFixed(2)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}