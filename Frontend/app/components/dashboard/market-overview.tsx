"use client"

import { useEffect, useState } from "react"
import axios from "axios"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

export function MarketOverview() {
  const [cryptoData, setCryptoData] = useState([])

  useEffect(() => {
    const fetchCryptoData = async () => {
      try {
        const response = await axios.get("https://api.coincap.io/v2/assets", {
          params: {
            limit: 10,
          },
        })
        console.log("API Response:", response.data)
        const data = response.data.data.map((coin: any) => ({
          name: coin.name,
          price: parseFloat(coin.priceUsd),
        }))
        console.log("Formatted Data:", data)
        setCryptoData(data)
      } catch (error) {
        console.error("Error fetching crypto data:", error)
        
      }
    }

    fetchCryptoData()
  }, [])

  useEffect(() => {
    console.log("Crypto Data State:", cryptoData)
  }, [cryptoData])

  return (
    <Card className="bg-black border border-border">
      <CardHeader>
        <CardTitle className="text-white">Market Overview</CardTitle>
        <CardDescription className="text-white">Live market data from major exchanges</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="crypto">
          <TabsList className="mb-4 bg-muted">
            <TabsTrigger
              value="crypto"
              className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground text-white"
            >
              Crypto
            </TabsTrigger>
            <TabsTrigger
              value="stocks"
              className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground text-white"
            >
              Stocks
            </TabsTrigger>
            <TabsTrigger
              value="forex"
              className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground text-white"
            >
              Forex
            </TabsTrigger>
          </TabsList>
          <TabsContent value="crypto">
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={cryptoData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="name" stroke="#888" />
                  <YAxis stroke="#888" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#000",
                      border: "1px solid #333",
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#f7931a"
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
          <TabsContent value="stocks">
            <div className="flex items-center justify-center h-[400px]">
              <p className="text-white">Stock market data coming soon</p>
            </div>
          </TabsContent>
          <TabsContent value="forex">
            <div className="flex items-center justify-center h-[400px]">
              <p className="text-white">Forex market data coming soon</p>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}