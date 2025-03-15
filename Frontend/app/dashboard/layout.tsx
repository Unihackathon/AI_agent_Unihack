import type React from "react"
import { SidebarProvider } from "@/app/components/ui/sidebar"
import { DashboardSidebar } from "@/app/components/dashboard/sidebar"
import { UserNav } from "@/app/components/dashboard/user-nav"
import { Chatbot } from "@/app/components/chatbot/page.tsx"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarProvider>
      <div className="flex h-screen w-screen overflow-hidden bg-black">
        <DashboardSidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <header className="border-b border-[#00FF00]/30 bg-black h-16 flex items-center px-6 justify-between">
            <h1 className="text-xl font-bold text-[#00FF00]">Dashboard</h1>
            <UserNav />
          </header>
          <main className="flex-1 overflow-auto p-6 relative">
            {children}
            <Chatbot />
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}