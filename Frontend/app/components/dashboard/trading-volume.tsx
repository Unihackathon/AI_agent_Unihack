"use client"

import { useEffect, useState } from "react"
import axios from "axios"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

export function TradingVolume() {
  const [volumeData, setVolumeData] = useState([])

  useEffect(() => {
    const fetchVolumeData = async () => {
      try {
        const response = await axios.get("https://api.coingecko.com/api/v3/coins/markets", {
          params: {
            vs_currency: 'usd',
            order: 'market_cap_desc',
            per_page: 10,
            page: 1,
            sparkline: false,
          },
        })
        console.log("API Response:", response.data)
        const data = response.data.map((coin: any) => ({
          name: coin.name,
          volume: coin.total_volume,
        }))
        console.log("Formatted Data:", data)
        setVolumeData(data)
      } catch (error) {
        console.error("Error fetching volume data:", error)
        
    }
    }

    fetchVolumeData()
  }, [])

  return (
    <Card className="bg-black border border-[#00FF00]/30">
      <CardHeader>
        <CardTitle className="text-white">Trading Volume</CardTitle>
        <CardDescription className="text-[#00FF00]/70">Top 10 cryptocurrencies by trading volume</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={volumeData} barSize={20}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="name" stroke="#AAA" />
              <YAxis stroke="#AAA" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#111",
                  border: "1px solid #444",
                }}
                formatter={(value) => [`$${value.toLocaleString()}`, "Volume"]}
              />
              <Legend />
              <Bar dataKey="volume" name="Trading Volume" fill="url(#colorVolume)" radius={[8, 8, 8, 8]} />
              <defs>
                <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#FFD700" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#FFD700" stopOpacity={0} />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}