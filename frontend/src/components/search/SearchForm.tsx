"use client";

import { useState } from "react";
import { Search, Mail, Loader2 } from "lucide-react";
import { isValidEmail } from "@/lib/utils";
import toast from "react-hot-toast";

interface SearchFormProps {
  onSearch: (email: string) => Promise<void>;
  loading?: boolean;
}

export function SearchForm({ onSearch, loading }: SearchFormProps) {
  const [email, setEmail] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = email.trim().toLowerCase();
    if (!trimmed) { toast.error("Enter an email address"); return; }
    if (!isValidEmail(trimmed)) { toast.error("Invalid email format"); return; }
    await onSearch(trimmed);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <div className="flex-1 relative">
        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="input pl-10 h-12 text-base"
          placeholder="you@company.com"
        />
      </div>
      <button type="submit" disabled={loading} className="btn-primary h-12 px-6">
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
        {loading ? "Searching..." : "Lookup"}
      </button>
    </form>
  );
}
