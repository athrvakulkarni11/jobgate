 import Sidebar from "./components/Sidebar";

export default function HomePage() {
  return (
    <main className="flex w-full">
      <Sidebar />
      <div className="p-6 flex-1">
        <h1 className="text-2xl font-bold mb-4">Welcome to My Next.js App</h1>
        <p>This is the main content area.</p>
      </div>
    </main>
  );
}
