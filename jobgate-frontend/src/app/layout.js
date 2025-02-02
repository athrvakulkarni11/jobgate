// app/layout.js
import Navbar from "./components/Navbar";
import "./globals.css";

export const metadata = {
  title: "My Next.js App",
  description: "An example project with reusable components",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="flex">
        <Navbar />
        <div className="flex w-full">
          {children}
        </div>
      </body>
    </html>
  );
}
