import { useMutation, useQueryClient } from "@tanstack/react-query";

import { login, register } from "./auth.api";
import { MutationOptionsFromFn } from "@/types";
import { MY_USER_KEY } from "@/api/myuser/myuser.hooks";

// Login hook
export function useLogin(options?: MutationOptionsFromFn<typeof login>) {
  const queryClient = useQueryClient();
  return useMutation({
    ...options,
    mutationFn: login,
    onSettled(...args) {
      queryClient.invalidateQueries({ queryKey: [MY_USER_KEY] });
      options?.onSettled?.(...args);
    },
  });
}

// Register hook
export function useRegister(options?: MutationOptionsFromFn<typeof register>) {
  const queryClient = useQueryClient();
  return useMutation({
    ...options,
    mutationFn: register,
    onSettled(...args) {
      queryClient.invalidateQueries({ queryKey: [MY_USER_KEY] });
      options?.onSettled?.(...args);
    },
  });
}
