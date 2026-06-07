"use client";

import Link from "next/link";
import { Search, Shield, Building2, Globe, ArrowRight, BarChart3, Sparkles, Users } from "lucide-react";
import { useTheme } from "@/components/layout/ThemeProvider";

const features = [
  {
    icon: Search,
    title: "Email Intelligence",
    description: "Look up public information about any email address including domain details, MX records, and Gravatar profiles.",
  },
  {
    icon: Globe,
    title: "Domain Analysis",
    description: "Comprehensive WHOIS lookups, DNS records, SPF/DKIM/DMARC checks, and hosting provider detection.",
  },
  {
    icon: Building2,
    title: "Company Research",
    description: "Discover company details, tech stack, social media profiles, and industry classification from public sources.",
  },
  {
    icon: Shield,
    title: "Risk Assessment",
    description: "AI-powered risk scoring and security posture evaluation for domains and email addresses.",
  },
  {
    icon: BarChart3,
    title: "Search Analytics",
    description: "Track your searches, analyze patterns, and generate comprehensive reports with beautiful dashboards.",
  },
  {
    icon: Sparkles,
    title: "AI Insights",
    description: "Automated AI summaries for companies and domains with lead scoring and business intelligence.",
  },
];

export default function Home() {
  const { resolvedTheme } = useTheme();

  return (
    <div className="min-h-screen">
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-blue-50 dark:from-gray-950 dark:via-gray-900 dark:to-primary-950" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-gradient-to-br from-primary-400/20 to-blue-400/20 rounded-full blur-3xl" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
              <Sparkles className="w-4 h-4" />
              OSINT & Business Intelligence Platform
            </div>
            <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-6">
              Uncover Insights from
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-blue-600"> Public Data</span>
            </h1>
            <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
              Email Insight is a powerful OSINT platform that helps you research email addresses, domains, and companies using only publicly available information.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/register" className="btn-primary px-8 py-3 text-lg">
                Get Started Free <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="/search" className="btn-secondary px-8 py-3 text-lg">
                Try Email Lookup
              </Link>
            </div>
            <div className="flex items-center justify-center gap-8 mt-12 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center gap-2"><Users className="w-4 h-4" /> No account required</div>
              <div className="flex items-center gap-2"><Shield className="w-4 h-4" /> Public data only</div>
              <div className="flex items-center gap-2"><Search className="w-4 h-4" /> Free lookups</div>
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Everything You Need</h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Comprehensive tools for public data intelligence gathering
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div key={feature.title} className="card-hover p-6">
              <div className="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-gray-50 dark:bg-gray-900/50 py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Exploring?</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-xl mx-auto">
            Begin your research journey with Email Insight. No credit card required.
          </p>
          <Link href="/register" className="btn-primary px-8 py-3 text-lg">
            Create Free Account <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      <footer className="border-t border-gray-200 dark:border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>Email Insight &mdash; OSINT &amp; Business Intelligence Platform</p>
          <p className="mt-1">All data is sourced from publicly available information only.</p>
        </div>
      </footer>
    </div>
  );
}
