"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { clsx } from 'clsx';
import {
    Library, // New icon
    LayoutDashboard, // New icon
    Compass, // New icon
    Sparkles,
    Settings // Keep Settings for now, though not used in navItems, it might be used elsewhere or removed later.
} from 'lucide-react';

const links = [
    { href: "/library", label: "My Library", icon: Library },
    { href: "/backlog", label: "Optimizer", icon: LayoutDashboard },
    { href: "/recommendations", label: "Discovery", icon: Compass },
    { href: "/assistant", label: "Session AI", icon: Sparkles },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="w-64 h-screen bg-sidebar border-r border-sidebar-border flex flex-col fixed left-0 top-0 shadow-2xl z-50">
            <div className="p-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-tr from-persona-red to-persona-neon rounded-lg shadow-lg shadow-persona-red/20"></div>
                <h1 className="text-2xl font-display font-bold tracking-wider text-sidebar-foreground">
                    SESSION<span className="text-persona-red">.</span>
                </h1>
            </div>

            <nav className="flex-1 px-4 space-y-2 mt-4">
                {links.map((link) => {
                    const isActive = pathname === link.href;
                    const Icon = link.icon;

                    return (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={clsx(
                                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 group relative overflow-hidden",
                                isActive
                                    ? "bg-sidebar-accent text-sidebar-primary-foreground font-medium shadow-md border-l-4 border-persona-red"
                                    : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground hover:pl-5"
                            )}
                        >
                            {isActive && (
                                <div className="absolute inset-0 bg-gradient-to-r from-persona-red/10 to-transparent opacity-50" />
                            )}
                            <Icon size={20} className={clsx("transition-colors", isActive ? "text-persona-red" : "group-hover:text-persona-red")} />
                            <span className="relative z-10">{link.label}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-sidebar-border">
                <div className="bg-sidebar-accent/50 p-4 rounded-xl border border-sidebar-border/50">
                    <div className="text-xs font-bold text-sidebar-foreground/50 uppercase tracking-widest mb-2">System Status</div>
                    <div className="flex items-center gap-2 text-sm text-green-400">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        Online
                    </div>
                </div>
            </div>
        </div>
    );
}
