// app/components/Sidebar.jsx
const Sidebar = () => {
    return (
      <aside className="bg-gray-100 w-64 p-4 h-screen">
        <h2 className="text-lg font-bold mb-4">Sidebar Menu</h2>
        <ul className="space-y-2">
          <li><a href="/" className="hover:underline">Dashboard</a></li>
          <li><a href="/settings" className="hover:underline">Settings</a></li>
          <li><a href="/profile" className="hover:underline">Profile</a></li>
        </ul>
      </aside>
    );
  };
  
  export default Sidebar;
  