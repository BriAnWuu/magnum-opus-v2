import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import "./globals.css";

const roboto = Roboto({
    weight: ["400", "500", "700"],
    style: ["normal", "italic"],
    subsets: ["latin"],
    display: "swap",
    variable: "--font-roboto",
    fallback: ["system-ui", "arial"],
});

export const metadata: Metadata = {
    title: {
        template: "%s | Magnum Opus",
        default: "Magnum Opus",
    },
    description: "",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body>{children}</body>
        </html>
    );
}
