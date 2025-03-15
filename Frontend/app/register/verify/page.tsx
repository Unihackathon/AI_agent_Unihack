"use client"

import { useState, useEffect } from "react"
import { useToast } from "@/app/components/ui/use-toast"

export default function VerifyPage() {
  const [timeLeft, setTimeLeft] = useState(45)
  const [isResending, setIsResending] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    if (timeLeft <= 0) return
    const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000)
    return () => clearTimeout(timer)
  }, [timeLeft])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  const handleResendLink = () => {
    setIsResending(true)
    setTimeout(() => {
      setIsResending(false)
      setTimeLeft(45)
      toast({
        title: "Verification link sent",
        description: "A new verification link has been sent to your email.",
      })
    }, 1500)
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-black">
      <div className="w-full max-w-md text-center space-y-8">
        <h1 className="neon-text text-4xl">
          AI Stock Trading
          <br />
          Agent
        </h1>

        <div className="border border-[#333] rounded-2xl p-8 space-y-6 bg-black/50">
          <h2 className="text-2xl tech-text">Verify your email</h2>

          <p className="tech-text text-sm">
            We&apos;ve sent a verification link to your
            <br />
            email [user@example.com]
          </p>

          <div>
            <p className="text-sm tech-text">Link expires in</p>
            <p className="text-2xl tech-text">{formatTime(timeLeft)}</p>
          </div>

          <p className="text-sm tech-text">Didn&apos;t receive the email?</p>

          <button onClick={handleResendLink} disabled={isResending || timeLeft > 0} className="neon-button">
            {isResending ? "Sending..." : "Resend Link"}
          </button>
        </div>
      </div>
    </div>
  )
}

