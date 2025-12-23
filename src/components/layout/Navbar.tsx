"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { clsx } from 'clsx';
import { LayoutDashboard, Swords, BookOpen, Tag, Server, Cpu, Gamepad2 } from 'lucide-react';

const navItems = [
    { href: "/", label: "DASHBOARD", icon: LayoutDashboard },
    { href: "/library", label: "LIBRARY", icon: Gamepad2 },
    { href: "/backlog", label: "OPTIMIZER", icon: Swords },
    { href: "/recommendations", label: "DISCOVERY", icon: BookOpen },
    { href: "/deals", label: "DEALS", icon: Tag },
    { href: "/servers", label: "SERVERS", icon: Server },
    { href: "/specs", label: "PC SPECS", icon: Cpu },
];

export function Navbar() {
    const pathname = usePathname();

    return (
        <header className="fixed top-0 left-0 right-0 z-50 border-b border-white/5" style={{
            background: 'linear-gradient(to bottom, rgba(0,0,0,0.95), rgba(0,0,0,0.8))',
            backdropFilter: 'blur(20px)'
        }}>
            <div className="max-w-7xl mx-auto px-6">
                <div className="flex items-center justify-between py-4">
                    {/* Logo */}
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-red-600 rounded flex items-center justify-center">
                            <Gamepad2 size={24} className="text-white" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-display font-bold tracking-wider text-red-600">
                                PHANTOM DECK
                            </h1>
                            <p className="text-[10px] text-gray-500 uppercase tracking-widest">
                                Your Ultimate Game Companion
                            </p>
                        </div>
                    </div>

                    {/* Navigation */}
                    <nav className="flex items-center gap-1">
                        {navItems.map((item) => {
                            const isActive = pathname === item.href;
                            const Icon = item.icon;

                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={clsx(
                                        "flex items-center gap-2 px-4 py-2 text-xs font-bold tracking-wider transition-all rounded",
                                        isActive
                                            ? "bg-red-600 text-white"
                                            : "text-gray-400 hover:text-white hover:bg-white/5"
                                    )}
                                >
                                    <Icon size={16} />
                                    {item.label}
                                </Link>
                            );
                        })}
                    </nav>
                </div>
            </div>
        </header>
    );
}
