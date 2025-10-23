import { cookies, headers } from "next/headers";

export default async function Page() {
  // forward browser cookies to the API
  const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/auth/me", {
    method: "GET",
    headers: {
      cookie: cookies().toString(),
      // if you proxy via same origin later, you won’t need manual cookie plumbing
    },
    cache: "no-store",
  });

  if (!res.ok) {
    // Not logged in: show a link to /login
    return (
      <main className="p-6">
        <a className="underline" href="/login">Please sign in</a>
      </main>
    );
  }

  const data = await res.json();

  const tasks = await fetch(process.env.NEXT_PUBLIC_API_URL + "/tasks", {
    headers: { cookie: cookies().toString() }, cache: "no-store"
  }).then(r => r.json());

  return (
    <main className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Welcome {data.user.email}</h1>
      <ul className="list-disc pl-6">
        {tasks.items.map((t: string) => <li key={t}>{t}</li>)}
      </ul>
      <form action={process.env.NEXT_PUBLIC_API_URL + "/auth/logout"} method="post">
        <button className="rounded border px-4 py-2">Logout</button>
      </form>
    </main>
  );
}
