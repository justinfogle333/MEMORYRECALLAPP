import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, AlertTriangle, XCircle, ChevronRight, ChevronLeft, Truck, Building, MapPin, Star, Shield, Zap } from "lucide-react";

// ─── IMAGE ASSETS (CDN) ───────────────────────────────────────────────────────
const IMG_BANNER = "/manus-storage/hero_web_banner_2c270395.png";
const IMG_NORMAL = "/manus-storage/hero_normal_move_15142225.png";
const IMG_EXPERT = "/manus-storage/hero_expert_move_d01529e3.png";
const IMG_TRUCK  = "/manus-storage/truck_diagram_9ed6a4d7.png";

// ─── TYPES ────────────────────────────────────────────────────────────────────
type FormData = {
  // General
  clientName: string;
  clientEmail: string;
  clientPhone: string;
  moveDate: string;
  // Pick-Up
  puAddress: string;
  puCity: string;
  puState: string;
  puZip: string;
  puUnit: string;
  puBuildingType: string;
  puTruckAccess: string;
  puDrivewayIssues: string;
  puClearanceIssues: string;
  puParkingRestrictions: string;
  puLongCarry: string;
  puStairsExt: string;
  puStairsInt: string;
  puElevator: string;
  puElevatorReservable: string;
  puElevatorHours: string;
  puHoisting: string;
  puCoi: string;
  puCoiContact: string;
  // Delivery
  delAddress: string;
  delCity: string;
  delState: string;
  delZip: string;
  delUnit: string;
  delBuildingType: string;
  delTruckAccess: string;
  delDrivewayIssues: string;
  delClearanceIssues: string;
  delParkingRestrictions: string;
  delLongCarry: string;
  delStairsExt: string;
  delStairsInt: string;
  delElevator: string;
  delElevatorReservable: string;
  delElevatorHours: string;
  delHoisting: string;
  delCoi: string;
  delCoiContact: string;
  // Service
  puSemiAccess: string;
  delSemiAccess: string;
  loadPreference: string;
  deliveryDeadline: string;
  specialtyItems: string;
  additionalNotes: string;
};

const INITIAL_FORM: FormData = {
  clientName: "", clientEmail: "", clientPhone: "", moveDate: "",
  puAddress: "", puCity: "", puState: "", puZip: "", puUnit: "", puBuildingType: "",
  puTruckAccess: "", puDrivewayIssues: "", puClearanceIssues: "", puParkingRestrictions: "",
  puLongCarry: "", puStairsExt: "", puStairsInt: "", puElevator: "", puElevatorReservable: "",
  puElevatorHours: "", puHoisting: "", puCoi: "", puCoiContact: "",
  delAddress: "", delCity: "", delState: "", delZip: "", delUnit: "", delBuildingType: "",
  delTruckAccess: "", delDrivewayIssues: "", delClearanceIssues: "", delParkingRestrictions: "",
  delLongCarry: "", delStairsExt: "", delStairsInt: "", delElevator: "", delElevatorReservable: "",
  delElevatorHours: "", delHoisting: "", delCoi: "", delCoiContact: "",
  puSemiAccess: "", delSemiAccess: "", loadPreference: "", deliveryDeadline: "",
  specialtyItems: "", additionalNotes: "",
};

// ─── DIFFICULTY LEVELS ────────────────────────────────────────────────────────
const LEVELS = [
  {
    level: 1,
    title: "Standard Access",
    color: "#00ff88",
    borderColor: "rgba(0,255,136,0.4)",
    bgColor: "rgba(0,255,136,0.06)",
    badge: "level-badge-green",
    image: IMG_NORMAL,
    description: "The baseline move. Truck parks in driveway, 10ft or less to door, no stairs, no restrictions.",
    factors: [
      "Truck parks in driveway (46ft+ space clear)",
      "Walk to door: 10 feet or less",
      "No exterior or interior stairs",
      "No elevator required",
      "No parking permits or restrictions",
      "No COI required",
      "No oversized items",
    ],
  },
  {
    level: 3,
    title: "Moderate Access",
    color: "#ffc800",
    borderColor: "rgba(255,200,0,0.4)",
    bgColor: "rgba(255,200,0,0.06)",
    badge: "level-badge-yellow",
    image: null,
    description: "Common complications that require additional planning, crew time, and equipment.",
    factors: [
      "1–2 flights of stairs (exterior or interior)",
      "Long carry: 50–150 feet from truck to door",
      "Steep or narrow driveway",
      "Elevator access with reserved hours",
      "Street parking only — no driveway",
      "Low-hanging branches or overhead wires",
      "Gated community entry",
    ],
  },
  {
    level: 5,
    title: "Expert Access",
    color: "#ff3c00",
    borderColor: "rgba(255,60,0,0.4)",
    bgColor: "rgba(255,60,0,0.06)",
    badge: "level-badge-red",
    image: IMG_EXPERT,
    description: "Maximum complexity. Requires specialized planning, extra crew, and specialized equipment.",
    factors: [
      "3+ flights of stairs",
      "Long carry exceeding 150 feet",
      "Elevator required with strict reservation windows",
      "Parking permit required from city or municipality",
      "COI required by building management",
      "Hoisting required for oversized items",
      "Shuttle truck required — no semi access",
      "Multiple trucks required for large volume",
    ],
  },
];

