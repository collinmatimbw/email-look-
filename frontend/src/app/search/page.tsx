"use client";

import { useState } from "react";
import { Search, Mail, Loader2, Globe, Building2, Shield, ExternalLink, Clock, Server, Flag, MapPin, Hash, Activity, ChevronRight, AlertTriangle, User, MapPinned, Bookmark, Users, Package, Star, GitFork, CalendarDays, MessageCircle, Award, Code2, Key, Fingerprint, Terminal, Image, Palette, Camera, Briefcase, Link } from "lucide-react";
import { api } from "@/lib/api";
import type { SearchResult, MXRecord, DNSRecord, WhoisInfo, CompanyInfo } from "@/types";
import { isValidEmail, cn, getRiskBadge } from "@/lib/utils";
import toast from "react-hot-toast";

export default function SearchPage() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = email.trim().toLowerCase();
    if (!trimmed) { toast.error("Enter an email address"); return; }
    if (!isValidEmail(trimmed)) { toast.error("Invalid email format"); return; }
    setLoading(true);
    setResult(null);
    try {
      const data = await api.email.lookup({ email: trimmed });
      setResult(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Lookup failed";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const InfoRow = ({ label, value, href }: { label: string; value: React.ReactNode; href?: string }) => (
    <div className="flex items-start gap-3 px-4 py-2.5 border-b border-gray-100 dark:border-gray-800/50 last:border-0">
      <span className="text-xs font-medium text-gray-400 dark:text-gray-500 w-28 shrink-0 pt-0.5">{label}</span>
      <div className="flex-1 text-sm">
        {href ? (
          <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary-600 dark:text-primary-400 hover:underline inline-flex items-center gap-1">
            {value} <ExternalLink className="w-3 h-3" />
          </a>
        ) : (
          <span className="text-gray-900 dark:text-gray-100">{value || <span className="text-gray-400 italic">Not found</span>}</span>
        )}
      </div>
    </div>
  );

  const Badge = ({ children, color }: { children: React.ReactNode; color?: string }) => (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium", color || "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300")}>
      {children}
    </span>
  );

  const Section = ({ title, icon: Icon, children }: { title: string; icon: React.ElementType; children: React.ReactNode }) => (
    <div className="card overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
        <Icon className="w-4 h-4 text-primary-500" />
        <span className="font-semibold text-sm text-gray-700 dark:text-gray-200">{title}</span>
      </div>
      <div className="divide-y divide-gray-100 dark:divide-gray-800/50">{children}</div>
    </div>
  );

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold mb-2">Email Intelligence</h1>
        <p className="text-gray-500 dark:text-gray-400">Comprehensive public data intelligence platform</p>
      </div>

      <form onSubmit={handleLookup} className="max-w-2xl mx-auto mb-8">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="input pl-10 h-12 text-base" placeholder="you@company.com" />
          </div>
          <button type="submit" disabled={loading} className="btn-primary h-12 px-6 min-w-[120px]">
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
            {loading ? "Scanning..." : "Investigate"}
          </button>
        </div>
      </form>

      {loading && (
        <div className="card p-8 text-center max-w-lg mx-auto">
          <Loader2 className="w-10 h-10 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Gathering intelligence</p>
          <div className="space-y-1.5">
            <div className="flex items-center justify-center gap-2 text-xs text-gray-400"><Loader2 className="w-3 h-3 animate-spin" /> Checking Gravatar...</div>
            <div className="flex items-center justify-center gap-2 text-xs text-gray-400"><Loader2 className="w-3 h-3 animate-spin" /> Searching public profiles...</div>
            <div className="flex items-center justify-center gap-2 text-xs text-gray-400"><Loader2 className="w-3 h-3 animate-spin" /> Cross-referencing username variants...</div>
          </div>
        </div>
      )}

      {result && (
        <div className="space-y-5">
          {/* HEADER — Person-first */}
          <div className="card p-5">
            <div className="flex items-start gap-5">
              {result.result_data?.gravatar_url && (
                <div className="relative shrink-0">
                  <img src={result.result_data.gravatar_url} alt="" className="w-16 h-16 rounded-full ring-2 ring-gray-100 dark:ring-gray-800" />
                  {result.result_data?.gravatar_has_profile && (
                    <span className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center text-white text-[10px] font-bold">G</span>
                  )}
                </div>
              )}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-xl font-bold break-all">{result.email}</h2>
                    {result.result_data?.possible_name && (
                      <p className="text-base text-gray-600 dark:text-gray-400 mt-1 font-medium">{result.result_data.possible_name}</p>
                    )}
                    <p className="text-xs text-gray-400 mt-0.5">@{result.result_data?.username || result.email.split("@")[0]}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={cn("px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider", getRiskBadge(result.risk_score || ""))}>
                      {result.risk_score || "N/A"} Risk
                    </span>
                    {result.result_data?.is_business && (
                      <span className="px-3 py-1 rounded-lg text-xs font-bold bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                        Business
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-3 mt-3">
                  <span className="text-xs text-gray-400 flex items-center gap-1"><User className="w-3 h-3" /> {result.result_data?.profile_count || 0} profiles</span>
                  <span className="text-xs text-gray-400 flex items-center gap-1"><Hash className="w-3 h-3" /> {result.result_data?.known_usernames?.length || 1} username(s)</span>
                  {result.result_data?.is_business && (
                    <span className="text-xs text-gray-400 flex items-center gap-1"><Building2 className="w-3 h-3" /> {result.result_data?.domain}</span>
                  )}
                  <span className="text-xs text-gray-400 flex items-center gap-1"><Clock className="w-3 h-3" /> {new Date(result.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>

          {/* AI SUMMARY */}
          {(result.ai_summary || result.result_data?.ai_summary) && (
            <div className="card overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-3 bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-950/30 dark:to-blue-950/30 border-b border-primary-100 dark:border-primary-900/30">
                <Activity className="w-4 h-5 text-primary-600" />
                <span className="font-semibold text-sm text-primary-700 dark:text-primary-300">AI Intelligence Summary</span>
              </div>
              <div className="p-4 text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                {result.ai_summary || result.result_data?.ai_summary}
              </div>
            </div>
          )}

          {/* KNOWN USERNAMES */}
          {result.result_data?.known_usernames && result.result_data.known_usernames.length > 1 && (
            <Section title="Known Usernames" icon={Hash}>
              <div className="px-4 py-3 flex flex-wrap gap-1.5">
                {result.result_data.known_usernames.map((u: string) => (
                  <Badge key={u}>{u}</Badge>
                ))}
              </div>
            </Section>
          )}

          {/* DOMAIN INFO (business only) */}
          {result.result_data?.is_business && (
            <>
              <div className="grid lg:grid-cols-2 gap-5">
                {result.result_data?.mx_records && result.result_data.mx_records.length > 0 && (
                  <Section title="MX Records" icon={Mail}>
                    {result.result_data.mx_records.map((mx: MXRecord, i: number) => (
                      <div key={i} className="flex items-center gap-3 px-4 py-2.5 border-b border-gray-100 dark:border-gray-800/50 last:border-0">
                        <span className="text-xs text-gray-400 w-6">{i + 1}.</span>
                        <span className="font-mono text-xs text-gray-900 dark:text-gray-100 flex-1 break-all">{mx.host}</span>
                        <Badge>Priority {mx.priority}</Badge>
                      </div>
                    ))}
                  </Section>
                )}
                {result.result_data?.dns_records && result.result_data.dns_records.length > 0 && (
                  <Section title="DNS Records" icon={Globe}>
                    {result.result_data.dns_records.slice(0, 10).map((rec: DNSRecord, i: number) => (
                      <div key={i} className="flex items-center gap-2 px-4 py-2 border-b border-gray-100 dark:border-gray-800/50 last:border-0">
                        <Badge color="bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 font-mono">{rec.type}</Badge>
                        <span className="font-mono text-xs text-gray-500 truncate flex-1">{rec.name}</span>
                        <span className="font-mono text-xs text-gray-900 dark:text-gray-100 truncate max-w-[200px] text-right">{rec.value}</span>
                      </div>
                    ))}
                    {result.result_data.dns_records.length > 10 && (
                      <div className="px-4 py-2 text-xs text-gray-400 text-center">+ {result.result_data.dns_records.length - 10} more</div>
                    )}
                  </Section>
                )}
              </div>

              {result.result_data?.whois && (
                <Section title="Domain Registration (WHOIS)" icon={Globe}>
                  <div className="grid sm:grid-cols-2">
                    <InfoRow label="Registrar" value={(result.result_data.whois as WhoisInfo).registrar} />
                    <InfoRow label="Created" value={(result.result_data.whois as WhoisInfo).creation_date} />
                    <InfoRow label="Expires" value={(result.result_data.whois as WhoisInfo).expiration_date} />
                    <InfoRow label="DNSSEC" value={(result.result_data.whois as WhoisInfo).dnssec ? "Enabled" : "Not enabled"} />
                  </div>
                </Section>
              )}

              {result.result_data?.company && (
                <Section title="Company" icon={Building2}>
                  <div className="grid sm:grid-cols-2">
                    <InfoRow label="Company" value={(result.result_data.company as CompanyInfo).name} href={(result.result_data.company as CompanyInfo).website} />
                    <InfoRow label="Industry" value={(result.result_data.company as CompanyInfo).industry} />
                    <InfoRow label="Founded" value={(result.result_data.company as CompanyInfo).founded_year} />
                    <InfoRow label="Employees" value={(result.result_data.company as CompanyInfo).employee_count} />
                    <InfoRow label="Location" value={(result.result_data.company as CompanyInfo).headquarters} />
                  </div>
                  {(result.result_data.company as CompanyInfo).description && (
                    <div className="border-t border-gray-100 dark:border-gray-800/50 px-4 py-3">
                      <span className="text-xs font-medium text-gray-400 dark:text-gray-500 block mb-1">Description</span>
                      <p className="text-sm text-gray-700 dark:text-gray-300">{(result.result_data.company as CompanyInfo).description}</p>
                    </div>
                  )}
                  {(result.result_data.company as CompanyInfo).tech_stack && (result.result_data.company as CompanyInfo).tech_stack.length > 0 && (
                    <div className="border-t border-gray-100 dark:border-gray-800/50 px-4 py-3">
                      <span className="text-xs font-medium text-gray-400 dark:text-gray-500 block mb-2">Tech Stack</span>
                      <div className="flex flex-wrap gap-1.5">
                        {(result.result_data.company as CompanyInfo).tech_stack.map((tech: string) => (
                          <Badge key={tech}>{tech}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </Section>
              )}
            </>
          )}

          {/* PUBLIC PROFILES */}
          {result.result_data?.public_profiles && result.result_data.public_profiles.length > 0 && (
            <Section title={`Accounts (${result.result_data.public_profiles.length})`} icon={Shield}>
              <div className="p-4 space-y-4">
                {result.result_data.public_profiles.map((profile) => {
                  const brandColors: Record<string, string> = {
                    github: "from-[#333] to-[#24292e]",
                    gitlab: "from-[#FC6D26] to-[#E24329]",
                    reddit: "from-[#FF4500] to-[#FF6A33]",
                    hackernews: "from-[#FF6600] to-[#FF8533]",
                    devto: "from-[#0A0A0A] to-[#333] dark:from-[#eee] dark:to-[#ccc]",
                    keybase: "from-[#33A0FF] to-[#0066CC]",
                    docker: "from-[#2496ED] to-[#1D7FCF]",
                    npm: "from-[#CB3837] to-[#A82E2D]",
                    pypi: "from-[#3775A9] to-[#2A5D84]",
                    bitbucket: "from-[#0052CC] to-[#003D99]",
                    linkedin: "from-[#0077B5] to-[#005A8C]",
                    twitter: "from-[#1DA1F2] to-[#0D8BD9]",
                    instagram: "from-[#F58529] via-[#DD2A7B] to-[#515BD4]",
                    youtube: "from-[#FF0000] to-[#CC0000]",
                    medium: "from-[#000] to-[#333] dark:from-[#fff] dark:to-[#ccc]",
                    telegram: "from-[#26A5E4] to-[#1B8CCE]",
                    stackoverflow: "from-[#F48024] to-[#D4661E]",
                    producthunt: "from-[#DA552F] to-[#B84424]",
                    behance: "from-[#1769FF] to-[#0F4FBF]",
                    dribbble: "from-[#EA4C89] to-[#D93A77]",
                    tiktok: "from-[#000] to-[#333] dark:from-[#fff] dark:to-[#ccc]",
                    pinterest: "from-[#E60023] to-[#BD001C]",
                    snapchat: "from-[#FFFC00] to-[#E6E300]",
                    facebook: "from-[#1877F2] to-[#0F5FBF]",
                    hackerone: "from-[#222] to-[#111]",
                    bugcrowd: "from-[#F26822] to-[#D45418]",
                    tryhackme: "from-[#212C42] to-[#151D2E]",
                    rubygems: "from-[#E9573F] to-[#CC3F2A]",
                    cratesio: "from-[#F7DF1E] to-[#D4BC1A]",
                    angellist: "from-[#000] to-[#333]",
                    crunchbase: "from-[#0288D1] to-[#016DA8]",
                    aboutme: "from-[#333399] to-[#262680]",
                    flickr: "from-[#FF0084] to-[#CC0069]",
                  };
                  const pk = profile.name.toLowerCase().replace(/[\s.]+/g, "");
                  const gradient = brandColors[pk] || "from-gray-500 to-gray-600";
                  const renderIcon = pk === "github" ? <Code2 className="w-5 h-5" /> :
                    pk === "gitlab" ? <GitFork className="w-5 h-5" /> :
                    pk === "reddit" ? <MessageCircle className="w-5 h-5" /> :
                    pk === "hackernews" ? <Award className="w-5 h-5" /> :
                    pk === "keybase" ? <Key className="w-5 h-5" /> :
                    pk === "docker" || pk === "npm" || pk === "pypi" || pk === "rubygems" || pk === "cratesio" ? <Package className="w-5 h-5" /> :
                    pk === "devto" ? <Terminal className="w-5 h-5" /> :
                    pk === "bitbucket" ? <Code2 className="w-5 h-5" /> :
                    pk === "linkedin" ? <Briefcase className="w-5 h-5" /> :
                    pk === "stackoverflow" ? <Bookmark className="w-5 h-5" /> :
                    pk === "behance" || pk === "dribbble" ? <Palette className="w-5 h-5" /> :
                    pk === "flickr" ? <Camera className="w-5 h-5" /> :
                    pk === "medium" ? <Bookmark className="w-5 h-5" /> :
                    <User className="w-5 h-5" />;

                  const details = profile.details || {};
                  const detailEntries = Object.entries(details);

                  return (
                    <div key={profile.url} className="rounded-xl border bg-white dark:bg-gray-900 overflow-hidden">
                      <div className="flex items-center gap-3 px-4 pt-4 pb-3 border-b bg-gray-50/50 dark:bg-gray-800/50">
                        <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${gradient} flex items-center justify-center text-white shadow-sm`}>
                          {renderIcon}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-sm">{profile.name}</h3>
                          <p className="text-xs text-gray-400">{profile.type}</p>
                        </div>
                        <a href={profile.url} target="_blank" rel="noopener noreferrer"
                          className="text-xs text-gray-400 hover:text-primary-500 transition-colors flex items-center gap-1 shrink-0">
                          View <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>

                      <div className="p-4">
                        <div className="flex items-start gap-4">
                          {profile.avatar && (
                            <img src={profile.avatar} alt="" className="w-16 h-16 rounded-xl object-cover shrink-0 border" referrerPolicy="no-referrer" />
                          )}
                          <div className="flex-1 min-w-0 space-y-2">
                            {profile.display_name && (
                              <p className="font-semibold text-base leading-tight">{profile.display_name}</p>
                            )}
                            {profile.bio && (
                              <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{profile.bio}</p>
                            )}
                            {profile.location && (
                              <p className="text-xs text-gray-400 flex items-center gap-1">
                                <MapPinned className="w-3 h-3" /> {profile.location}
                              </p>
                            )}
                          </div>
                        </div>

                        {detailEntries.length > 0 && (
                          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mt-4 pt-4 border-t">
                            {detailEntries.map(([key, val]) => (
                              <div key={key} className="space-y-0.5">
                                <p className="text-[10px] uppercase tracking-wider text-gray-400 font-medium">{key}</p>
                                <p className="text-sm font-semibold truncate">{val || "N/A"}</p>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </Section>
          )}

          {/* RAW DATA FOOTER */}
          <div className="text-center text-xs text-gray-400 dark:text-gray-600 py-4">
            <p>All data is gathered from publicly available sources only.</p>
          </div>
        </div>
      )}

      {!loading && !result && (
        <div className="card p-16 text-center max-w-lg mx-auto">
          <Search className="w-14 h-14 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Investigate an Email Address</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Enter any email address above to gather publicly available intelligence including domain information, company data, security records, and more.
          </p>
          <div className="grid grid-cols-2 gap-3 text-xs text-gray-400 max-w-xs mx-auto">
            <div className="card p-3 text-center">DNS Records</div>
            <div className="card p-3 text-center">WHOIS Data</div>
            <div className="card p-3 text-center">MX Records</div>
            <div className="card p-3 text-center">SPF/DKIM/DMARC</div>
            <div className="card p-3 text-center">Company Intel</div>
            <div className="card p-3 text-center">Tech Stack</div>
          </div>
        </div>
      )}
    </div>
  );
}
