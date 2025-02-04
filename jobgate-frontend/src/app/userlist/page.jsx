// src/app/page.js
import UserList from "../components/UserList";
import Counter from "../components/Counter";
export default function HomePage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome to the User Dashboard</h1>
      <UserList />
      <Counter />
    </div>
  );
}