// ─── STEP CONFIG ──────────────────────────────────────────────────────────────
const STEPS = [
  { id: 0, label: "Overview", icon: Star },
  { id: 1, label: "Your Info", icon: Shield },
  { id: 2, label: "Pick-Up", icon: MapPin },
  { id: 3, label: "Delivery", icon: MapPin },
  { id: 4, label: "Service", icon: Zap },
  { id: 5, label: "Review", icon: CheckCircle },
];

// ─── HELPERS ──────────────────────────────────────────────────────────────────
function Input({ label, name, value, onChange, placeholder = "", type = "text", required = false }: {
  label: string; name: string; value: string; onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string; type?: string; required?: boolean;
}) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium tracking-widest uppercase" style={{ color: "rgba(0,229,255,0.7)" }}>
        {label}{required && <span className="text-red-400 ml-1">*</span>}
      </label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="form-input rounded px-3 py-2 text-sm w-full"
      />
    </div>
  );
}

function Select({ label, name, value, onChange, options, required = false }: {
  label: string; name: string; value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  options: { value: string; label: string }[]; required?: boolean;
}) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium tracking-widest uppercase" style={{ color: "rgba(0,229,255,0.7)" }}>
        {label}{required && <span className="text-red-400 ml-1">*</span>}
      </label>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="form-input rounded px-3 py-2 text-sm w-full"
        style={{ background: "rgba(0,229,255,0.04)" }}
      >
        <option value="">— Select —</option>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-3 mb-6">
      <div className="h-px flex-1" style={{ background: "rgba(0,229,255,0.2)" }} />
      <span className="text-xs font-bold tracking-widest uppercase" style={{ color: "#00e5ff" }}>{children}</span>
      <div className="h-px flex-1" style={{ background: "rgba(0,229,255,0.2)" }} />
    </div>
  );
}

const YES_NO = [{ value: "yes", label: "Yes" }, { value: "no", label: "No" }, { value: "unsure", label: "Unsure" }];
const BUILDING_TYPES = [
  { value: "single_family", label: "Single Family Home" },
  { value: "apartment", label: "Apartment" },
  { value: "condo", label: "Condo" },
  { value: "townhome", label: "Townhome" },
  { value: "high_rise", label: "High-Rise" },
  { value: "storage", label: "Storage Unit" },
  { value: "other", label: "Other" },
];
const TRUCK_ACCESS = [
  { value: "clear_46ft", label: "Yes — 46ft+ clear space available" },
  { value: "clear_multi", label: "Yes — Space for multiple trucks / semi" },
  { value: "restricted", label: "No — Restricted / Street parking only" },
  { value: "unsure", label: "Unsure" },
];
const LOAD_OPTIONS = [
  { value: "live_load", label: "Live Load / Direct Load (Semi at my door)" },
  { value: "branch_load", label: "Branch Load (Warehouse transfer)" },
  { value: "shuttle", label: "Semi + Shuttle Hybrid" },
  { value: "no_preference", label: "No Preference — Show me all pricing options" },
];

