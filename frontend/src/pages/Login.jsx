import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
const API_URL =
  import.meta.env.VITE_API_URL;

export default function Login() {

  const navigate = useNavigate();

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleLogin = async () => {

    const response = await fetch(
      `${API_URL}/api/login/`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      }
    );

    const data = await response.json();

    console.log("RESPONSE:", data);

    if (data.success) {

      localStorage.setItem(
        "token",
        data.access
      );

      localStorage.setItem(
        "username",
        username
      );
      window.location.replace("/dashboard");


    } else {

      alert(
        data.message
      );

    }

  };

  return (

    <div className="min-h-screen bg-[#07070a] flex items-center justify-center px-6">

      <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-purple-700 opacity-20 blur-[180px]" />

      <div className="relative z-10 w-full max-w-md">

        <div className="bg-[#111113]/90 backdrop-blur-xl border border-zinc-800 rounded-3xl p-10 shadow-2xl">

          <div className="text-center">

            <h1 className="text-5xl font-black bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">
              ClipForge
            </h1>

            <p className="text-zinc-400 mt-4">
              Transform YouTube videos into viral AI-powered shorts
            </p>

          </div>

          <div className="mt-10 space-y-4">

            <input
              placeholder="Username"
              value={username}
              onChange={(e) =>
                setUsername(
                  e.target.value
                )
              }
              className="w-full bg-[#1a1a1d] border border-zinc-700 rounded-2xl px-5 py-4 outline-none focus:border-purple-500"
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) =>
                setPassword(
                  e.target.value
                )
              }
              className="w-full bg-[#1a1a1d] border border-zinc-700 rounded-2xl px-5 py-4 outline-none focus:border-purple-500"
            />

            <button
              onClick={handleLogin}
              className="w-full bg-purple-600 hover:bg-purple-500 transition-all py-4 rounded-2xl font-semibold"
            >
              Login
            </button>

          </div>

          <div className="text-center mt-8">

            <span className="text-zinc-500">
              Don't have an account?
            </span>

            <Link
              to="/register"
              className="text-purple-400 hover:text-purple-300 ml-2"
            >
              Register
            </Link>

          </div>

        </div>

      </div>

    </div>

  );
}