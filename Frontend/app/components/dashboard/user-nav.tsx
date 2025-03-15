"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/app/components/ui/avatar"
import { Button } from "@/app/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/app/components/ui/dropdown-menu"
import { useRouter } from "next/navigation"

export function UserNav() {
  const router = useRouter()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-10 w-10 rounded-full hover:bg-primary/10">
          <Avatar className="h-10 w-10">
            <AvatarImage src="/placeholder.svg?height=40&width=40" alt="User" />
            <AvatarFallback className="bg-muted text-primary">JD</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56 bg-black border-[#00FF00]/30 text-[#00FF00]" align="end" forceMount>
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">John Doe</p>
            <p className="text-xs leading-none text-[#00FF00]/70">john.doe@example.com</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator className="bg-[#00FF00]/30" />
        <DropdownMenuGroup>
          <DropdownMenuItem
            onClick={() => router.push("/dashboard/profile")}
            className="hover:bg-[#00FF00]/10 hover:text-[#00FF00] focus:bg-[#00FF00]/10 focus:text-[#00FF00]"
          >
            Profile
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => router.push("/dashboard/settings")}
            className="hover:bg-[#00FF00]/10 hover:text-[#00FF00] focus:bg-[#00FF00]/10 focus:text-[#00FF00]"
          >
            Settings
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => router.push("/dashboard/billing")}
            className="hover:bg-[#00FF00]/10 hover:text-[#00FF00] focus:bg-[#00FF00]/10 focus:text-[#00FF00]"
          >
            Billing
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator className="bg-[#00FF00]/30" />
        <DropdownMenuItem
          onClick={() => router.push("/login")}
          className="hover:bg-[#00FF00]/10 hover:text-[#00FF00] focus:bg-[#00FF00]/10 focus:text-[#00FF00]"
        >
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}