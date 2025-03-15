"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LineChart, Settings, Bell, Home, PieChart, Wallet, Zap, History, BookOpen } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
} from "@/app/components/ui/sidebar"

export function DashboardSidebar() {
  const pathname = usePathname()

  return (
    <Sidebar>
      <SidebarHeader className="border-b border-[#00FF00]/30 p-4">
        <h2 className="text-white text-xl">AI Stock Trading</h2>
      </SidebarHeader>

      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard"}
              tooltip="Dashboard"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard">
                <Home className="mr-2" />
                <span>Dashboard</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/market"}
              tooltip="Market Data"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/market">
                <LineChart className="mr-2" />
                <span>Market Data</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/predictions"}
              tooltip="AI Predictions"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/predictions">
                <Zap className="mr-2" />
                <span>AI Predictions</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/portfolio"}
              tooltip="Portfolio"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/portfolio">
                <PieChart className="mr-2" />
                <span>Portfolio</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/wallet"}
              tooltip="Wallet"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/wallet">
                <Wallet className="mr-2" />
                <span>Wallet</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/history"}
              tooltip="Trade History"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/history">
                <History className="mr-2" />
                <span>Trade History</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/news"}
              tooltip="Market News"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/news">
                <BookOpen className="mr-2" />
                <span>Market News</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>

      <SidebarFooter className="border-t border-[#00FF00]/30 p-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/notifications"}
              tooltip="Notifications"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/notifications">
                <Bell className="mr-2" />
                <span>Notifications</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={pathname === "/dashboard/settings"}
              tooltip="Settings"
              className="text-white hover:text-[#00FF00] hover:bg-[#00FF00]/10"
            >
              <Link href="/dashboard/settings">
                <Settings className="mr-2" />
                <span>Settings</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}