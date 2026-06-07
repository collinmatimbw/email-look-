"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, TrendingUp, Globe, AlertTriangle, Target, Loader2, ArrowRight, Clock, BarChart3 } from "lucide-react";
import { api } from "@/lib/api";
import type { DashboardStats } from "@/types";
import { formatRelativeTime, getRiskBadge, cn } from "@/lib/utils";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await api.dashboard.stats();
      setStats(data);
    } catch {
      // Will need auth redirect
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Sign in to view dashboard</h2>
          <Link href="/login" className="btn-primary">Sign In</Link>
        </div>
      </div>
    );
  }

  const statCards = [
    { label: "Total Searches", value: stats.total_searches, icon: Search, color: "text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400" },
    { label: "Searches Today", value: stats.searches_today, icon: TrendingUp, color: "text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400" },
    { label: "Unique Domains", value: stats.unique_domains, icon: Globe, color: "text-purple-600 bg-purple-100 dark:bg-purple-900/30 dark:text-purple-400" },
    { label: "Avg. Lead Score", value: `${stats.avg_lead_score}%`, icon: Target, color: "text-orange-600 bg-orange-100 dark:bg-orange-900/30 dark:text-orange-400" },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-gray-500 dark:text-gray-400">Your intelligence overview</p>
        </div>
        <Link href="/search" className="btn-primary">
          <Search className="w-4 h-4" /> New Search
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((card) => (
          <div key={card.label} className="card p-5">
            <div className="flex items-center justify-between mb-3">
              <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", card.color)}>
                <card.icon className="w-5 h-5" />
              </div>
            </div>
            <p className="text-2xl font-bold">{card.value}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">{card.label}</p>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-400" /> Recent Searches
          </h2>
          <div className="space-y-3">
            {stats.recent_searches.slice(0, 5).map((s) => (
              <div key={s.id} className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-800 last:border-0">
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium truncate">{s.email}</p>
                  <p className="text-xs text-gray-500">{formatRelativeTime(s.created_at)}</p>
                </div>
                <span className={cn("badge", getRiskBadge(s.risk_score || ""))}>
                  {s.risk_score || "N/A"}
                </span>
              </div>
            ))}
            {stats.recent_searches.length === 0 && (
              <p className="text-sm text-gray-400 text-center py-4">No searches yet</p>
            )}
          </div>
          {stats.recent_searches.length > 0 && (
            <Link href="/history" className="btn-ghost w-full mt-4 text-sm justify-center">
              View All <ArrowRight className="w-3 h-3" />
            </Link>
          )}
        </div>

        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Globe className="w-4 h-4 text-gray-400" /> Top Domains
          </h2>
          <div className="space-y-3">
            {stats.top_domains.map((d, i) => (
              <div key={d.domain} className="flex items-center justify-between py-2">
                <div className="flex items-center gap-3 min-w-0">
                  <span className="text-sm text-gray-400 w-5">{i + 1}</span>
                  <span className="text-sm font-medium truncate">{d.domain}</span>
                </div>
                <span className="text-sm text-gray-500">{d.count} searches</span>
              </div>
            ))}
            {stats.top_domains.length === 0 && (
              <p className="text-sm text-gray-400 text-center py-4">No domain data yet</p>
            )}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-gray-400" /> Risk Distribution
          </h2>
          <div className="space-y-4">
            {[
              { label: "Low Risk", value: stats.risk_distribution.low, color: "bg-green-500" },
              { label: "Medium Risk", value: stats.risk_distribution.medium, color: "bg-yellow-500" },
              { label: "High Risk", value: stats.risk_distribution.high, color: "bg-red-500" },
            ].map((item) => {
              const total = stats.risk_distribution.low + stats.risk_distribution.medium + stats.risk_distribution.high;
              const pct = total > 0 ? Math.round((item.value / total) * 100) : 0;
              return (
                <div key={item.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span>{item.label}</span>
                    <span className="text-gray-500">{item.value} ({pct}%)</span>
                  </div>
                  <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div className={cn("h-full rounded-full transition-all", item.color)} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-gray-400" /> Monthly Activity
          </h2>
          <div className="space-y-2">
            {stats.searches_by_day.slice(-14).map((day) => {
              const maxCount = Math.max(...stats.searches_by_day.map(d => d.count), 1);
              const heightPct = (day.count / maxCount) * 100;
              return (
                <div key={day.date} className="flex items-center gap-3">
                  <span className="text-xs text-gray-400 w-20 truncate">{day.date.slice(5)}</span>
                  <div className="flex-1 h-5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div className="h-full bg-primary-500 rounded-full transition-all" style={{ width: `${heightPct}%` }} />
                  </div>
                  <span className="text-xs text-gray-500 w-6 text-right">{day.count}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
