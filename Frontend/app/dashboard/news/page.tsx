"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import { Search, Calendar, Clock, ExternalLink } from "lucide-react"
import Image from "next/image"

// News categories
const CATEGORIES = [
  { id: "all", name: "All News" },
  { id: "stocks", name: "Stocks" },
  { id: "crypto", name: "Cryptocurrency" },
  { id: "forex", name: "Forex" },
  { id: "commodities", name: "Commodities" },
  { id: "economy", name: "Economy" },
]

export default function NewsPage() {
  const [activeCategory, setActiveCategory] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [newsData, setNewsData] = useState<NewsItem[]>([])

  // Fetch news data from NewsAPI
  useEffect(() => {
    const fetchNews = async () => {
      setIsLoading(true)
      try {
        const response = await axios.get("https://newsapi.org/v2/everything", {
          params: {
            q: "market",
            apiKey: "60d06596928d4201bbd6b51fec4f5b3b", // Replace with your NewsAPI key
          },
        })

        // Assign categories to each article
        const categorizedNews = response.data.articles.map((article: NewsItem) => ({
          ...article,
          category: assignCategory(article),
        }))

        setNewsData(categorizedNews)
      } catch (error) {
        console.error("Error fetching news data:", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchNews()
  }, [])

  // Function to assign categories based on keywords
  const assignCategory = (news: NewsItem): string => {
    const title = news.title.toLowerCase()
    if (title.includes("stock")) return "stocks"
    if (title.includes("crypto") || title.includes("bitcoin") || title.includes("ethereum")) return "crypto"
    if (title.includes("forex") || title.includes("currency")) return "forex"
    if (title.includes("oil") || title.includes("gold") || title.includes("commodity")) return "commodities"
    if (title.includes("economy") || title.includes("inflation") || title.includes("gdp")) return "economy"
    return "all" // Default to "all" if no match is found
  }

  // Filter news based on category and search query
  const filteredNews = newsData.filter((item) => {
    const matchesCategory = activeCategory === "all" || item.category === activeCategory
    const matchesSearchQuery =
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase())

    return matchesCategory && matchesSearchQuery
  })

  // Format date to readable string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  // Format time to readable string
  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Market News</h1>
          <p className="text-gray-400">Stay updated with the latest market developments</p>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search news..."
            className="input-field pl-10 w-full"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Categories */}
      <div className="flex overflow-x-auto pb-2 space-x-2 no-scrollbar">
        {CATEGORIES.map((category) => (
          <button
            key={category.id}
            className={`px-4 py-2 rounded-full whitespace-nowrap ${
              activeCategory === category.id ? "bg-blue-500 text-white" : "bg-gray-800 text-gray-300 hover:bg-gray-700"
            }`}
            onClick={() => setActiveCategory(category.id)}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* News Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-40 bg-gray-800 rounded-t-lg"></div>
              <div className="p-4 space-y-3">
                <div className="h-4 bg-gray-800 rounded w-3/4"></div>
                <div className="h-4 bg-gray-800 rounded w-1/2"></div>
                <div className="h-20 bg-gray-800 rounded"></div>
                <div className="h-4 bg-gray-800 rounded w-1/4"></div>
              </div>
            </div>
          ))}
        </div>
      ) : filteredNews.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNews.map((news, index) => (
            <NewsCard key={index} news={news} formatDate={formatDate} formatTime={formatTime} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">No news found matching your criteria</div>
          <button
            className="btn btn-secondary"
            onClick={() => {
              setActiveCategory("all")
              setSearchQuery("")
            }}
          >
            Reset filters
          </button>
        </div>
      )}
    </div>
  )
}

interface NewsItem {
  title: string
  description: string
  source: { name: string }
  category?: string
  url: string
  urlToImage: string
  publishedAt: string
}

interface NewsCardProps {
  news: NewsItem
  formatDate: (date: string) => string
  formatTime: (date: string) => string
}

function NewsCard({ news, formatDate, formatTime }: NewsCardProps) {
  return (
    <div className="card overflow-hidden flex flex-col h-full hover:border-blue-500/30 transition-all duration-200">
      <div className="relative h-40">
        <Image src={news.urlToImage || "/placeholder.svg"} alt={news.title} fill className="object-cover" />
      </div>

      <div className="p-4 flex-1 flex flex-col">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{news.title}</h3>
        <p className="text-gray-400 text-sm mb-4 line-clamp-3">{news.description}</p>

        <div className="mt-auto flex items-center justify-between text-xs text-gray-500">
          <span>{formatDate(news.publishedAt)}</span>
          <span>{formatTime(news.publishedAt)}</span>
        </div>

        <a href={news.url} target="_blank" className="text-xs flex items-center text-blue-500 hover:text-blue-400">
          Read more <ExternalLink className="h-3 w-3 ml-1" />
        </a>
      </div>
    </div>
  )
}
