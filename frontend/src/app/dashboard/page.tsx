"use client";

import { useAuth } from "@/lib/auth-context";


export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <main>
      <header>
        <h1>{user?.name}</h1>

        <button onClick={logout}>
          Logout
        </button>
      </header>
    </main>
  );
}
