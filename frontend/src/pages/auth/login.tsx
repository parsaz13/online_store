import { useForm } from "react-hook-form";
import { LoginRequestData } from "@/types";
import { storeTokens } from "@/hooks/useAuth";
import { LogoTypeIcon } from "@/icons/logo-type";
import InputWithLabel from "@/components/ui/input-with-label";
import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router";
import { useLogin } from "@/api/auth/auth.hooks";

export default function Login() {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequestData>();
  const loginMutation = useLogin({
    onSuccess(data) {
      storeTokens(data.access, data.refresh);
      navigate("/");
    },
  });

  const onSubmit = (data: LoginRequestData) => {
    loginMutation.mutate(data);
  };

  return (
    <div className="mx-auto mt-10 max-w-sm p-2">
      <a href="/">
        <LogoTypeIcon className="h-16 w-full" />
      </a>
      <p className="my-10 text-center">ورود | ثبت نام</p>

      {loginMutation.isError && (
        <div className="mb-4 rounded-md bg-red-200 p-2 text-sm text-red-900">
          خطا در ورود
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <InputWithLabel
          className="w-full"
          label="نام کاربری"
          id="username"
          {...register("username", { required: "نام کاربری الزامی است" })}
          error={errors.username?.message}
        />
        <InputWithLabel
          type="password"
          label="کلمه عبور"
          id="password"
          {...register("password", { required: "کلمه عبور الزامی است" })}
          error={errors.password?.message}
        />

        <p className="my-6 text-center text-xs">
          ورود و عضویت شما به منزله پذیرفتن قوانین و مقررات می باشد.
        </p>

        <Button
          type="submit"
          className="w-full"
          variant="default"
          disabled={loginMutation.isPending}
        >
          ورود به سایت
        </Button>
      </form>

      <Button className="mt-6 w-full" variant="link" asChild>
        <Link to="/auth/register">ثبت نام در سایت</Link>
      </Button>
    </div>
  );
}
