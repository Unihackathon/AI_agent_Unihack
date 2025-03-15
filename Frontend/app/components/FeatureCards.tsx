"use client"; 

export default function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 border border-[#333] rounded-2xl hover:border-[#00FF00] transition-all duration-200">
      <h3 className="text-xl text-[#00FF00] mb-3 font-semibold">{title}</h3>
      <p>{description}</p>
    </div>
  );
}
