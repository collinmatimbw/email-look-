"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Search, ArrowLeft, Loader2, Globe, Building2, Shield, ExternalLink } from "lucide-react";
import { api } from "@/lib/api";
import type { SearchResult, MXRecord, DNSRecord, WhoisInfo, CompanyInfo } from "@/types";
import { cn, getRiskBadge, formatDate } from "@/lib/utils";

export default function SearchDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) loadDetail();
  }, [id]);

  const loadDetail = async () => {
    try {
      const data = await api.search.detail(id);
      setResult(data);
    } catch {
      // Handle error
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-[60vh] flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;
  }

  if (!result) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <p className="text-gray-500">Search not found</p>
        <Link href="/history" className="btn-primary mt-4">Back to History</Link>
      </div>
    );
  }

  const InfoRow = ({ label, value }: { label: string; value: React.ReactNode }) => (
    <div className="flex justify-between py-1.5 text-sm">
      <span className="text-gray-500">{label}</span>
      <span className="font-medium text-right ml-4">{value || "—"}</span>
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Link href="/history" className="btn-ghost text-sm mb-6">
        <ArrowLeft className="w-4 h-4" /> Back to History
      </Link>

      <div className="card p-5 mb-6">
        <div className="flex items-start gap-4">
          {result.result_data?.gravatar_url && <img src={result.result_data.gravatar_url} alt="" className="w-14 h-14 rounded-full" />}
          <div className="flex-1 min-w-0">
            <h1 className="text-lg font-semibold break-all">{result.email}</h1>
            <p className="text-sm text-gray-500">Domain: {result.domain}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className={cn("badge", getRiskBadge(result.risk_score || ""))}>{result.risk_score?.toUpperCase()} Risk</span>
              <span className="text-xs text-gray-400">{formatDate(result.created_at)}</span>
            </div>
          </div>
        </div>
      </div>

      {result.ai_summary && (
        <div className="card p-4 mb-4">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-4 h-4 text-primary-600" />
            <span className="font-medium text-sm">AI Summary</span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{result.ai_summary}</p>
        </div>
      )}

      <div className="space-y-4">
        <div className="card p-4">
          <h3 className="font-medium text-sm mb-3 flex items-center gap-2"><Globe className="w-4 h-4 text-gray-400" /> MX Records</h3>
          {result.result_data?.mx_records?.length ? (
            <div className="space-y-1">
              {result.result_data.mx_records.map((mx: MXRecord, i: number) => (
                <div key={i} className="flex justify-between text-sm py-1">
                  <span className="font-mono text-xs">{mx.host}</span>
                  <span className="text-gray-500 text-xs">Priority: {mx.priority}</span>
                </div>
              ))}
            </div>
          ) : <p className="text-sm text-gray-400">No MX records found</p>}
        </div>

        <div className="card p-4">
          <h3 className="font-medium text-sm mb-3 flex items-center gap-2"><Globe className="w-4 h-4 text-gray-400" /> Domain Info</h3>
          {result.result_data?.whois ? (
            <>
              <InfoRow label="Registrar" value={(result.result_data.whois as WhoisInfo).registrar} />
              <InfoRow label="Created" value={(result.result_data.whois as WhoisInfo).creation_date} />
              <InfoRow label="Expires" value={(result.result_data.whois as WhoisInfo).expiration_date} />
            </>
          ) : <p className="text-sm text-gray-400">No domain info available</p>}
        </div>

        <div className="card p-4">
          <h3 className="font-medium text-sm mb-3 flex items-center gap-2"><Building2 className="w-4 h-4 text-gray-400" /> Company</h3>
          {result.result_data?.company ? (
            <>
              <InfoRow label="Name" value={(result.result_data.company as CompanyInfo).name} />
              <InfoRow label="Industry" value={(result.result_data.company as CompanyInfo).industry} />
              <InfoRow label="Lead Score" value={result.result_data.company.lead_score ? `${result.result_data.company.lead_score}%` : "—"} />
              {(result.result_data.company as CompanyInfo).tech_stack?.length > 0 && (
                <div className="mt-2">
                  <span className="text-sm text-gray-500">Tech Stack:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {(result.result_data.company as CompanyInfo).tech_stack.map((tech: string) => (
                      <span key={tech} className="badge bg-gray-100 dark:bg-gray-800 text-xs">{tech}</span>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : <p className="text-sm text-gray-400">No company data available</p>}
        </div>
      </div>
    </div>
  );
}
