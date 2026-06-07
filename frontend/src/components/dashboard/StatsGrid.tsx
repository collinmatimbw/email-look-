import { Search, TrendingUp, Globe, Target } from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";

interface StatsGridProps {
  totalSearches: number;
  searchesToday: number;
  uniqueDomains: number;
  avgLeadScore: number;
}

export function StatsGrid({ totalSearches, searchesToday, uniqueDomains, avgLeadScore }: StatsGridProps) {
  const stats = [
    { label: "Total Searches", value: totalSearches, icon: Search, color: "text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400" },
    { label: "Searches Today", value: searchesToday, icon: TrendingUp, color: "text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400" },
    { label: "Unique Domains", value: uniqueDomains, icon: Globe, color: "text-purple-600 bg-purple-100 dark:bg-purple-900/30 dark:text-purple-400" },
    { label: "Avg. Lead Score", value: `${avgLeadScore}%`, icon: Target, color: "text-orange-600 bg-orange-100 dark:bg-orange-900/30 dark:text-orange-400" },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <StatCard key={stat.label} {...stat} />
      ))}
    </div>
  );
}