// ─── MAIN COMPONENT ───────────────────────────────────────────────────────────
export default function Home() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<FormData>(INITIAL_FORM);
  const [submitted, setSubmitted] = useState(false);
  const [activeLevelIdx, setActiveLevelIdx] = useState(0);
  const topRef = useRef<HTMLDivElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const next = () => {
    setStep(s => Math.min(s + 1, STEPS.length - 1));
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  const prev = () => {
    setStep(s => Math.max(s - 1, 0));
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = () => {
    setSubmitted(true);
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Auto-cycle levels on overview
  useEffect(() => {
    if (step !== 0) return;
    const t = setInterval(() => setActiveLevelIdx(i => (i + 1) % LEVELS.length), 4000);
    return () => clearInterval(t);
  }, [step]);

  return (
    <div className="min-h-screen grid-bg" style={{ background: "#080d1a", fontFamily: "'Space Grotesk', sans-serif" }}>
      {/* Scan line effect */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="scan-line absolute inset-0 w-full h-32" />
      </div>

      {/* ── HERO BANNER ── */}
      <div ref={topRef} className="relative w-full" style={{ height: "520px", overflow: "hidden" }}>
        <img src={IMG_BANNER} alt="Move Intelligence System" className="w-full h-full object-cover" style={{ objectPosition: "center center" }} />
        <div className="absolute inset-0" style={{ background: "linear-gradient(to bottom, rgba(8,13,26,0.3) 0%, rgba(8,13,26,0.85) 100%)" }} />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
            <div className="text-xs font-bold tracking-widest mb-4" style={{ color: "#00e5ff", letterSpacing: "0.3em" }}>
              [COMPANY NAME] PRESENTS
            </div>
            <h1 className="font-bold mb-4" style={{ fontSize: "clamp(2rem, 6vw, 4rem)", color: "#ffffff", letterSpacing: "-0.02em", lineHeight: 1.1 }}>
              MOVE INTELLIGENCE<br />
              <span style={{ color: "#00e5ff" }}>SYSTEM</span>
            </h1>
            <p className="text-lg mb-8 max-w-2xl mx-auto" style={{ color: "rgba(255,255,255,0.7)" }}>
              The industry's most advanced logistics intake process.<br />
              Tell us about your move. We handle the rest.
            </p>
            {step === 0 && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.97 }}
                onClick={next}
                className="px-10 py-4 font-bold text-sm tracking-widest uppercase rounded"
                style={{ background: "linear-gradient(135deg, #00e5ff, #0080ff)", color: "#080d1a", letterSpacing: "0.15em" }}
              >
                BEGIN LOGISTICS INTAKE →
              </motion.button>
            )}
          </motion.div>
        </div>
      </div>

      {/* ── PROGRESS BAR ── */}
      {step > 0 && !submitted && (
        <div className="sticky top-0 z-50 py-4 px-4" style={{ background: "rgba(8,13,26,0.95)", borderBottom: "1px solid rgba(0,229,255,0.1)", backdropFilter: "blur(10px)" }}>
          <div className="max-w-4xl mx-auto flex items-center justify-between gap-2">
            {STEPS.slice(1).map((s, i) => {
              const realIdx = i + 1;
              const done = step > realIdx;
              const active = step === realIdx;
              return (
                <div key={s.id} className="flex items-center gap-2 flex-1">
                  <div className="flex flex-col items-center gap-1">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300 ${active ? "progress-step-active text-black" : done ? "progress-step-done text-cyan-300" : "progress-step-pending text-white/30"}`}>
                      {done ? "✓" : realIdx}
                    </div>
                    <span className="text-xs hidden sm:block" style={{ color: active ? "#00e5ff" : "rgba(255,255,255,0.3)", fontSize: "10px" }}>{s.label}</span>
                  </div>
                  {i < STEPS.length - 2 && <div className="h-px flex-1" style={{ background: done ? "rgba(0,229,255,0.4)" : "rgba(255,255,255,0.08)" }} />}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── MAIN CONTENT ── */}
      <div className="max-w-5xl mx-auto px-4 py-12 relative z-10">
        <AnimatePresence mode="wait">

          {/* ── STEP 0: OVERVIEW ── */}
          {step === 0 && (
            <motion.div key="step0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              {/* Truck Diagram */}
              <div className="mb-16">
                <div className="text-center mb-8">
                  <div className="text-xs font-bold tracking-widest mb-2" style={{ color: "#00e5ff", letterSpacing: "0.3em" }}>TRUCK ACCESS REQUIREMENTS</div>
                  <h2 className="text-3xl font-bold text-white">Know Before You Move</h2>
                </div>
                <div className="hud-border rounded-xl overflow-hidden">
                  <img src={IMG_TRUCK} alt="Truck Dimensions" className="w-full" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
                  {[
                    { label: "26ft Box Truck", value: "46 FT MIN", sub: "36ft bumper-to-bumper + 10ft ramp" },
                    { label: "Semi-Trailer", value: "80 FT MIN", sub: "70ft bumper-to-bumper + 10ft ramp" },
                    { label: "Multiple Trucks", value: "46 FT EACH", sub: "Per truck, side-by-side or sequential" },
                  ].map(item => (
                    <div key={item.label} className="hud-border rounded-lg p-5 text-center">
                      <div className="text-xs tracking-widest mb-1" style={{ color: "rgba(0,229,255,0.6)" }}>{item.label}</div>
                      <div className="text-2xl font-bold mb-1" style={{ color: "#00e5ff" }}>{item.value}</div>
                      <div className="text-xs" style={{ color: "rgba(255,255,255,0.4)" }}>{item.sub}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Difficulty Levels */}
              <div className="mb-16">
                <div className="text-center mb-8">
                  <div className="text-xs font-bold tracking-widest mb-2" style={{ color: "#00e5ff", letterSpacing: "0.3em" }}>ACCESS DIFFICULTY LEVELS</div>
                  <h2 className="text-3xl font-bold text-white">Every Move is Different</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {LEVELS.map((lvl, idx) => (
                    <motion.div
                      key={lvl.level}
                      className="rounded-xl overflow-hidden cursor-pointer"
                      style={{ border: `1px solid ${lvl.borderColor}`, background: lvl.bgColor, transition: "all 0.3s ease" }}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => setActiveLevelIdx(idx)}
                    >
                      {lvl.image && (
                        <div className="relative" style={{ height: "180px", overflow: "hidden" }}>
                          <img src={lvl.image} alt={lvl.title} className="w-full h-full object-cover" />
                          <div className="absolute inset-0" style={{ background: `linear-gradient(to top, ${lvl.bgColor} 0%, transparent 60%)` }} />
                        </div>
                      )}
                      {!lvl.image && (
                        <div className="flex items-center justify-center" style={{ height: "180px", background: lvl.bgColor }}>
                          <div className="text-6xl font-bold" style={{ color: lvl.color, opacity: 0.3 }}>L{lvl.level}</div>
                        </div>
                      )}
                      <div className="p-5">
                        <div className="flex items-center gap-2 mb-3">
                          <span className={`${lvl.badge} text-xs font-bold px-3 py-1 rounded-full`}>LEVEL {lvl.level}</span>
                          <span className="font-bold text-white">{lvl.title}</span>
                        </div>
                        <p className="text-sm mb-4" style={{ color: "rgba(255,255,255,0.6)" }}>{lvl.description}</p>
                        <ul className="space-y-1">
                          {lvl.factors.slice(0, 4).map(f => (
                            <li key={f} className="flex items-start gap-2 text-xs" style={{ color: "rgba(255,255,255,0.5)" }}>
                              <span style={{ color: lvl.color, marginTop: "2px", flexShrink: 0 }}>›</span>
                              {f}
                            </li>
                          ))}
                          {lvl.factors.length > 4 && (
                            <li className="text-xs" style={{ color: lvl.color }}>+{lvl.factors.length - 4} more factors...</li>
                          )}
                        </ul>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Service Options */}
              <div className="mb-16">
                <div className="text-center mb-8">
                  <div className="text-xs font-bold tracking-widest mb-2" style={{ color: "#00e5ff", letterSpacing: "0.3em" }}>SERVICE STRUCTURES</div>
                  <h2 className="text-3xl font-bold text-white">Two Options. Multiple Price Points.</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {[
                    { icon: "🚛", title: "Live Load", sub: "Direct Load", desc: "Semi-trailer loads directly at your home. Fewest handling touchpoints. Most efficient for large moves.", tag: "SEMI ACCESS REQUIRED" },
                    { icon: "🏭", title: "Branch Load", sub: "Warehouse Transfer", desc: "Box trucks transport to our warehouse, then loaded onto semi for long-distance. Ideal for restricted access.", tag: "NO SEMI NEEDED" },
                    { icon: "🔄", title: "Semi + Shuttle", sub: "Hybrid Service", desc: "Shuttle truck transfers goods between your home and a semi staged nearby. Maximum flexibility.", tag: "FLEXIBLE ACCESS" },
                  ].map(opt => (
                    <div key={opt.title} className="hud-border rounded-xl p-6">
                      <div className="text-3xl mb-3">{opt.icon}</div>
                      <div className="text-xs tracking-widest mb-1" style={{ color: "#00e5ff" }}>{opt.tag}</div>
                      <div className="text-lg font-bold text-white mb-1">{opt.title}</div>
                      <div className="text-sm mb-3" style={{ color: "rgba(0,229,255,0.6)" }}>{opt.sub}</div>
                      <p className="text-sm" style={{ color: "rgba(255,255,255,0.55)" }}>{opt.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* CTA */}
              <div className="text-center">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={next}
                  className="px-12 py-5 font-bold text-base tracking-widest uppercase rounded-lg"
                  style={{ background: "linear-gradient(135deg, #00e5ff, #0080ff)", color: "#080d1a", letterSpacing: "0.15em" }}
                >
                  START MY LOGISTICS INTAKE →
                </motion.button>
                <p className="mt-4 text-sm" style={{ color: "rgba(255,255,255,0.35)" }}>Takes approximately 5 minutes. No wrong answers.</p>
              </div>
            </motion.div>
          )}

          {/* ── STEP 1: CLIENT INFO ── */}
          {step === 1 && (
            <motion.div key="step1" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
              <div className="hud-border rounded-2xl p-8">
                <SectionTitle>Client Information</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Input label="Full Name" name="clientName" value={form.clientName} onChange={handleChange} placeholder="John Smith" required />
                  <Input label="Email Address" name="clientEmail" value={form.clientEmail} onChange={handleChange} placeholder="john@email.com" type="email" required />
                  <Input label="Phone Number" name="clientPhone" value={form.clientPhone} onChange={handleChange} placeholder="(555) 000-0000" type="tel" />
                  <Input label="Desired Move Date" name="moveDate" value={form.moveDate} onChange={handleChange} type="date" />
                </div>
              </div>
            </motion.div>
          )}

          {/* ── STEP 2: PICK-UP ── */}
          {step === 2 && (
            <motion.div key="step2" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
              <div className="mb-6 rounded-xl overflow-hidden hud-border">
                <img src={IMG_NORMAL} alt="Pick-Up Location" className="w-full" style={{ maxHeight: "220px", objectFit: "cover" }} />
              </div>
              <div className="hud-border rounded-2xl p-8 space-y-8">
                <SectionTitle>Pick-Up Location — General</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div className="sm:col-span-2">
                    <Input label="Street Address" name="puAddress" value={form.puAddress} onChange={handleChange} placeholder="123 Main Street" required />
                  </div>
                  <Input label="City" name="puCity" value={form.puCity} onChange={handleChange} placeholder="Los Angeles" required />
                  <Input label="State" name="puState" value={form.puState} onChange={handleChange} placeholder="CA" />
                  <Input label="Zip Code" name="puZip" value={form.puZip} onChange={handleChange} placeholder="90001" />
                  <Input label="Apt / Unit #" name="puUnit" value={form.puUnit} onChange={handleChange} placeholder="Unit 4B" />
                  <div className="sm:col-span-2">
                    <Select label="Type of Building" name="puBuildingType" value={form.puBuildingType} onChange={handleChange} options={BUILDING_TYPES} required />
                  </div>
                </div>

                <SectionTitle>Pick-Up — Truck Access & Parking</SectionTitle>
                <div className="hud-border rounded-lg p-4 mb-4" style={{ background: "rgba(0,229,255,0.04)" }}>
                  <p className="text-xs" style={{ color: "rgba(0,229,255,0.8)" }}>
                    ⚡ Our 26ft box truck requires <strong style={{ color: "#00e5ff" }}>46 feet minimum</strong> of continuous, unobstructed space (36ft bumper-to-bumper + 10ft ramp). Large moves may require multiple trucks or a semi-trailer (80ft minimum).
                  </p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Select label="Can our truck access your location?" name="puTruckAccess" value={form.puTruckAccess} onChange={handleChange} options={TRUCK_ACCESS} required />
                  <Select label="Driveway issues? (steep, narrow, unpaved, shared)" name="puDrivewayIssues" value={form.puDrivewayIssues} onChange={handleChange} options={YES_NO} />
                  <Select label="Clearance obstacles? (branches, gates, wires, low bridges)" name="puClearanceIssues" value={form.puClearanceIssues} onChange={handleChange} options={YES_NO} />
                  <Select label="Parking restrictions or permit required?" name="puParkingRestrictions" value={form.puParkingRestrictions} onChange={handleChange} options={YES_NO} />
                  <div className="sm:col-span-2">
                    <Input label="Distance from truck to front door (if not at driveway)" name="puLongCarry" value={form.puLongCarry} onChange={handleChange} placeholder="e.g. 50 ft, 100 ft, N/A" />
                  </div>
                </div>

                <SectionTitle>Pick-Up — Stairs, Elevators & Hoisting</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Input label="Flights of stairs OUTSIDE (1 flight = ~10-12 steps)" name="puStairsExt" value={form.puStairsExt} onChange={handleChange} placeholder="0, 1, 2, 3..." />
                  <Input label="Flights of stairs INSIDE" name="puStairsInt" value={form.puStairsInt} onChange={handleChange} placeholder="0, 1, 2, 3..." />
                  <Select label="Elevator on site?" name="puElevator" value={form.puElevator} onChange={handleChange} options={YES_NO} />
                  {form.puElevator === "yes" && <>
                    <Select label="Can elevator be reserved for moving?" name="puElevatorReservable" value={form.puElevatorReservable} onChange={handleChange} options={YES_NO} />
                    <div className="sm:col-span-2">
                      <Input label="Elevator allowed hours & interior dimensions (H x W x D)" name="puElevatorHours" value={form.puElevatorHours} onChange={handleChange} placeholder="e.g. 8am-6pm | 7ft x 4ft x 5ft" />
                    </div>
                  </>}
                  <div className="sm:col-span-2">
                    <Select label="Hoisting needed? (oversized items that won't fit through doors/stairs)" name="puHoisting" value={form.puHoisting} onChange={handleChange} options={YES_NO} />
                  </div>
                </div>

                <SectionTitle>Pick-Up — Building Requirements</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Select label="Certificate of Insurance (COI) required?" name="puCoi" value={form.puCoi} onChange={handleChange} options={YES_NO} />
                  {form.puCoi === "yes" && (
                    <div className="sm:col-span-2">
                      <Input label="Building Manager Name / Phone / Email" name="puCoiContact" value={form.puCoiContact} onChange={handleChange} placeholder="Jane Doe / (555) 000-0000 / jane@building.com" />
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}

          {/* ── STEP 3: DELIVERY ── */}
          {step === 3 && (
            <motion.div key="step3" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
              <div className="mb-6 rounded-xl overflow-hidden hud-border">
                <img src={IMG_EXPERT} alt="Delivery Location" className="w-full" style={{ maxHeight: "220px", objectFit: "cover" }} />
              </div>
              <div className="hud-border rounded-2xl p-8 space-y-8">
                <SectionTitle>Delivery Location — General</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div className="sm:col-span-2">
                    <Input label="Street Address" name="delAddress" value={form.delAddress} onChange={handleChange} placeholder="456 New Street" required />
                  </div>
                  <Input label="City" name="delCity" value={form.delCity} onChange={handleChange} placeholder="New York" required />
                  <Input label="State" name="delState" value={form.delState} onChange={handleChange} placeholder="NY" />
                  <Input label="Zip Code" name="delZip" value={form.delZip} onChange={handleChange} placeholder="10001" />
                  <Input label="Apt / Unit #" name="delUnit" value={form.delUnit} onChange={handleChange} placeholder="Apt 12C" />
                  <div className="sm:col-span-2">
                    <Select label="Type of Building" name="delBuildingType" value={form.delBuildingType} onChange={handleChange} options={BUILDING_TYPES} required />
                  </div>
                </div>

                <SectionTitle>Delivery — Truck Access & Parking</SectionTitle>
                <div className="hud-border rounded-lg p-4 mb-4" style={{ background: "rgba(0,229,255,0.04)" }}>
                  <p className="text-xs" style={{ color: "rgba(0,229,255,0.8)" }}>
                    ⚡ Our 26ft box truck requires <strong style={{ color: "#00e5ff" }}>46 feet minimum</strong> of continuous, unobstructed space (36ft bumper-to-bumper + 10ft ramp). Large moves may require multiple trucks or a semi-trailer (80ft minimum).
                  </p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Select label="Can our truck access your location?" name="delTruckAccess" value={form.delTruckAccess} onChange={handleChange} options={TRUCK_ACCESS} required />
                  <Select label="Driveway issues? (steep, narrow, unpaved, shared)" name="delDrivewayIssues" value={form.delDrivewayIssues} onChange={handleChange} options={YES_NO} />
                  <Select label="Clearance obstacles? (branches, gates, wires, low bridges)" name="delClearanceIssues" value={form.delClearanceIssues} onChange={handleChange} options={YES_NO} />
                  <Select label="Parking restrictions or permit required?" name="delParkingRestrictions" value={form.delParkingRestrictions} onChange={handleChange} options={YES_NO} />
                  <div className="sm:col-span-2">
                    <Input label="Distance from truck to front door (if not at driveway)" name="delLongCarry" value={form.delLongCarry} onChange={handleChange} placeholder="e.g. 50 ft, 100 ft, N/A" />
                  </div>
                </div>

                <SectionTitle>Delivery — Stairs, Elevators & Hoisting</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Input label="Flights of stairs OUTSIDE (1 flight = ~10-12 steps)" name="delStairsExt" value={form.delStairsExt} onChange={handleChange} placeholder="0, 1, 2, 3..." />
                  <Input label="Flights of stairs INSIDE" name="delStairsInt" value={form.delStairsInt} onChange={handleChange} placeholder="0, 1, 2, 3..." />
                  <Select label="Elevator on site?" name="delElevator" value={form.delElevator} onChange={handleChange} options={YES_NO} />
                  {form.delElevator === "yes" && <>
                    <Select label="Can elevator be reserved for moving?" name="delElevatorReservable" value={form.delElevatorReservable} onChange={handleChange} options={YES_NO} />
                    <div className="sm:col-span-2">
                      <Input label="Elevator allowed hours & interior dimensions (H x W x D)" name="delElevatorHours" value={form.delElevatorHours} onChange={handleChange} placeholder="e.g. 8am-6pm | 7ft x 4ft x 5ft" />
                    </div>
                  </>}
                  <div className="sm:col-span-2">
                    <Select label="Hoisting needed? (oversized items that won't fit through doors/stairs)" name="delHoisting" value={form.delHoisting} onChange={handleChange} options={YES_NO} />
                  </div>
                </div>

                <SectionTitle>Delivery — Building Requirements</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Select label="Certificate of Insurance (COI) required?" name="delCoi" value={form.delCoi} onChange={handleChange} options={YES_NO} />
                  {form.delCoi === "yes" && (
                    <div className="sm:col-span-2">
                      <Input label="Building Manager Name / Phone / Email" name="delCoiContact" value={form.delCoiContact} onChange={handleChange} placeholder="Jane Doe / (555) 000-0000 / jane@building.com" />
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}

          {/* ── STEP 4: SERVICE OPTIONS ── */}
          {step === 4 && (
            <motion.div key="step4" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
              <div className="hud-border rounded-2xl p-8 space-y-8">
                <SectionTitle>Service Structure & Preferences</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <Select label="Can a semi-trailer access your PICK-UP location?" name="puSemiAccess" value={form.puSemiAccess} onChange={handleChange} options={YES_NO} />
                  <Select label="Can a semi-trailer access your DELIVERY location?" name="delSemiAccess" value={form.delSemiAccess} onChange={handleChange} options={YES_NO} />
                  <div className="sm:col-span-2">
                    <Select label="Service preference (or show me all pricing options)" name="loadPreference" value={form.loadPreference} onChange={handleChange} options={LOAD_OPTIONS} />
                  </div>
                  <div className="sm:col-span-2">
                    <Input label="Hard delivery deadline or specific timing requirements?" name="deliveryDeadline" value={form.deliveryDeadline} onChange={handleChange} placeholder="e.g. Must be delivered by Aug 15, flexible, etc." />
                  </div>
                </div>

                <SectionTitle>Specialty Items & Additional Details</SectionTitle>
                <div className="grid grid-cols-1 gap-5">
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-medium tracking-widest uppercase" style={{ color: "rgba(0,229,255,0.7)" }}>
                      Specialty / Heavy Items (Piano, gun safe, pool table, hot tub, gym equipment, large artwork)
                    </label>
                    <textarea
                      name="specialtyItems"
                      value={form.specialtyItems}
                      onChange={handleChange}
                      rows={3}
                      placeholder="List any specialty items here..."
                      className="form-input rounded px-3 py-2 text-sm w-full resize-none"
                    />
                  </div>
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-medium tracking-widest uppercase" style={{ color: "rgba(0,229,255,0.7)" }}>
                      Anything else we should know? (Construction, HOA rules, gated entry, narrow hallways, low ceilings, etc.)
                    </label>
                    <textarea
                      name="additionalNotes"
                      value={form.additionalNotes}
                      onChange={handleChange}
                      rows={4}
                      placeholder="Any additional details that could affect the move..."
                      className="form-input rounded px-3 py-2 text-sm w-full resize-none"
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* ── STEP 5: REVIEW ── */}
          {step === 5 && !submitted && (
            <motion.div key="step5" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
              <div className="hud-border rounded-2xl p-8">
                <SectionTitle>Review Your Submission</SectionTitle>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
                  {[
                    { title: "Client Info", fields: [["Name", form.clientName], ["Email", form.clientEmail], ["Phone", form.clientPhone], ["Move Date", form.moveDate]] },
                    { title: "Pick-Up", fields: [["Address", form.puAddress], ["City/State", `${form.puCity}, ${form.puState}`], ["Building", form.puBuildingType], ["Truck Access", form.puTruckAccess], ["Stairs Ext/Int", `${form.puStairsExt || "0"} / ${form.puStairsInt || "0"}`], ["Elevator", form.puElevator]] },
                    { title: "Delivery", fields: [["Address", form.delAddress], ["City/State", `${form.delCity}, ${form.delState}`], ["Building", form.delBuildingType], ["Truck Access", form.delTruckAccess], ["Stairs Ext/Int", `${form.delStairsExt || "0"} / ${form.delStairsInt || "0"}`], ["Elevator", form.delElevator]] },
                    { title: "Service", fields: [["Load Preference", form.loadPreference], ["PU Semi Access", form.puSemiAccess], ["Del Semi Access", form.delSemiAccess], ["Deadline", form.deliveryDeadline]] },
                  ].map(section => (
                    <div key={section.title} className="hud-border rounded-xl p-5">
                      <div className="text-xs font-bold tracking-widest mb-4" style={{ color: "#00e5ff" }}>{section.title.toUpperCase()}</div>
                      <div className="space-y-2">
                        {section.fields.map(([k, v]) => (
                          <div key={k} className="flex justify-between gap-2 text-sm">
                            <span style={{ color: "rgba(255,255,255,0.4)" }}>{k}</span>
                            <span className="text-right font-medium text-white">{v || "—"}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                {form.specialtyItems && (
                  <div className="hud-border rounded-xl p-5 mb-4">
                    <div className="text-xs font-bold tracking-widest mb-2" style={{ color: "#00e5ff" }}>SPECIALTY ITEMS</div>
                    <p className="text-sm text-white">{form.specialtyItems}</p>
                  </div>
                )}
                {form.additionalNotes && (
                  <div className="hud-border rounded-xl p-5 mb-4">
                    <div className="text-xs font-bold tracking-widest mb-2" style={{ color: "#00e5ff" }}>ADDITIONAL NOTES</div>
                    <p className="text-sm text-white">{form.additionalNotes}</p>
                  </div>
                )}
                <div className="text-center mt-8">
                  <motion.button
                    whileHover={{ scale: 1.04 }}
                    whileTap={{ scale: 0.97 }}
                    onClick={handleSubmit}
                    className="px-12 py-4 font-bold text-sm tracking-widest uppercase rounded-lg"
                    style={{ background: "linear-gradient(135deg, #00e5ff, #0080ff)", color: "#080d1a", letterSpacing: "0.15em" }}
                  >
                    SUBMIT LOGISTICS INTAKE ✓
                  </motion.button>
                </div>
              </div>
            </motion.div>
          )}

          {/* ── SUBMITTED ── */}
          {submitted && (
            <motion.div key="submitted" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-20">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
                className="w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-8"
                style={{ background: "rgba(0,229,255,0.1)", border: "2px solid #00e5ff", boxShadow: "0 0 40px rgba(0,229,255,0.3)" }}
              >
                <CheckCircle size={48} style={{ color: "#00e5ff" }} />
              </motion.div>
              <h2 className="text-4xl font-bold text-white mb-4">Intake Complete</h2>
              <p className="text-lg mb-2" style={{ color: "#00e5ff" }}>Thank you, {form.clientName || "valued client"}.</p>
              <p className="text-base mb-8 max-w-lg mx-auto" style={{ color: "rgba(255,255,255,0.55)" }}>
                Our logistics team will review your submission and prepare multiple pricing options tailored to your exact access conditions and service preferences. Expect to hear from us shortly.
              </p>
              <div className="hud-border rounded-xl p-6 max-w-md mx-auto">
                <div className="text-xs tracking-widest mb-4" style={{ color: "#00e5ff" }}>WHAT HAPPENS NEXT</div>
                {["Logistics team reviews your intake", "Pricing options prepared for your conditions", "Quote delivered to your email", "Move confirmed and crew assigned"].map((item, i) => (
                  <div key={item} className="flex items-center gap-3 mb-3 text-sm text-left">
                    <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0" style={{ background: "rgba(0,229,255,0.15)", color: "#00e5ff", border: "1px solid rgba(0,229,255,0.3)" }}>{i + 1}</div>
                    <span style={{ color: "rgba(255,255,255,0.7)" }}>{item}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

        </AnimatePresence>

        {/* ── NAV BUTTONS ── */}
        {step > 0 && !submitted && (
          <div className="flex justify-between items-center mt-10">
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={prev}
              className="flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-medium"
              style={{ border: "1px solid rgba(0,229,255,0.25)", color: "rgba(0,229,255,0.8)", background: "rgba(0,229,255,0.04)" }}
            >
              <ChevronLeft size={16} /> BACK
            </motion.button>
            {step < STEPS.length - 1 && (
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={next}
                className="flex items-center gap-2 px-8 py-3 rounded-lg text-sm font-bold tracking-widest"
                style={{ background: "linear-gradient(135deg, #00e5ff, #0080ff)", color: "#080d1a" }}
              >
                NEXT <ChevronRight size={16} />
              </motion.button>
            )}
          </div>
        )}
      </div>

      {/* ── FOOTER ── */}
      <footer className="mt-20 py-8 text-center" style={{ borderTop: "1px solid rgba(0,229,255,0.08)" }}>
        <p className="text-xs" style={{ color: "rgba(255,255,255,0.2)", letterSpacing: "0.2em" }}>
          [COMPANY NAME] · MOVE INTELLIGENCE SYSTEM · POWERED BY PRECISION
        </p>
      </footer>
    </div>
  );
}
