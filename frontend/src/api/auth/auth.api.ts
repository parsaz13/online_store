import {
  LoginRequestData,
  LoginResponseData,
  RegisterRequestData,
  RegisterResponseData,
} from "@/types";
import baseApi, { baseURL } from "../base";
import axios from "axios";

export async function login(data: LoginRequestData) {
  const res = await axios.post<LoginResponseData>(
    baseURL + "accounts/login/",
    data,
  );
  return res.data;
}

export async function register(data: RegisterRequestData) {
  const res = await axios.post<RegisterResponseData>(
    baseURL + "accounts/register/",
    data,
  );
  return res.data;
}

export async function refreshToken(data: { refresh: string }) {
  const res = await baseApi.post<{ access: string; refresh: string }>(
    "/accounts/token/refresh/",
    data,
  );
  return res.data;
}
