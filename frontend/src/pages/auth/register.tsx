import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { RegisterRequestData } from "@/types";
import { Button } from "@/components/ui/button";
import InputWithLabel from "@/components/ui/input-with-label";
import { LogoTypeIcon } from "@/icons/logo-type";
import { Link } from "react-router";
import { useRegister } from "@/api/auth/auth.hooks";

export default function Register() {
  const navigate = useNavigate();

  const {
    register: formRegister,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterRequestData>();

  const registerMutation = useRegister({
    onSuccess: () => {
      navigate("/auth/login");
    },
  });

  const onSubmit = (data: RegisterRequestData) => {
    registerMutation.mutate(data);
  };

  return (
    <div className="mx-auto mt-10 max-w-sm p-2">
      <a href="/">
        <LogoTypeIcon className="h-16 w-full" />
      </a>
      <p className="my-10 text-center">ورود | ثبت نام</p>

      {registerMutation.isError && (
        <div className="mb-4 rounded-md bg-red-200 p-2 text-sm text-red-900">
          ثبت نام ناموفق بود
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <InputWithLabel
          className="w-full"
          id="username"
          label="نام کاربری"
          {...formRegister("username", { required: "نام کاربری الزامی است" })}
          error={errors.username?.message}
        />
        <InputWithLabel
          className="w-full"
          id="email"
          type="email"
          label="ایمیل"
          {...formRegister("email", {
            required: "ایمیل الزامی است",
            pattern: {
              value: /^\S+@\S+$/i,
              message: "فرمت ایمیل معتبر نیست",
            },
          })}
          error={errors.email?.message}
        />
        <InputWithLabel
          id="password"
          type="password"
          label="کلمه عبور"
          {...formRegister("password", { required: "کلمه عبور الزامی است" })}
          error={errors.password?.message}
        />
        <InputWithLabel
          id="password2"
          type="password"
          label="تکرار کلمه عبور"
          {...formRegister("password2", {
            required: "تکرار کلمه عبور الزامی است",
            validate: (val) =>
              val === watch("password") || "کلمه عبور یکسان نیست",
          })}
          error={errors.password2?.message}
        />

        <p className="my-6 text-center text-xs">
          ورود و عضویت شما به منزله پذیرفتن قوانین و مقررات می باشد.
        </p>

        <Button
          className="w-full"
          variant="default"
          type="submit"
          disabled={registerMutation.isPending}
        >
          ثبت نام
        </Button>
      </form>

      <Button className="mt-6 w-full" variant="link" asChild>
        <Link to="/auth/login">ورود</Link>
      </Button>
    </div>
  );
}
