import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";

export default function AppLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Navbar />
      <div className="flex flex-1 overflow-hidden h-[calc(100vh-64px)]">
        <Sidebar />
        <div className="flex-1 overflow-y-auto relative bg-surface">
          {children}
        </div>
      </div>
    </>
  );
}
