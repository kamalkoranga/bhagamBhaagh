"use client";

import { LoginRequest, ProfileOut, RegisterRequest, TokenResponse, UserOut } from "@/types/api";
import { useRouter } from "next/navigation";
import React, { createContext, useContext, useEffect, useState } from "react";
import { fetchApi } from "./api";

interface AuthContextType {
  user: UserOut | null;
  token: string | null;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (credentials: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({
  children
}: {
    children: React.ReactNode;
  }) {
  const [user, setUser] = useState<UserOut | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const router = useRouter();

  const saveAuthData = (data: TokenResponse) => {
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
    setUser(data.user);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('token');

      if (!storedToken) {
        setIsLoading(false);
        return;
      }

      try {
        const profile = await fetchApi<ProfileOut>("/profile");

        setToken(storedToken);
        setUser(profile);
      } catch {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: LoginRequest) => {
    const data = await fetchApi<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials)
    });

    saveAuthData(data);
    router.push("/dashboard");
  }

  const register = async (credentials: RegisterRequest) => {
    const data = await fetchApi<TokenResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(credentials),
    });

    saveAuthData(data);
    router.push("/dashboard");
  };

  const logout = async () => {
    try {
      await fetchApi('/auth/logout', {
        method: 'POST'
      });
    } catch { }
    finally {
      localStorage.removeItem('token');

      setToken(null);
      setUser(null);

      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        register,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
