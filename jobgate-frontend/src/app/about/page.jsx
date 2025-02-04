import Sidebar from "../components/Sidebar";
import DynamicPage from './DynamicPage';  

export default function HomePage() {
  return (
    <main className="flex w-full">
      <Sidebar />
      <div className="p-6 flex-1">
<h2>inside about</h2>
<h2>inside about</h2>
<DynamicPage />
      </div>  
    </main>
  );
}

