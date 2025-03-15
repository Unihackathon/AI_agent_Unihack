"use client"

import type React from "react"
import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useToast } from "@/app/components/ui/use-toast"
import { FcGoogle } from "react-icons/fc"

export default function RegisterPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [agreedToTerms, setAgreedToTerms] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()

    if (password !== confirmPassword) {
      toast({
        variant: "destructive",
        title: "Passwords don't match",
        description: "Please make sure your passwords match.",
      })
      return
    }

    if (!agreedToTerms) {
      toast({
        variant: "destructive",
        title: "Terms and conditions",
        description: "You must agree to the terms and conditions to register.",
      })
      return
    }

    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
      router.push("/register/verify")
    }, 1500)
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-black">
      <div className="w-full max-w-md space-y-8 p-8">
        <div className="text-center space-y-6">
          <h1 className="neon-text text-4xl">
            AI Stock Trading
            <br />
            Agent
          </h1>
        </div>

        <button onClick={() => {}} disabled={isLoading} className="google-button">
          <FcGoogle className="h-5 w-5" />
          <span>Sign in with Google</span>
        </button>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-[#333]" />
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-black px-4 text-[#666] uppercase tracking-wider">Or register with email</span>
          </div>
        </div>

        <form onSubmit={handleRegister} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm tech-text pl-4">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input-field w-full"
              placeholder="Enter your email"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm tech-text pl-4">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input-field w-full"
              placeholder="Create a password"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="confirm-password" className="text-sm tech-text pl-4">
              Confirm Password
            </label>
            <input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="input-field w-full"
              placeholder="Confirm your password"
            />
          </div>

          <div className="flex items-center space-x-2 px-4">
            <input
              type="checkbox"
              id="terms"
              checked={agreedToTerms}
              onChange={(e) => setAgreedToTerms(e.target.checked)}
              className="rounded border-[#333] text-[#00FF00] focus:ring-[#00FF00]"
            />
            <label htmlFor="terms" className="text-sm tech-text">
              I agree to the{" "}
              <Link href="/terms" className="link-text">
                terms and conditions
              </Link>
            </label>
          </div>

          <button type="submit" disabled={isLoading} className="neon-button mt-8">
            {isLoading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="text-center text-sm mt-8">
          Already have an account?{" "}
          <Link href="/login" className="link-text">
            login here
          </Link>
        </p>
      </div>
    </div>
  )
}

