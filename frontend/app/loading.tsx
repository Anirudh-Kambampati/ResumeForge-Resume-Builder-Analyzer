import ForgeLoader from "@/components/ui/ForgeLoader";

export default function Loading() {
  return (
    <main className="flex h-dvh items-center justify-center bg-app">
      <ForgeLoader label="Warming up the forge…" />
    </main>
  );
}
