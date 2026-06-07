export function SearchProgress() {
  return (
    <div className="card p-8 text-center">
      <div className="flex items-center justify-center gap-1 mb-4">
        <div className="w-3 h-3 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
        <div className="w-3 h-3 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
        <div className="w-3 h-3 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
      </div>
      <p className="text-sm text-gray-500 font-medium">Searching public sources...</p>
      <div className="mt-4 space-y-2 text-xs text-gray-400">
        <p>Checking DNS records...</p>
        <p>Looking up WHOIS data...</p>
        <p>Searching public profiles...</p>
      </div>
    </div>
  );
}
