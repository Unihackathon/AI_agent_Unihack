"use client"

import { useEffect, useState } from "react"
import axios from "axios"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Badge } from "@/app/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/app/components/ui/table"

export function RecentTrades() {
  interface Trade {
    id: string;
    asset: string;
    type: string;
    amount: string;
    price: string;
    value: string;
    time: string;
    status: string;
  }

  const [trades, setTrades] = useState<Trade[]>([])

  useEffect(() => {
    const fetchTradesData = async () => {
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
        const data = response.data.map((coin: any, index: number) => ({
          id: `TR-${1234 - index}`,
          asset: `${coin.symbol.toUpperCase()}/USDT`,
          type: index % 2 === 0 ? "buy" : "sell",
          amount: `${(Math.random() * 10).toFixed(2)} ${coin.symbol.toUpperCase()}`,
          price: `$${coin.current_price.toLocaleString()}`,
          value: `$${(coin.current_price * (Math.random() * 10)).toFixed(2)}`,
          time: `${Math.floor(Math.random() * 60)} minutes ago`,
          status: "completed",
        }))
        console.log("Formatted Data:", data)
        setTrades(data)
      } catch (error) {
        console.error("Error fetching trades data:", error)
        
      }
    }

    fetchTradesData()
  }, [])

  return (
    <Card className="bg-black border border-border">
      <CardHeader>
        <CardTitle className="text-white">Recent Trades</CardTitle>
        <CardDescription className="text-white">Your most recent trading activity</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow className="border-border">
              <TableHead className="text-white">ID</TableHead>
              <TableHead className="text-white">Asset</TableHead>
              <TableHead className="text-white">Type</TableHead>
              <TableHead className="text-white">Amount</TableHead>
              <TableHead className="text-white">Price</TableHead>
              <TableHead className="text-white">Value</TableHead>
              <TableHead className="text-white">Time</TableHead>
              <TableHead className="text-white">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {trades.map((trade) => (
              <TableRow key={trade.id} className="border-border">
                <TableCell className="font-medium text-white">{trade.id}</TableCell>
                <TableCell className="text-white">{trade.asset}</TableCell>
                <TableCell>
                  <Badge
                    variant={trade.type === "buy" ? "default" : "secondary"}
                    className={trade.type === "buy" ? "bg-primary text-primary-foreground" : "text-white"}
                  >
                    {trade.type}
                  </Badge>
                </TableCell>
                <TableCell className="text-white">{trade.amount}</TableCell>
                <TableCell className="text-white">{trade.price}</TableCell>
                <TableCell className="text-white">{trade.value}</TableCell>
                <TableCell className="text-white">{trade.time}</TableCell>
                <TableCell>
                  <Badge variant="outline" className="bg-primary/10 text-primary border-primary">
                    {trade.status}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}