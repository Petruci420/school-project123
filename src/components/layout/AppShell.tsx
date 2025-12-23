import { Navbar } from "./Navbar";

export function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-background text-foreground font-body">
            <Navbar />
            <main className="pt-20 pb-12">
                <div className="max-w-7xl mx-auto px-6">
                    {children}
                </div>
            </main>
        </div>
    );
}
