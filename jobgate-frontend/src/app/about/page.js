import Home from '../components/Home';
import Sidebar from "../components/Sidebar";

export default function HomePage() {
  return (
    <main className="flex w-full">
      <Sidebar />
      <div className="p-6 flex-1">
        <Home />
      </div>
    </main>
  );
}

