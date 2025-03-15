"use client"

import { useState } from "react"
import { Button } from "@/app/components/ui/button"
import { Input } from "@/app/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card"

enum ConversationState {
  INITIAL,
  WAITING_FOR_NAME_EMAIL,
  WAITING_FOR_QUERY,
  WAITING_FOR_BITCOIN_PRICE,
}

export function Chatbot() {
  const [messages, setMessages] = useState<{ user: string; bot: string }[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [conversationState, setConversationState] = useState<ConversationState>(ConversationState.INITIAL)

  const handleSend = async () => {
    if (input.trim() === "") return

    const userMessage = input
    setMessages((prev) => [...prev, { user: userMessage, bot: "..." }])
    setInput("")
    setLoading(true)

    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: userMessage,
          symbol: "TSLA", // Change as needed
          period: "6mo",   // Change as needed
        }),
      })

      if (!res.ok) throw new Error(`Failed to fetch response: ${res.statusText}`)

      const data = await res.json()
      console.log("API Response:", data)

      const botReply = data.response || "Sorry, I couldn't understand that."

      setMessages((prev) =>
        prev.map((msg, index) =>
          index === prev.length - 1 ? { ...msg, bot: botReply } : msg
        )
      )
    } catch (error) {
      console.error("Error fetching response:", error)
      setMessages((prev) =>
        prev.map((msg, index) =>
          index === prev.length - 1 ? { ...msg, bot: "Error fetching response." } : msg
        )
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="fixed bottom-4 right-4 w-80 bg-black border border-[#00FF00]/30">
      <CardHeader>
        <CardTitle className="text-[#00FF00]">AI Chatbot</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col space-y-4">
        <div className="flex-1 overflow-y-auto max-h-64 space-y-2">
          {messages.map((msg, index) => (
            <div key={index} className="space-y-1">
              <div className="text-white">User: {msg.user}</div>
              <div className="text-[#00FF00]">Bot: {msg.bot}</div>
            </div>
          ))}
        </div>
        <div className="flex space-x-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 bg-black border-[#00FF00]/30 text-white"
          />
          <Button onClick={handleSend} className="bg-[#00FF00] text-black" disabled={loading}>
            {loading ? "Sending..." : "Send"}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}