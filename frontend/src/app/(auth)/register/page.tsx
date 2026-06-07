"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Search, Loader2 } from "lucide-react";
import { api, setStoredTokens, setStoredUser } from "@/lib/api";
import toast from "react-hot-toast";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    full_name: "",
    company: "",
  });
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.email || !formData.username || !formData.password) {
      toast.error("Please fill in all required fields");
      return;
    }
    if (formData.password.length < 8) {
      toast.error("Password must be at least 8 characters");
      return;
    }
    setLoading(true);
    try {
      const result = await api.auth.register(formData);
      setStoredTokens(result);
      setStoredUser(result.user);
      toast.success("Account created successfully!");
      router.push("/dashboard");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Registration failed";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-primary-600 flex items-center justify-center mx-auto mb-4">
            <Search className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold">Create Account</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">Start exploring public data</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5">Email *</label>
            <input type="email" name="email" value={formData.email} onChange={handleChange} className="input" placeholder="you@company.com" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">Username *</label>
            <input type="text" name="username" value={formData.username} onChange={handleChange} className="input" placeholder="johndoe" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">Password *</label>
            <input type="password" name="password" value={formData.password} onChange={handleChange} className="input" placeholder="Min. 8 characters" required />
            <p className="text-xs text-gray-400 mt-1">Must contain uppercase, lowercase, and a number</p>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">Full Name</label>
            <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} className="input" placeholder="John Doe" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">Company</label>
            <input type="text" name="company" value={formData.company} onChange={handleChange} className="input" placeholder="Acme Inc." />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-gray-500">
          Already have an account?{" "}
          <Link href="/login" className="text-primary-600 hover:text-primary-700 font-medium">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
