export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  company?: string;
  role: string;
  is_active: boolean;
  email_verified: boolean;
  avatar_url?: string;
  search_count: number;
  created_at: string;
  last_login?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface EmailResult {
  email: string;
  domain: string;
  username: string;
  is_business: boolean;
  possible_name?: string;
  known_usernames: string[];
  gravatar_url?: string;
  gravatar_has_profile: boolean;
  public_profiles: PublicProfile[];
  profile_count: number;
  mx_records: MXRecord[];
  dns_records: DNSRecord[];
  whois: WhoisInfo;
  company?: CompanyInfo;
  ai_summary?: string;
  risk_score: string;
}

export interface MXRecord {
  priority: number;
  host: string;
}

export interface DNSRecord {
  type: string;
  name: string;
  value: string;
  ttl?: number;
}

export interface WhoisInfo {
  registrar?: string;
  creation_date?: string;
  expiration_date?: string;
  updated_date?: string;
  name_servers: string[];
  registrar_abuse_contact?: string;
  dnssec: boolean;
  raw?: string;
}

export interface CompanyInfo {
  name?: string;
  domain?: string;
  website?: string;
  industry?: string;
  description?: string;
  employee_count?: string;
  founded_year?: string;
  headquarters?: string;
  social_media: Record<string, string>;
  tech_stack: string[];
  ai_summary?: string;
  risk_level: string;
  lead_score: number;
}

export interface PublicProfile {
  name: string;
  url: string;
  type: string;
  category: string;
  avatar?: string;
  display_name?: string;
  bio?: string;
  location?: string;
  details?: Record<string, string>;
}

export interface SearchHistoryItem {
  id: string;
  email: string;
  domain?: string;
  search_type: string;
  status: string;
  risk_score?: string;
  created_at: string;
}

export interface SearchAnalytics {
  total_searches: number;
  unique_domains: number;
  unique_emails: number;
  searches_today: number;
  searches_this_week: number;
  searches_this_month: number;
  top_domains: { domain: string; count: number }[];
  recent_searches: SearchHistoryItem[];
  searches_by_day: { date: string; count: number }[];
}

export interface DashboardStats {
  total_searches: number;
  searches_today: number;
  searches_this_month: number;
  unique_domains: number;
  unique_emails: number;
  avg_lead_score: number;
  risk_distribution: {
    low: number;
    medium: number;
    high: number;
  };
  recent_searches: {
    id: string;
    email: string;
    domain?: string;
    risk_score?: string;
    created_at: string;
  }[];
  top_domains: { domain: string; count: number }[];
  searches_by_day: { date: string; count: number }[];
}

export interface DomainResult {
  domain_name: string;
  registrar?: string;
  creation_date?: string;
  expiration_date?: string;
  name_servers: string[];
  mx_records: MXRecord[];
  spf_record?: string;
  dkim_record?: string;
  dmarc_record?: string;
  hosting_provider?: string;
  ip_address?: string;
  dnssec_enabled: boolean;
  dns_records: DNSRecord[];
}

export interface SearchResult {
  id: string;
  email: string;
  domain: string;
  search_type: string;
  status: string;
  result_data: EmailResult;
  risk_score?: string;
  ai_summary?: string;
  company?: CompanyInfo;
  domain_info?: WhoisInfo;
  created_at: string;
}
