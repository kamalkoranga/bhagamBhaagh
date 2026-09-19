export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface UserOut {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
  user: UserOut;
}

export interface ProfileOut {
  id: string;
  name: string;
  email: string;
  created_at: string;
}
