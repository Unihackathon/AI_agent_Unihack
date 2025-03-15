"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/app/components/ui/button"
import { Input } from "@/app/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/app/components/ui/select"
import { useToast } from "@/app/components/ui/use-toast"

export default function CompleteRegistrationPage() {
  const [firstName, setFirstName] = useState("")
  const [secondName, setSecondName] = useState("")
  const [lastName, setLastName] = useState("")
  const [day, setDay] = useState("")
  const [month, setMonth] = useState("")
  const [year, setYear] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const router = useRouter()
  const { toast } = useToast()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      setIsLoading(false)
      toast({
        title: "Registration complete",
        description: "Your account has been successfully created.",
      })
      router.push("/dashboard")
    }, 1500)
  }

  // Generate days, months, and years for the date of birth selectors
  const days = Array.from({ length: 31 }, (_, i) => i + 1)
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 100 }, (_, i) => currentYear - i)

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-black">
      <div className="w-full max-w-md space-y-8 p-8 rounded-lg">
        <div className="text-center">
          <h1 className="neon-text text-4xl mb-6">
            AI Stock Trading
            <br />
            Agent
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div>
              <label htmlFor="firstName" className="text-sm font-medium text-[#00FF00]">
                First Name
              </label>
              <Input
                id="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                className="h-12 bg-input border-primary/30 text-primary mt-1"
              />
            </div>

            <div>
              <label htmlFor="secondName" className="text-sm font-medium text-[#00FF00]">
                Second Name
              </label>
              <Input
                id="secondName"
                value={secondName}
                onChange={(e) => setSecondName(e.target.value)}
                className="h-12 bg-input border-primary/30 text-primary mt-1"
              />
            </div>

            <div>
              <label htmlFor="lastName" className="text-sm font-medium text-[#00FF00]">
                Last Name
              </label>
              <Input
                id="lastName"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
                className="h-12 bg-input border-primary/30 text-primary mt-1"
              />
            </div>

            <div>
              <label className="text-sm font-medium block mb-1 text-[#00FF00]">Date of Birth</label>
              <div className="grid grid-cols-3 gap-2">
                <Select value={day} onValueChange={setDay}>
                  <SelectTrigger className="bg-input border-primary/30 text-primary">
                    <SelectValue placeholder="Day" />
                  </SelectTrigger>
                  <SelectContent className="bg-black border-primary text-primary">
                    {days.map((d) => (
                      <SelectItem
                        key={d}
                        value={d.toString()}
                        className="text-primary focus:bg-primary/20 focus:text-primary"
                      >
                        {d}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select value={month} onValueChange={setMonth}>
                  <SelectTrigger className="bg-input border-primary/30 text-primary">
                    <SelectValue placeholder="Month" />
                  </SelectTrigger>
                  <SelectContent className="bg-black border-primary text-primary">
                    {months.map((m, i) => (
                      <SelectItem
                        key={m}
                        value={(i + 1).toString()}
                        className="text-primary focus:bg-primary/20 focus:text-primary"
                      >
                        {m}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select value={year} onValueChange={setYear}>
                  <SelectTrigger className="bg-input border-primary/30 text-primary">
                    <SelectValue placeholder="Year" />
                  </SelectTrigger>
                  <SelectContent className="bg-black border-primary text-primary">
                    {years.map((y) => (
                      <SelectItem
                        key={y}
                        value={y.toString()}
                        className="text-primary focus:bg-primary/20 focus:text-primary"
                      >
                        {y}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <label htmlFor="email" className="text-sm font-medium text-[#00FF00]">
                Email Address
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="h-12 bg-input border-primary/30 text-primary mt-1"
              />
            </div>

            <div>
              <label htmlFor="phone" className="text-sm font-medium text-[#00FF00]">
                Phone Number
              </label>
              <Input
                id="phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="h-12 bg-input border-primary/30 text-primary mt-1"
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full py-6 font-bold text-black bg-[#00FF00] hover:bg-[#00FF00]/90 neon-button"
            disabled={isLoading}
          >
            {isLoading ? "Finishing..." : "Finish"}
          </Button>
        </form>
      </div>
    </div>
  )
}

