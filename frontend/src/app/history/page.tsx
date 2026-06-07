"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { History, Search, Trash2, Loader2, ExternalLink, Download, Filter, ChevronLeft, ChevronRight } from "lucide-react";
import { api } from "@/lib/api";
import type { SearchHistoryItem } from "@/types";
import { formatRelativeTime, getRiskBadge, cn } from "@/lib/utils";
import toast from "react-hot-toast";

export default function HistoryPage() {
  const [items, setItems] = useState<SearchHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [filter, setFilter] = useState<string>("");
  const perPage = 20;

  useEffect(() => {
    loadHistory();
  }, [page, filter]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = { page: String(page), per_page: String(perPage) };
      if (filter) params.search_type = filter;
      const data = await api.search.history(params);
      setItems(data);
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleSelect = (id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selected.size === items.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(items.map(i => i.id)));
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.search.delete(id);
      setItems(prev => prev.filter(i => i.id !== id));
      toast.success("Search deleted");
    } catch {
      toast.error("Failed to delete");
    }
  };

  const handleExport = async (format: string) => {
    if (selected.size === 0) { toast.error("Select searches to export"); return; }
    try {
      const blob = await api.search.export({ search_ids: Array.from(selected), format_type: format });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `email-insight-export.${format}`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Export downloaded");
    } catch {
      toast.error("Export failed");
    }
  };

  const handleDeleteSelected = async () => {
    if (selected.size === 0) return;
    for (const id of selected) await handleDelete(id);
    setSelected(new Set());
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Search History</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">{items.length} results</p>
        </div>
        <div className="flex items-center gap-2">
          {selected.size > 0 && (
            <>
              <span className="text-sm text-gray-500">{selected.size} selected</span>
              <button onClick={() => handleExport("csv")} className="btn-secondary text-sm"><Download className="w-4 h-4" /> CSV</button>
              <button onClick={() => handleExport("json")} className="btn-secondary text-sm"><Download className="w-4 h-4" /> JSON</button>
              <button onClick={handleDeleteSelected} className="btn-danger text-sm"><Trash2 className="w-4 h-4" /></button>
            </>
          )}
          <select value={filter} onChange={(e) => { setFilter(e.target.value); setPage(1); }} className="input text-sm w-auto">
            <option value="">All Types</option>
            <option value="email">Email</option>
            <option value="domain">Domain</option>
            <option value="company">Company</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>
      ) : items.length === 0 ? (
        <div className="card p-12 text-center">
          <History className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="font-medium mb-2">No search history yet</h3>
          <p className="text-sm text-gray-500 mb-4">Start by looking up an email address</p>
          <Link href="/search" className="btn-primary"><Search className="w-4 h-4" /> New Search</Link>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="hidden sm:grid grid-cols-12 gap-4 px-4 py-3 text-xs font-medium text-gray-500 border-b border-gray-200 dark:border-gray-700">
            <div className="col-span-1"><input type="checkbox" checked={selected.size === items.length && items.length > 0} onChange={toggleSelectAll} className="rounded" /></div>
            <div className="col-span-4">Email</div>
            <div className="col-span-2">Domain</div>
            <div className="col-span-2">Type</div>
            <div className="col-span-1">Risk</div>
            <div className="col-span-1">Time</div>
            <div className="col-span-1" />
          </div>

          {items.map((item) => (
            <div key={item.id} className="grid grid-cols-12 gap-4 items-center px-4 py-3 border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
              <div className="col-span-1">
                <input type="checkbox" checked={selected.has(item.id)} onChange={() => toggleSelect(item.id)} className="rounded" />
              </div>
              <div className="col-span-4 sm:col-span-4 min-w-0">
                <Link href={`/search/${item.id}`} className="text-sm font-medium hover:text-primary-600 truncate block">
                  {item.email}
                </Link>
              </div>
              <div className="col-span-2 text-sm text-gray-500 truncate hidden sm:block">{item.domain || "—"}</div>
              <div className="col-span-2 text-sm text-gray-500 hidden sm:block">
                <span className="badge bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">{item.search_type}</span>
              </div>
              <div className="col-span-1">
                <span className={cn("badge", getRiskBadge(item.risk_score || ""))}>{item.risk_score?.toUpperCase() || "—"}</span>
              </div>
              <div className="col-span-1 text-xs text-gray-400 hidden sm:block">{formatRelativeTime(item.created_at)}</div>
              <div className="col-span-1 flex justify-end gap-1">
                <Link href={`/search/${item.id}`} className="btn-ghost p-1"><ExternalLink className="w-3.5 h-3.5" /></Link>
                <button onClick={() => handleDelete(item.id)} className="btn-ghost p-1 text-red-500"><Trash2 className="w-3.5 h-3.5" /></button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-6">
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary text-sm">
          <ChevronLeft className="w-4 h-4" /> Previous
        </button>
        <span className="text-sm text-gray-500">Page {page}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={items.length < perPage} className="btn-secondary text-sm">
          Next <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
