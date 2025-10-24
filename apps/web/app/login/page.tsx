"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Page() {
  const r = useRouter();
  const [email, setEmail] = useState(""); 
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/auth/login", {
      method: "POST",
      credentials: "include",               // send/receive session cookie
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) { setErr("Invalid credentials"); return; }
    r.push("/dashboard");
  }

  return (
    // <main className="min-h-dvh grid place-items-center p-6">
    //   <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 border rounded-xl p-6">
    //     <h1 className="text-2xl font-semibold">Sign in</h1>
    //     <input className="w-full rounded border p-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
    //     <input className="w-full rounded border p-2" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
    //     {err && <p className="text-sm text-red-600">{err}</p>}
    //     <button className="w-full rounded bg-black text-white p-2">Sign in</button>
    //   </form>
    // </main>
        <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
          <div className="sm:mx-auto sm:w-full sm:max-w-sm">
            <img src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500" alt="Your Company" className="mx-auto h-10 w-auto" />
            <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-white">Sign in to your account</h2>
          </div>
          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form action="#" method="POST" className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm/6 font-medium text-gray-100">Email address</label>
                <div className="mt-2">
                  <input id="email" type="email" name="email" required autoComplete="email" className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <label htmlFor="password" className="block text-sm/6 font-medium text-gray-100">Password</label>
                  <div className="text-sm">
                    <a href="#" className="font-semibold text-indigo-400 hover:text-indigo-300">Forgot password?</a>
                  </div>
                </div>
                <div className="mt-2">
                  <input id="password" type="password" name="password" required autoComplete="current-password" className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
                </div>
              </div>

              <div>
                <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">Sign in</button>
              </div>
            </form>

            <p className="mt-10 text-center text-sm/6 text-gray-400">
              Not a member?
              <a href="#" className="font-semibold text-indigo-400 hover:text-indigo-300">Start a 14 day free trial</a>
            </p>
          </div>
        </div>
  );
}
