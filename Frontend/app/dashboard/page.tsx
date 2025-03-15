import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs"
import { MarketOverview } from "@/app/components/dashboard/market-overview"
import { PredictionChart } from "@/app/components/dashboard/prediction-chart"
import { RecentTrades } from "@/app/components/dashboard/recent-trades"
import { TradingVolume } from "@/app/components/dashboard/trading-volume"

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-black border border-[#00FF00]/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">Portfolio Value</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#00FF00]">$45,231.89</div>
            <p className="text-xs text-[#00FF00]/70">
              <span className="text-white">+20.1%</span> from last month
            </p>
          </CardContent>
        </Card>
        <Card className="bg-black border border-[#00FF00]/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">Active Positions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#00FF00]">12</div>
            <p className="text-xs text-[#00FF00]/70">
              <span className="text-white">+2</span> new positions today
            </p>
          </CardContent>
        </Card>
        <Card className="bg-black border border-[#00FF00]/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">AI Predictions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#00FF00]">7</div>
            <p className="text-xs text-[#00FF00]/70">
              <span className="text-white">+3</span> new signals today
            </p>
          </CardContent>
        </Card>
        <Card className="bg-black border border-[#00FF00]/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">Market Sentiment</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#00FF00]">Bullish</div>
            <p className="text-xs text-[#00FF00]/70">Based on 24h market analysis</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="bg-muted border border-[#00FF00]/30">
          <TabsTrigger
            value="overview"
            className="data-[state=active]:bg-[#00FF00] data-[state=active]:text-black text-white"
          >
            Market Overview
          </TabsTrigger>
          <TabsTrigger
            value="predictions"
            className="data-[state=active]:bg-[#00FF00] data-[state=active]:text-black text-white"
          >
            AI Predictions
          </TabsTrigger>
          <TabsTrigger
            value="trades"
            className="data-[state=active]:bg-[#00FF00] data-[state=active]:text-black text-white"
          >
            Recent Trades
          </TabsTrigger>
          <TabsTrigger
            value="volume"
            className="data-[state=active]:bg-[#00FF00] data-[state=active]:text-black text-white"
          >
            Trading Volume
          </TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <MarketOverview />
        </TabsContent>
        <TabsContent value="predictions" className="space-y-4">
          <PredictionChart />
        </TabsContent>
        <TabsContent value="trades" className="space-y-4">
          <RecentTrades />
        </TabsContent>
        <TabsContent value="volume" className="space-y-4">
          <TradingVolume />
        </TabsContent>
      </Tabs>
    </div>
  )
}