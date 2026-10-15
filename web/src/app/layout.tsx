import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Synthetic User Simulation Engine | Behavioral Economics & Discrete Choice Modeling",
  description: "A mathematically grounded synthetic user simulation engine backed by McFadden's Discrete Choice Model, Kahneman-Tversky Prospect Theory, and Demographic Post-Stratification.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className={`${geistSans.variable} ${geistMono.variable} min-h-full bg-[#FBFBFA] text-stone-900 flex flex-col font-sans antialiased selection:bg-stone-200 selection:text-stone-900`}>
        {children}
      </body>
    </html>
  );
}
