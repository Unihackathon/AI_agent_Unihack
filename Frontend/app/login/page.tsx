"use client"

import type React from "react"
import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useToast } from "@/app/components/ui/use-toast"
import { FcGoogle } from "react-icons/fc"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      setIsLoading(false)
      toast({
        title: "Login successful",
        description: "Welcome back to AI Stock Trading Agent",
      })
      router.push("/dashboard")
    }, 1500)
  }

  const handleGoogleLogin = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
      toast({
        title: "Google login successful",
        description: "Welcome back to AI Stock Trading Agent",
      })
      router.push("/dashboard")
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

        <button onClick={handleGoogleLogin} disabled={isLoading} className="google-button">
          <FcGoogle className="h-5 w-5" />
          <span>Sign in with Google</span>
        </button>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-[#333]" />
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-black px-4 text-[#666] uppercase tracking-wider">Or continue with email</span>
          </div>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
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
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="text-sm tech-text pl-4">
                Password
              </label>
              <Link href="/forgot-password" className="text-xs link-text">
                Forgot password?
              </Link>
            </div>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input-field w-full"
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" disabled={isLoading} className="neon-button mt-8">
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="text-center text-white text-sm mt-8">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="link-text">
            sign up
          </Link>{" "}
          here
        </p>
      </div>
    </div>
  )
}

