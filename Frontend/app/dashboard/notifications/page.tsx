"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card"

type Notification = {
  id: number
  message: string
  timestamp: Date
}

const mockNotifications: Notification[] = [
  { id: 1, message: "Stock XYZ has increased by 5%", timestamp: new Date() },
  { id: 2, message: "Stock ABC has decreased by 3%", timestamp: new Date() },
]

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([])

  useEffect(() => {
    // Simulate fetching notifications from a server
    const fetchNotifications = () => {
      setNotifications(mockNotifications)
    }

    fetchNotifications()
  }, [])

  return (
    <Card className="bg-black border border-[#00FF00]/30">
      <CardHeader>
        <CardTitle className="text-[#00FF00]">Notifications</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col space-y-4">
        {notifications.map((notification) => (
          <div key={notification.id} className="text-white">
            <p>{notification.message}</p>
            <small className="text-gray-500">{notification.timestamp.toLocaleString()}</small>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}