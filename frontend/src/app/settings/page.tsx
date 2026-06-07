"use client";

import { useState, useEffect } from "react";
import { Settings, User, Lock, Moon, Sun, Monitor, Save, Loader2 } from "lucide-react";
import { api, getStoredUser, setStoredUser } from "@/lib/api";
import type { User as UserType } from "@/types";
import { useTheme } from "@/components/layout/ThemeProvider";
import toast from "react-hot-toast";

export default function SettingsPage() {
  const [user, setUser] = useState<UserType | null>(null);
  const [loading, setLoading] = useState(false);
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const { theme, setTheme, resolvedTheme } = useTheme();

  useEffect(() => {
    const stored = getStoredUser<UserType>();
    if (stored) {
      setUser(stored);
      setFullName(stored.full_name || "");
      setCompany(stored.company || "");
    }
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const updated = await api.auth.me();
      setUser(updated);
      setStoredUser(updated);
      toast.success("Profile updated");
    } catch {
      toast.error("Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    if (newPassword.length < 8) {
      toast.error("Password must be at least 8 characters");
      return;
    }
    setLoading(true);
    try {
      await api.auth.changePassword({ current_password: currentPassword, new_password: newPassword });
      toast.success("Password changed");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to change password";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const themeOptions = [
    { value: "light", label: "Light", icon: Sun },
    { value: "dark", label: "Dark", icon: Moon },
    { value: "system", label: "System", icon: Monitor },
  ] as const;

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-gray-500 dark:text-gray-400">Manage your account preferences</p>
      </div>

      <div className="space-y-6">
        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2"><User className="w-4 h-4 text-gray-400" /> Profile</h2>
          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1.5">Email</label>
              <input type="email" value={user?.email || ""} disabled className="input bg-gray-50 dark:bg-gray-800/50 cursor-not-allowed" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Username</label>
              <input type="text" value={user?.username || ""} disabled className="input bg-gray-50 dark:bg-gray-800/50 cursor-not-allowed" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Full Name</label>
              <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} className="input" placeholder="Your full name" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Company</label>
              <input type="text" value={company} onChange={(e) => setCompany(e.target.value)} className="input" placeholder="Your company" />
            </div>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Save Changes
            </button>
          </form>
        </div>

        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2"><Lock className="w-4 h-4 text-gray-400" /> Change Password</h2>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1.5">Current Password</label>
              <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} className="input" required />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">New Password</label>
              <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="input" placeholder="Min. 8 characters" required />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Confirm New Password</label>
              <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="input" required />
            </div>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Update Password
            </button>
          </form>
        </div>

        <div className="card p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            {resolvedTheme === "dark" ? <Moon className="w-4 h-4 text-gray-400" /> : <Sun className="w-4 h-4 text-gray-400" />}
            Theme
          </h2>
          <div className="flex gap-3">
            {themeOptions.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setTheme(opt.value)}
                className={`flex items-center gap-2 px-4 py-3 rounded-lg border-2 transition-all ${
                  theme === opt.value
                    ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                    : "border-gray-200 dark:border-gray-700 hover:border-gray-300"
                }`}
              >
                <opt.icon className="w-4 h-4" />
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
