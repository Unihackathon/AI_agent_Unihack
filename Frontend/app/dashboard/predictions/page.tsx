"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/app/components/ui/select"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

const data = [
  { date: "2023-03-01", actual: 42000, predicted: 42100 },
  { date: "2023-03-02", actual: 43500, predicted: 43200 },
  { date: "2023-03-03", actual: 43200, predicted: 43800 },
  { date: "2023-03-04", actual: 44000, predicted: 44200 },
  { date: "2023-03-05", actual: 45000, predicted: 44800 },
  { date: "2023-03-06", actual: 44800, predicted: 45500 },
  { date: "2023-03-07", actual: 45500, predicted: 46000 },
  { date: "2023-03-08", actual: null, predicted: 46500 },
  { date: "2023-03-09", actual: null, predicted: 47000 },
  { date: "2023-03-10", actual: null, predicted: 47200 },
]

export default function PredictionsPage() {
  return (
    <div className="p-6">
      <Card className="bg-black border border-[#00FF00]/30">
        <CardHeader className="flex flex-row items-center">
          <div className="flex-1">
            <CardTitle className="text-white">AI Price Predictions</CardTitle>
            <CardDescription className="text-[#00FF00]/70">LSTM/Transformer model predictions</CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Select defaultValue="BTC">
              <SelectTrigger className="w-[120px] bg-black border-[#00FF00]/30 text-white">
                <SelectValue placeholder="Select Asset" />
              </SelectTrigger>
              <SelectContent className="bg-black border-[#00FF00]/30 text-white">
                <SelectItem value="BTC">Bitcoin</SelectItem>
                <SelectItem value="ETH">Ethereum</SelectItem>
                <SelectItem value="SOL">Solana</SelectItem>
                <SelectItem value="AAPL">Apple</SelectItem>
                <SelectItem value="MSFT">Microsoft</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="date" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#000",
                    border: "1px solid #333",
                  }}
                />
                <Legend />
                <defs>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorPredicted" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00ff00" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#00ff00" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="actual"
                  stroke="#8884d8"
                  fillOpacity={1}
                  fill="url(#colorActual)"
                  strokeWidth={2}
                />
                <Area
                  type="monotone"
                  dataKey="predicted"
                  stroke="#00ff00"
                  fillOpacity={1}
                  fill="url(#colorPredicted)"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-[#1a1a1a] p-3 border border-[#00FF00]/30">
              <div className="text-sm font-medium text-white">Confidence Level</div>
              <div className="text-2xl font-bold text-[#00FF00]">87%</div>
            </div>
            <div className="rounded-lg bg-[#1a1a1a] p-3 border border-[#00FF00]/30">
              <div className="text-sm font-medium text-white">Predicted Change (7d)</div>
              <div className="text-2xl font-bold text-[#00FF00]">+12.4%</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}