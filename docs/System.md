import { useState, useRef, useEffect } from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

// ─── OJT TEMPLATES ────────────────────────────────────────────────────────────
const TEMPLATES = [
  {
    id: "t1",
    name: "OJT Endorsement Letter",
    category: "Pre-OJT",
    fields: ["studentName", "studentId", "course", "company", "companyAddress", "supervisor", "startDate", "endDate", "hoursRequired", "coordinator"],
    content: `Republic of the Philippines
[University / College Name]
Office of Practicum and OJT Affairs

Date: [Current Date]

{{supervisor}}
[Company / Organization Name]
{{companyAddress}}

Dear {{supervisor}},

We are pleased to endorse {{studentName}}, a bona fide student of this institution currently enrolled in {{course}}, with Student ID {{studentId}}, to undergo On-the-Job Training (OJT) at your esteemed company from {{startDate}} to {{endDate}}.

The student is required to complete a minimum of {{hoursRequired}} training hours as part of the academic requirements of the program.

We trust that you will extend your full support and guidance to our student throughout the duration of the training. Should you have any concerns, please do not hesitate to contact the undersigned.

Thank you for this opportunity.

Sincerely,

{{coordinator}}
OJT / Practicum Coordinator`,
  },
  {
    id: "t2",
    name: "OJT Completion Certificate Request",
    category: "Post-OJT",
    fields: ["studentName", "studentId", "course", "company", "supervisor", "startDate", "endDate", "hoursRendered", "coordinator"],
    content: `CERTIFICATE OF OJT COMPLETION REQUEST

Date: [Current Date]

TO: {{coordinator}}
       OJT / Practicum Coordinator

FROM: {{studentName}}
         Student ID: {{studentId}}
         Course: {{course}}

SUBJECT: Request for Issuance of Certificate of Completion

I am writing to formally request the issuance of my Certificate of OJT Completion.

I have successfully completed my On-the-Job Training at {{company}} under the supervision of {{supervisor}}, from {{startDate}} to {{endDate}}, rendering a total of {{hoursRendered}} training hours.

I hereby submit all required post-OJT documents for your evaluation and request the processing of my completion certificate at your earliest convenience.

Respectfully,
{{studentName}}
{{studentId}}`,
  },
  {
    id: "t3",
    name: "OJT Extension Request",
    category: "During OJT",
    fields: ["studentName", "studentId", "course", "company", "supervisor", "originalEndDate", "newEndDate", "reason", "coordinator"],
    content: `REQUEST FOR OJT EXTENSION

Date: [Current Date]

{{coordinator}}
OJT / Practicum Coordinator
[Department Name]

Dear {{coordinator}},

I, {{studentName}} (Student ID: {{studentId}}), a student of {{course}}, respectfully request an extension of my On-the-Job Training period at {{company}} under {{supervisor}}.

My original training period was set to end on {{originalEndDate}}. However, due to the following reason:

{{reason}}

I am requesting that my OJT period be extended up to {{newEndDate}} to fulfill the required number of training hours and meet the program's academic requirements.

I assure you of my continued diligence and commitment throughout the extended training period.

Respectfully yours,
{{studentName}}
Student ID: {{studentId}}`,
  },
  {
    id: "t4",
    name: "Company Acceptance / MOA Request",
    category: "Pre-OJT",
    fields: ["studentName", "studentId", "course", "company", "companyAddress", "supervisor", "startDate", "endDate", "hoursRequired", "coordinator"],
    content: `MEMORANDUM OF AGREEMENT
On-the-Job Training

This Memorandum of Agreement (MOA) is entered into by and between:

THE TRAINING ESTABLISHMENT:
{{company}}
{{companyAddress}}
Hereinafter referred to as the "Company," represented by {{supervisor}};

— AND —

THE ACADEMIC INSTITUTION:
[University / College Name]
Hereinafter referred to as the "School," represented by {{coordinator}};

WHEREAS, the School requires its students enrolled in {{course}} to undergo On-the-Job Training as part of the academic curriculum;

WHEREAS, the Company is willing to accept {{studentName}} (Student ID: {{studentId}}) as a trainee from {{startDate}} to {{endDate}} for a minimum of {{hoursRequired}} training hours;

NOW THEREFORE, both parties agree to the terms and conditions set forth in this agreement.

Signed this day at [City], Philippines.

_______________________          _______________________
{{supervisor}}                            {{coordinator}}
Company Representative              OJT Coordinator`,
  },
  {
    id: "t5",
    name: "OJT Excuse / Absence Letter",
    category: "During OJT",
    fields: ["studentName", "studentId", "course", "company", "supervisor", "absenceDate", "reason", "returnDate"],
    content: `EXCUSE LETTER FOR OJT ABSENCE

Date: [Current Date]

{{supervisor}}
[Company / Organization Name]

Dear {{supervisor}},

I, {{studentName}} (Student ID: {{studentId}}), currently undergoing OJT at your company as part of my {{course}} program, am writing to formally inform you of my absence on {{absenceDate}}.

The reason for my absence is as follows:
{{reason}}

I assure you that I will resume my duties on {{returnDate}} and will make up for any missed hours as required.

I sincerely apologize for any inconvenience this may have caused and thank you for your understanding.

Respectfully,
{{studentName}}
OJT Trainee — {{course}}`,
  },
];

const INITIAL_REQUESTS = [
  {
    id: "ojt-001", studentName: "Ana Reyes", studentId: "2022-0041", course: "BS Information Technology",
    templateName: "OJT Endorsement Letter", category: "Pre-OJT", status: "pending", urgent: true,
    submittedAt: "2026-03-07T09:30:00",
    speechText: "I need an endorsement letter for my OJT at TechCorp Manila, my supervisor is Ms. Dela Cruz, starting April 1 to June 30, 500 hours required",
    processedText: "I am requesting an endorsement letter for my On-the-Job Training at TechCorp Manila under the supervision of Ms. Dela Cruz, scheduled from April 1 to June 30 with a required total of 500 training hours.",
    filledDocument: `<div style="text-align: center;"><p><strong>Republic of the Philippines</strong></p><p><strong>[University / College Name]</strong></p><p>Office of Practicum and OJT Affairs</p></div><br/><p style="text-align: right;">Date: March 7, 2026</p><br/><p><strong>Ms. Dela Cruz</strong></p><p>TechCorp Manila</p><p>123 Ayala Ave, Makati City</p><br/><p>Dear Ms. Dela Cruz,</p><br/><p>We are pleased to endorse <strong>Ana Reyes</strong>, a bona fide student currently enrolled in BS Information Technology, with Student ID 2022-0041, to undergo On-the-Job Training (OJT) at TechCorp Manila from April 1, 2026 to June 30, 2026.</p><br/><p>The student is required to complete a minimum of 500 training hours.</p><br/><p>Sincerely,</p><br/><br/><p style="text-align: right;"><strong>Prof. Santos</strong></p><p style="text-align: right;">OJT / Practicum Coordinator</p>`,
  },
  {
    id: "ojt-002", studentName: "Carlo Mendoza", studentId: "2021-0088", course: "BS Accountancy",
    templateName: "OJT Completion Certificate Request", category: "Post-OJT", status: "approved", urgent: false,
    submittedAt: "2026-03-06T14:00:00",
    speechText: "I finished my OJT at BDO Unibank, 600 hours, from January to March under Sir Ramos",
    processedText: "I have successfully completed my On-the-Job Training at BDO Unibank under the supervision of Sir Ramos, rendering a total of 600 training hours from January to March 2026.",
    filledDocument: `<div style="text-align: center;"><p><strong>CERTIFICATE OF OJT COMPLETION REQUEST</strong></p></div><br/><p style="text-align: right;">Date: March 6, 2026</p><br/><p>TO: <strong>Prof. Santos</strong></p><p>OJT / Practicum Coordinator</p><br/><p>FROM: <strong>Carlo Mendoza</strong></p><p>Student ID: 2021-0088</p><p>Course: BS Accountancy</p><br/><p>SUBJECT: Request for Issuance of Certificate of Completion</p><br/><p>I have successfully completed my OJT at BDO Unibank under the supervision of Mr. Ramos from January to March 2026, rendering 600 training hours.</p><br/><p>Respectfully,</p><br/><br/><p style="text-align: right;"><strong>Carlo Mendoza</strong></p><p style="text-align: right;">2021-0088</p>`,
  },
];

const COORDINATORS = ["Prof. Santos", "Dr. Lim", "Prof. Reyes", "Dr. Bautista"];

// ─── API ──────────────────────────────────────────────────────────────────────
async function callAI(prompt, system = "", onChunk) {
  try {
    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ system: system || "You help process OJT document text.", prompt }),
    });
    if (!res.ok) throw new Error("Local AI server error.");
    
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let text = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      text += chunk;
      if (onChunk) onChunk(text);
    }
    return text;
  } catch (err) {
    console.error(err);
    throw new Error("AI server unavailable. Please ensure the backend is running.");
  }
}

// ─── UTILS ────────────────────────────────────────────────────────────────────
const fmtDate = (iso) => new Date(iso).toLocaleString("en-PH", { dateStyle: "medium", timeStyle: "short" });
const uid = () => "ojt-" + Math.random().toString(36).slice(2, 7).toUpperCase();

const toRichText = (text) => {
  if (!text) return "";
  if (text.includes("</p>")) return text; // already HTML
  return text.split("\n\n").map(p => `<p>${p.split("\n").join("<br/>")}</p>`).join("");
};

const CAT_COLORS = { "Pre-OJT": "#4f8ef7", "During OJT": "#e9c46a", "Post-OJT": "#2a9d8f" };
const STATUS_MAP = {
  pending:  { color: "#e9c46a", bg: "#e9c46a18", label: "Pending" },
  approved: { color: "#2a9d8f", bg: "#2a9d8f18", label: "Approved" },
  rejected: { color: "#e74c3c", bg: "#e74c3c18", label: "Rejected" },
};

// --- QUILL CONFIG ---
const Size = ReactQuill.Quill.import('attributors/style/size');
Size.whitelist = ['10px', '12px', '14px', '16px', '18px', '20px', '24px'];
ReactQuill.Quill.register(Size, true);

const QUILL_MODULES = {
  toolbar: [
    [{ 'header': [1, 2, 3, false] }],
    [{ 'size': ['10px', '12px', '14px', '16px', '18px', '20px', '24px'] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
    [{ 'align': [] }],
    ['clean']
  ],
};

// ─── MAIN ─────────────────────────────────────────────────────────────────────
export default function App() {
  const [role, setRole] = useState(null);
  const [requests, setRequests] = useState(INITIAL_REQUESTS);
  const [notifications, setNotifications] = useState([
    { id: 1, msg: "🚨 Urgent OJT endorsement request from Ana Reyes", time: "9:31 AM", read: false, type: "urgent" },
    { id: 2, msg: "OJT Completion for Carlo Mendoza approved", time: "2:20 PM", read: true, type: "approved" },
  ]);

  const addRequest = (req) => {
    setRequests(p => [req, ...p]);
    setNotifications(p => [{ id: Date.now(), msg: req.urgent ? `🚨 URGENT OJT request from ${req.studentName}` : `New OJT request from ${req.studentName}`, time: new Date().toLocaleTimeString("en-PH", { timeStyle: "short" }), read: false, type: req.urgent ? "urgent" : "new" }, ...p]);
  };
  const updateRequest = (id, changes) => setRequests(p => p.map(r => r.id === id ? { ...r, ...changes } : r));

  if (!role) return <RoleSelect onSelect={setRole} />;
  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif", minHeight: "100vh", background: "#0c0e14" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Serif+Display:ital@0;1&display=swap');
        *{box-sizing:border-box;margin:0;padding:0;}
        ::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:#13151f}::-webkit-scrollbar-thumb{background:#4f8ef7;border-radius:3px}
        .btn{cursor:pointer;border:none;outline:none;transition:all .2s;}.btn:active{transform:scale(.97)}
        .slide-in{animation:sIn .35s ease}@keyframes sIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
        .fade-in{animation:fIn .3s ease}@keyframes fIn{from{opacity:0}to{opacity:1}}
        .pulse{animation:pulse 1.8s infinite}@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(231,76,60,.35)}60%{box-shadow:0 0 0 10px rgba(231,76,60,0)}}
        .card{background:#13151f;border:1px solid #1e2130;border-radius:16px;overflow:hidden;box-shadow: 0 12px 32px rgba(0,0,0,0.4);transition: transform 0.3s ease, box-shadow 0.3s ease;}
        .card:hover{transform: translateY(-4px); box-shadow: 0 20px 48px rgba(0,0,0,0.5);}
        .inp{background:#1a1d2a;color:#dde2f0;border:1px solid #252840;border-radius:9px;padding:10px 14px;font-family:'DM Sans',sans-serif;font-size:14px;outline:none;transition:border-color .2s, box-shadow 0.2s;width:100%}
        .inp:focus{border-color:#4f8ef7; box-shadow: 0 0 0 3px rgba(79,142,247,0.15);}
        textarea.inp{resize:vertical}
        .tag{display:inline-flex;align-items:center;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:.4px; backdrop-filter: blur(4px);}
        .notif-dot{position:absolute;top:-2px;right:-2px;width:8px;height:8px;background:#e74c3c;border-radius:50%;border:2px solid #0c0e14}
        .step-num{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
        .hover-row{transition:background .15s, transform 0.15s;cursor:pointer}
        .hover-row:hover{background:#1a1d2a!important; transform: translateX(4px);}
        select.inp option{background:#1a1d2a}
        @keyframes shimmer{0%{background-position:-468px 0}100%{background-position:468px 0}}
        .ql-toolbar{background: rgba(26, 29, 42, 0.8)!important; backdrop-filter: blur(12px); border-color:#252840!important; border-top-left-radius:9px; border-top-right-radius:9px; position: sticky; top: 0; z-index: 10;}
        .ql-container{border-color:#252840!important;border-bottom-left-radius:9px;border-bottom-right-radius:9px;background:#13151f;color:#dde2f0;font-family:'DM Sans',sans-serif!important;font-size:14px!important;}
        .ql-editor{min-height:200px;padding:20px!important;}
        .ql-editor p{margin-bottom:16px!important;line-height:1.8;}
        .ql-stroke{stroke:#6b7590!important}.ql-fill{fill:#6b7590!important}.ql-picker{color:#6b7590!important}
        .ql-picker.ql-size .ql-picker-label::before { content: 'Numbering fonting'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="10px"]::before { content: '10px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="12px"]::before { content: '12px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="14px"]::before { content: '14px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="16px"]::before { content: '16px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="18px"]::before { content: '18px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="20px"]::before { content: '20px'!important; }
        .ql-picker.ql-size .ql-picker-label[data-value="24px"]::before { content: '24px'!important; }
        .ql-picker.ql-size .ql-picker-item::before { content: attr(data-value)!important; }
        .ql-picker.ql-size { width: 140px!important; }

        /* --- MOBILE RESPONSIVENESS --- */
        @media (max-width: 768px) {
          .card{border-radius:12px;}
          .top-bar-text { display: none; }
          .role-select-container { padding: 16px!important; }
          .role-card-group { flex-direction: column!important; width: 100%!important; align-items: center; }
          .rc { width: 100%!important; max-width: 320px; }
          .student-grid { grid-template-columns: 1fr!important; }
          .coordinator-layout { grid-template-columns: 1fr!important; }
          .stats-grid { grid-template-columns: 1fr 1fr!important; }
          .admin-tabs { gap: 4px!important; overflow-x: auto; white-space: nowrap; padding-bottom: 8px; }
          .admin-tabs button { padding: 6px 12px!important; font-size: 12px!important; }
          .template-grid { grid-template-columns: 1fr!important; }
          .job-details-modal { width: 95%!important; padding: 16px!important; }
          .step-progress { display: none!important; } /* Hide complex progress on mobile */
          .mobile-step-indicator { display: block!important; text-align: center; margin-bottom: 16px; color: #4f8ef7; font-weight: 700; font-size: 14px; }
          .inp-group { flex-direction: column!important; }
          .inp-group > * { width: 100%!important; }
          .suggestion-tag { padding: 4px 10px!important; font-size: 11px!important; }
        }
        .mobile-step-indicator { display: none; }
      `}</style>
      {role === "student"     && <StudentView     requests={requests} addRequest={addRequest} onLogout={() => setRole(null)} notifications={notifications} setNotifications={setNotifications} />}
      {role === "coordinator" && <CoordinatorView requests={requests} updateRequest={updateRequest} notifications={notifications} setNotifications={setNotifications} onLogout={() => setRole(null)} />}
      {role === "admin"       && <AdminView       requests={requests} updateRequest={updateRequest} notifications={notifications} setNotifications={setNotifications} onLogout={() => setRole(null)} />}
    </div>
  );
}

// ─── ROLE SELECT ─────────────────────────────────────────────────────────────
function RoleSelect({ onSelect }) {
  return (
    <div style={{ minHeight: "100vh", background: "#0c0e14", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');*{box-sizing:border-box;margin:0;padding:0}.rc{cursor:pointer;background:#13151f;border:1px solid #1e2130;border-radius:20px;padding:32px 28px;width:230px;text-align:center;transition:all .3s}.rc:hover{transform:translateY(-5px);border-color:#4f8ef7;box-shadow:0 16px 48px rgba(79,142,247,.1)}`}</style>

      {/* Logo */}
      <div style={{ textAlign: "center", marginBottom: 52 }}>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
          <div style={{ width: 44, height: 44, background: "linear-gradient(135deg,#4f8ef7,#2a5ccc)", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/></svg>
          </div>
          <div>
            <div style={{ fontFamily: "'DM Sans',sans-serif", fontWeight: 700, fontSize: 20, color: "#dde2f0", letterSpacing: -.3 }}>OJT DocAssist</div>
            <div style={{ fontSize: 11, color: "#4f8ef7", fontWeight: 600, letterSpacing: 1.2, textTransform: "uppercase" }}>AI-Powered Document System</div>
          </div>
        </div>
        <p style={{ color: "#4b5472", fontSize: 14, fontStyle: "italic" }}>Streamlining OJT document requests through speech & AI</p>
      </div>

      <div style={{ display: "flex", gap: 18, flexWrap: "wrap", justifyContent: "center" }} className="role-card-group">
        {[
          { key: "student",     label: "OJT Student",   desc: "Submit and track your OJT document requests",     icon: "M12 2a5 5 0 1 0 0 10 5 5 0 0 0 0-10zM2 20a10 10 0 0 1 20 0", color: "#4f8ef7",  sub: "Trainee" },
          { key: "coordinator", label: "Coordinator",   desc: "Review and process OJT document submissions",     icon: "M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11", color: "#e9c46a", sub: "Faculty" },
          { key: "admin",       label: "Admin",         desc: "Full system control and final document approval", icon: "M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z", color: "#e76f51",  sub: "Office" },
        ].map(({ key, label, desc, icon, color, sub }) => (
          <div key={key} className="rc" onClick={() => onSelect(key)}>
            <div style={{ width: 60, height: 60, background: `${color}18`, border: `1.5px solid ${color}30`, borderRadius: 14, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d={icon}/></svg>
            </div>
            <div style={{ fontFamily: "'DM Sans',sans-serif", fontWeight: 700, fontSize: 16, color: "#dde2f0", marginBottom: 4 }}>{label}</div>
            <div style={{ fontSize: 11, color, fontWeight: 600, marginBottom: 10, textTransform: "uppercase", letterSpacing: .8 }}>{sub}</div>
            <div style={{ fontSize: 12.5, color: "#4b5472", lineHeight: 1.5 }}>{desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── TOP BAR ─────────────────────────────────────────────────────────────────
function TopBar({ roleLabel, roleColor, notifications, setNotifications, onLogout }) {
  const [open, setOpen] = useState(false);
  const unread = notifications.filter(n => !n.read).length;
  return (
    <div style={{ background: "#0f1118", borderBottom: "1px solid #1e2130", padding: "11px 24px", display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, zIndex: 100 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ width: 30, height: 30, background: "linear-gradient(135deg,#4f8ef7,#2a5ccc)", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>
        </div>
        <span style={{ fontWeight: 700, fontSize: 15, color: "#dde2f0" }}>OJT DocAssist</span>
        <span style={{ background: `${roleColor}18`, color: roleColor, padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: .8 }}>{roleLabel}</span>
      </div>
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <div style={{ position: "relative" }}>
          <button className="btn" onClick={() => { setOpen(!open); setNotifications(p => p.map(n => ({ ...n, read: true }))); }}
            style={{ background: "transparent", padding: 8, borderRadius: 8, color: "#6b7590", display: "flex", position: "relative" }}>
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            {unread > 0 && <span className="notif-dot" />}
          </button>
          {open && (
            <div className="fade-in" style={{ position: "absolute", right: 0, top: 42, width: 310, background: "#13151f", border: "1px solid #1e2130", borderRadius: 14, boxShadow: "0 20px 60px rgba(0,0,0,.5)", zIndex: 200, overflow: "hidden" }}>
              <div style={{ padding: "12px 16px", borderBottom: "1px solid #1e2130", fontWeight: 600, fontSize: 13, color: "#dde2f0" }}>Notifications</div>
              {notifications.length === 0
                ? <div style={{ padding: "18px 16px", color: "#4b5472", fontSize: 13 }}>No notifications</div>
                : notifications.map(n => (
                  <div key={n.id} style={{ padding: "11px 16px", borderBottom: "1px solid #0f1118", display: "flex", gap: 10 }}>
                    <div style={{ width: 7, height: 7, borderRadius: "50%", background: n.type === "urgent" ? "#e74c3c" : n.type === "approved" ? "#2a9d8f" : "#4f8ef7", marginTop: 5, flexShrink: 0 }} />
                    <div>
                      <div style={{ fontSize: 13, color: "#b0b8d4", lineHeight: 1.4 }}>{n.msg}</div>
                      <div style={{ fontSize: 11, color: "#3a4060", marginTop: 2 }}>{n.time}</div>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
        <button className="btn" onClick={onLogout}
          style={{ display: "flex", alignItems: "center", gap: 6, background: "#1a1d2a", border: "1px solid #252840", color: "#6b7590", padding: "7px 14px", borderRadius: 8, fontSize: 12.5, fontWeight: 500 }}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/></svg>
          Switch Role
        </button>
      </div>
    </div>
  );
}

// ─── STUDENT VIEW ─────────────────────────────────────────────────────────────
function StudentView({ requests, addRequest, onLogout, notifications, setNotifications }) {
  const [tab, setTab] = useState("new");
  const [myReqs, setMyReqs]     = useState(INITIAL_REQUESTS);
  const [speech, setSpeech]     = useState("");
  const [recording, setRec]     = useState(false);
  const [processed, setProc]    = useState("");
  const [aiLoading, setAiLoad]  = useState(false);
  const [template, setTemplate] = useState(null);
  const [filled, setFilled]     = useState("");
  const [filling, setFilling]   = useState(false);
  const [urgent, setUrgent]     = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [step, setStep]         = useState(1);
  const recRef = useRef(null);

  const STUDENT = { name: "Ana Reyes", id: "2022-0041", course: "BS Information Technology" };

  const startRec = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert("Use Chrome for speech recognition."); return; }
    const r = new SR(); r.continuous = true; r.interimResults = true; r.lang = "en-US";
    r.onresult = e => { let t = ""; for (let i = 0; i < e.results.length; i++) t += e.results[i][0].transcript; setSpeech(t); };
    r.onend = () => setRec(false);
    r.start(); recRef.current = r; setRec(true);
  };
  const stopRec = () => { recRef.current?.stop(); setRec(false); };

  const processAI = async () => {
    if (!speech.trim()) return;
    setAiLoad(true);
    try {
      const r = await callAI(
        `Convert this OJT-related informal speech into formal written English suitable for an official OJT document. Keep it to 2–3 sentences. Speech: "${speech}"`,
        "You convert informal Filipino student speech into formal OJT document language. Return only the converted text.",
        (text) => setProc(text)
      );
      setProc(r); 
      setStep(2);
    } catch (e) { alert(e.message); }
    finally { setAiLoad(false); }
  };

  const autoFill = async () => {
    if (!template || !processed) return;
    setFilling(true);
    try {
      const r = await callAI(
        `You are filling an OJT document template for a Filipino college student.
Student: ${STUDENT.name}, ID: ${STUDENT.id}, Course: ${STUDENT.course}
Request text: "${processed}"
Template name: ${template.name}
Fields needed: ${template.fields.join(", ")}
Today's date: ${new Date().toLocaleDateString("en-PH", { dateStyle: "long" })}

Fill in the template below. Replace every {{field}} with appropriate content extracted from the request text. For missing info use reasonable placeholders (e.g. "[Company Name]", "[Start Date]"). Return ONLY the completed document text.

Template:
${template.content}`,
        "You fill OJT document templates accurately. Return only the completed document, no commentary.",
        (text) => setFilled(toRichText(text))
      );
      setFilled(toRichText(r)); 
      setStep(4);
    } catch (e) { alert(e.message); }
    finally { setFilling(false); }
  };

  const submit = () => {
    const req = {
      id: uid(), studentName: STUDENT.name, studentId: STUDENT.id, course: STUDENT.course,
      templateName: template?.name, category: template?.category, status: "pending", urgent,
      submittedAt: new Date().toISOString(), speechText: speech, processedText: processed, filledDocument: filled,
    };
    addRequest(req); setMyReqs(p => [req, ...p]);
    setSubmitted(true);
    setTimeout(() => { setSubmitted(false); setSpeech(""); setProc(""); setTemplate(null); setFilled(""); setUrgent(false); setStep(1); setTab("my"); }, 1800);
  };

  const downloadDoc = req => {
    const content = req.filledDocument || req.processedText || "";
    const plainText = content.replace(/<[^>]*>/g, ""); 
    const b = new Blob([plainText], { type: "text/plain" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(b);
    a.download = `${req.templateName?.replace(/\s+/g,"_")}_${req.id}.txt`; a.click();
  };

  const steps = ["Speak / Type", "Select Template", "AI Auto-Fill", "Review & Submit"];

  return (
    <div>
      <TopBar roleLabel="OJT Student" roleColor="#4f8ef7" notifications={notifications} setNotifications={setNotifications} onLogout={onLogout} />
      <div style={{ maxWidth: 820, margin: "0 auto", padding: "28px 20px" }}>
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28, flexWrap: "wrap", gap: 16 }}>
          <div>
            <h1 style={{ fontFamily: "'DM Serif Display',serif", fontSize: 26, color: "#dde2f0", marginBottom: 4 }}>OJT Document Request</h1>
            <p style={{ color: "#4b5472", fontSize: 13 }}>Hi, <strong style={{ color: "#4f8ef7" }}>{STUDENT.name}</strong> · {STUDENT.course} · ID {STUDENT.id}</p>
          </div>
          <div style={{ display: "flex", gap: 4, background: "#13151f", border: "1px solid #1e2130", borderRadius: 10, padding: 4 }}>
            {["new","my","coach"].map(t => (
              <button key={t} className="btn" onClick={() => setTab(t)}
                style={{ padding: "7px 20px", borderRadius: 7, fontWeight: 600, fontSize: 13, background: tab === t ? "#4f8ef7" : "transparent", color: tab === t ? "#fff" : "#4b5472" }}>
                {t === "new" ? "New Request" : t === "my" ? `My Requests (${myReqs.length})` : "Career Coach"}
              </button>
            ))}
          </div>
        </div>

        {tab === "coach" && <CareerCoachView />}

        {tab === "new" && (
          <div className="slide-in">
            {/* Progress */}
            <div style={{ display: "flex", gap: 0, marginBottom: 28, background: "#13151f", border: "1px solid #1e2130", borderRadius: 12, overflow: "hidden" }}>
              {steps.map((s, i) => {
                const num = i + 1;
                const active = step === num;
                const done = step > num;
                return (
                  <div key={s} style={{ flex: 1, padding: "12px 8px", display: "flex", flexDirection: "column", alignItems: "center", gap: 6, borderRight: i < 3 ? "1px solid #1e2130" : "none", background: active ? "#4f8ef710" : "transparent", transition: "background .2s" }}>
                    <div style={{ width: 26, height: 26, borderRadius: "50%", background: done ? "#2a9d8f" : active ? "#4f8ef7" : "#1e2130", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700, color: done || active ? "#fff" : "#3a4060" }}>
                      {done ? "✓" : num}
                    </div>
                    <div style={{ fontSize: 11, fontWeight: 600, color: active ? "#4f8ef7" : done ? "#2a9d8f" : "#3a4060", textAlign: "center" }}>{s}</div>
                  </div>
                );
              })}
            </div>

            {/* Step 1: Speech */}
            <Section title="1 — Speak or Type Your OJT Request" color="#4f8ef7">
              <p style={{ color: "#4b5472", fontSize: 13, marginBottom: 16, fontStyle: "italic" }}>
                Describe what document you need. Example: <em>"I need an endorsement letter for my OJT at [company], starting [date]…"</em>
              </p>
              <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 14, flexWrap: "wrap" }}>
                <button className={`btn ${recording ? "pulse" : ""}`} onClick={recording ? stopRec : startRec}
                  style={{ width: 52, height: 52, borderRadius: "50%", background: recording ? "#e74c3c" : "#4f8ef7", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 20 }}>
                  🎤
                </button>
                <div style={{ color: recording ? "#e74c3c" : "#4b5472", fontWeight: 600, fontSize: 13 }}>
                  {recording ? "● Recording… tap to stop" : "Tap to record, or type below"}
                </div>
              </div>
              <textarea className="inp" rows={4} placeholder="Your OJT request will appear here, or type it directly…" value={speech} onChange={e => setSpeech(e.target.value)} />
              <button className="btn" onClick={processAI} disabled={!speech.trim() || aiLoading}
                style={{ marginTop: 12, padding: "9px 22px", background: speech.trim() && !aiLoading ? "#4f8ef7" : "#1e2130", color: speech.trim() && !aiLoading ? "#fff" : "#3a4060", borderRadius: 8, fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
                ✦ {aiLoading ? "Processing…" : "AI — Convert to Formal Text"}
              </button>
              {processed && (
                <div style={{ marginTop: 14, background: "#4f8ef710", border: "1px solid #4f8ef730", borderRadius: 10, padding: 14 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#4f8ef7", marginBottom: 8, textTransform: "uppercase", letterSpacing: .8 }}>✦ AI Formal Version</div>
                  <textarea className="inp" rows={3} style={{ background: "transparent", border: "none", borderBottom: "1px solid #252840", borderRadius: 0, padding: "0 0 8px" }} value={processed} onChange={e => setProc(e.target.value)} />
                </div>
              )}
            </Section>

            {/* Step 2: Template */}
            {processed && (
              <Section title="2 — Select OJT Document Template" color="#4f8ef7" mt>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(230px,1fr))", gap: 10 }}>
                  {TEMPLATES.map(t => (
                    <div key={t.id} onClick={() => { setTemplate(t); setStep(3); }}
                      style={{ padding: "14px 16px", border: `1.5px solid ${template?.id === t.id ? "#4f8ef7" : "#1e2130"}`, borderRadius: 10, cursor: "pointer", background: template?.id === t.id ? "#4f8ef710" : "#13151f", transition: "all .2s" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, alignItems: "flex-start", gap: 6 }}>
                        <span style={{ fontWeight: 600, fontSize: 13, color: "#dde2f0", lineHeight: 1.3 }}>{t.name}</span>
                        <span className="tag" style={{ background: `${CAT_COLORS[t.category]}18`, color: CAT_COLORS[t.category], flexShrink: 0 }}>{t.category}</span>
                      </div>
                      <div style={{ fontSize: 11, color: "#3a4060" }}>Fields: {t.fields.slice(0,4).join(", ")}{t.fields.length > 4 ? "…" : ""}</div>
                    </div>
                  ))}
                </div>
                {template && (
                  <button className="btn" onClick={autoFill} disabled={filling}
                    style={{ marginTop: 16, padding: "9px 22px", background: filling ? "#1e2130" : "#4f8ef7", color: filling ? "#3a4060" : "#fff", borderRadius: 8, fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
                    ✦ {filling ? "Auto-filling…" : `AI Auto-Fill "${template.name}"`}
                  </button>
                )}
              </Section>
            )}

            {/* Step 3: Preview */}
            {(filled || filling) && (
              <Section title="3 — Preview & Edit Document" color="#4f8ef7" mt>
                {filling && !filled
                  ? <div style={{ height: 180, background: "linear-gradient(90deg,#13151f 25%,#1a1d2a 50%,#13151f 75%)", backgroundSize: "400%", animation: "shimmer 1.6s infinite", borderRadius: 8 }} />
                  : <ReactQuill theme="snow" modules={QUILL_MODULES} value={filled} onChange={setFilled} style={{ height: "auto" }} />
                }
              </Section>
            )}

            {/* Step 4: Submit */}
            {filled && (
              <Section title="4 — Submit Request" color="#4f8ef7" mt>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 16 }}>
                  <label style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}>
                    <div onClick={() => setUrgent(!urgent)}
                      style={{ width: 46, height: 25, borderRadius: 13, background: urgent ? "#e74c3c" : "#1e2130", border: `1px solid ${urgent ? "#e74c3c" : "#252840"}`, cursor: "pointer", position: "relative", transition: "all .2s", flexShrink: 0 }}>
                      <div style={{ position: "absolute", top: 3, left: urgent ? 23 : 3, width: 19, height: 19, borderRadius: "50%", background: "#fff", transition: "left .2s" }} />
                    </div>
                    <span style={{ fontWeight: 600, fontSize: 13, color: urgent ? "#e74c3c" : "#4b5472" }}>
                      {urgent ? "🚨 Urgent — Rush Processing" : "Mark as Urgent"}
                    </span>
                  </label>
                  <button className="btn" onClick={submit} disabled={submitted}
                    style={{ padding: "11px 28px", background: submitted ? "#2a9d8f" : "#4f8ef7", color: "#fff", borderRadius: 10, fontWeight: 700, fontSize: 14, display: "flex", alignItems: "center", gap: 8 }}>
                    {submitted ? "✓ Submitted!" : "Submit to Coordinator →"}
                  </button>
                </div>
              </Section>
            )}
          </div>
        )}

        {tab === "my" && (
          <div className="slide-in">
            <h2 style={{ fontFamily: "'DM Serif Display',serif", fontSize: 19, color: "#dde2f0", marginBottom: 18 }}>My OJT Requests</h2>
            {myReqs.length === 0 ? <Empty msg="No requests yet" /> :
              myReqs.map(r => (
                <div key={r.id} className={r.urgent ? "pulse" : ""} style={{ background: "#13151f", border: `1px solid ${r.urgent ? "#e74c3c33" : "#1e2130"}`, borderRadius: 12, padding: "18px 20px", marginBottom: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 10 }}>
                    <div>
                      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4, flexWrap: "wrap" }}>
                        <span style={{ fontWeight: 700, fontSize: 15, color: "#dde2f0" }}>{r.templateName}</span>
                        {r.category && <span className="tag" style={{ background: `${CAT_COLORS[r.category]}18`, color: CAT_COLORS[r.category] }}>{r.category}</span>}
                        {r.urgent && <span className="tag" style={{ background: "#e74c3c18", color: "#e74c3c" }}>🚨 URGENT</span>}
                      </div>
                      <div style={{ fontSize: 12, color: "#3a4060" }}>{fmtDate(r.submittedAt)}</div>
                    </div>
                    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <StatusBadge status={r.status} />
                      {r.status === "approved" && (
                        <button className="btn" onClick={() => downloadDoc(r)}
                          style={{ padding: "7px 14px", background: "#2a9d8f18", color: "#2a9d8f", border: "1px solid #2a9d8f30", borderRadius: 7, fontWeight: 600, fontSize: 12, display: "flex", alignItems: "center", gap: 5 }}>
                          ⬇ Download
                        </button>
                      )}
                    </div>
                  </div>
                  {r.status === "pending" && (
                    <div style={{ marginTop: 10, fontSize: 12, color: "#4b5472", display: "flex", alignItems: "center", gap: 6 }}>
                      <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#e9c46a", display: "inline-block" }} />
                      Awaiting coordinator review
                    </div>
                  )}
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── COORDINATOR VIEW ─────────────────────────────────────────────────────────
function CoordinatorView({ requests, updateRequest, notifications, setNotifications, onLogout }) {
  const [selected, setSelected]   = useState(null);
  const [editedDoc, setEditedDoc] = useState("");
  const [filter, setFilter]       = useState("all");
  const [aiNote, setAiNote]       = useState("");
  const [genNote, setGenNote]     = useState(false);

  const visible = requests.filter(r =>
    filter === "all" ? true : filter === "urgent" ? r.urgent : r.status === filter
  );

  const approve = req => {
    updateRequest(req.id, { status: "approved", filledDocument: editedDoc || req.filledDocument });
    setNotifications(p => [{ id: Date.now(), msg: `OJT request ${req.id} from ${req.studentName} approved`, time: new Date().toLocaleTimeString("en-PH", { timeStyle: "short" }), read: false, type: "approved" }, ...p]);
    setSelected(null);
  };
  const reject = req => { updateRequest(req.id, { status: "rejected" }); setSelected(null); };

  const generateNote = async () => {
    if (!selected) return;
    setGenNote(true);
    try {
      const r = await callAI(
        `Write a brief 2-sentence coordinator review note for this OJT document request.\nStudent: ${selected.studentName} (${selected.studentId})\nDocument: ${selected.templateName}\nRequest: ${selected.processedText}\nStatus: APPROVED\nKeep it professional and concise.`,
        "You write brief official coordinator review notes for OJT documents.",
        (text) => setAiNote(text)
      );
      setAiNote(r);
    } catch (e) { alert(e.message); }
    finally { setGenNote(false); }
  };

  const downloadDoc = req => {
    const content = editedDoc || req.filledDocument || req.processedText || "";
    const plainText = content.replace(/<[^>]*>/g, ""); // Basic HTML strip
    const b = new Blob([plainText], { type: "text/plain" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(b);
    a.download = `${req.templateName?.replace(/\s+/g,"_")}_${req.id}.txt`; a.click();
  };

  const pendingCount = requests.filter(r => r.status === "pending").length;
  const urgentCount  = requests.filter(r => r.urgent && r.status === "pending").length;

  return (
    <div>
      <TopBar roleLabel="Coordinator" roleColor="#e9c46a" notifications={notifications} setNotifications={setNotifications} onLogout={onLogout} />
      <div style={{ maxWidth: 1160, margin: "0 auto", padding: "28px 20px", display: "grid", gridTemplateColumns: selected ? "380px 1fr" : "1fr", gap: 24 }}>

        {/* Left: Queue */}
        <div>
          <div style={{ marginBottom: 20 }}>
            <h1 style={{ fontFamily: "'DM Serif Display',serif", fontSize: 23, color: "#dde2f0", marginBottom: 6 }}>OJT Request Queue</h1>
            <div style={{ display: "flex", gap: 12 }}>
              <Stat label="Pending" value={pendingCount} color="#e9c46a" />
              <Stat label="Urgent" value={urgentCount} color="#e74c3c" />
              <Stat label="Total" value={requests.length} color="#4f8ef7" />
            </div>
          </div>

          {/* Filters */}
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 16 }}>
            {[["all","All"], ["urgent","🚨 Urgent"], ["pending","Pending"], ["approved","Approved"], ["rejected","Rejected"]].map(([k,l]) => (
              <button key={k} className="btn" onClick={() => setFilter(k)}
                style={{ padding: "6px 14px", borderRadius: 20, fontWeight: 600, fontSize: 12, background: filter === k ? "#e9c46a" : "#13151f", color: filter === k ? "#0c0e14" : "#4b5472", border: filter === k ? "none" : "1px solid #1e2130" }}>
                {l}
              </button>
            ))}
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {visible.length === 0 ? <Empty msg="No requests here" /> :
              visible.map(req => (
                <div key={req.id} className={`hover-row ${req.urgent ? "pulse" : ""}`} onClick={() => { setSelected(req); setEditedDoc(toRichText(req.filledDocument || "")); setAiNote(""); }}
                  style={{ background: selected?.id === req.id ? "#1a1d2a" : "#13151f", border: `1.5px solid ${req.urgent ? "#e74c3c33" : selected?.id === req.id ? "#e9c46a30" : "#1e2130"}`, borderRadius: 12, padding: "15px 17px", cursor: "pointer", transition: "all .2s" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8, marginBottom: 6 }}>
                    <div style={{ fontWeight: 700, fontSize: 14, color: "#dde2f0" }}>{req.studentName}</div>
                    <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                      {req.urgent && <span className="tag" style={{ background: "#e74c3c18", color: "#e74c3c" }}>URGENT</span>}
                      <StatusBadge status={req.status} />
                    </div>
                  </div>
                  <div style={{ fontSize: 13, color: "#6b7590", marginBottom: 3 }}>{req.templateName}</div>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    {req.category && <span className="tag" style={{ background: `${CAT_COLORS[req.category]}15`, color: CAT_COLORS[req.category] }}>{req.category}</span>}
                    <span style={{ fontSize: 11, color: "#3a4060" }}>{fmtDate(req.submittedAt)}</span>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Right: Detail */}
        {selected && (
          <div className="slide-in">
            <div className="card">
              <div style={{ padding: "14px 20px", borderBottom: "1px solid #1e2130", display: "flex", justifyContent: "space-between", alignItems: "center", background: "#e9c46a08" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{ width: 3, height: 18, background: "#e9c46a", borderRadius: 2 }} />
                  <span style={{ fontWeight: 700, fontSize: 15, color: "#dde2f0" }}>{selected.studentName}</span>
                  <span style={{ fontSize: 12, color: "#4b5472" }}>· {selected.studentId}</span>
                  {selected.urgent && <span className="tag" style={{ background: "#e74c3c18", color: "#e74c3c" }}>🚨 URGENT</span>}
                </div>
                <button className="btn" onClick={() => setSelected(null)} style={{ background: "transparent", color: "#4b5472", padding: 6, fontSize: 18 }}>×</button>
              </div>
              <div style={{ padding: "18px 20px" }}>
                {/* Meta */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 18 }}>
                  {[["Course", selected.course || "—"], ["Document", selected.templateName], ["Category", selected.category || "—"], ["Submitted", fmtDate(selected.submittedAt)]].map(([k,v]) => (
                    <div key={k} style={{ background: "#1a1d2a", border: "1px solid #1e2130", borderRadius: 8, padding: "9px 12px" }}>
                      <div style={{ fontSize: 10, color: "#3a4060", fontWeight: 600, textTransform: "uppercase", letterSpacing: .6, marginBottom: 3 }}>{k}</div>
                      <div style={{ fontSize: 13, color: "#b0b8d4", fontWeight: 500 }}>{v}</div>
                    </div>
                  ))}
                </div>

                {/* Speech */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#4b5472", textTransform: "uppercase", letterSpacing: .6, marginBottom: 6 }}>Student's Speech</div>
                  <div style={{ background: "#1a1d2a", border: "1px solid #1e2130", borderRadius: 8, padding: 12, fontSize: 13, color: "#6b7590", fontStyle: "italic" }}>"{selected.speechText}"</div>
                </div>

                {/* Edit doc */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#4b5472", textTransform: "uppercase", letterSpacing: .6, marginBottom: 6 }}>Generated Document — Edit if Needed</div>
                  <ReactQuill theme="snow" modules={QUILL_MODULES} value={editedDoc} onChange={setEditedDoc} style={{ height: "auto" }} />
                </div>

                {/* AI Review Note */}
                <div style={{ marginBottom: 18 }}>
                  <button className="btn" onClick={generateNote} disabled={genNote}
                    style={{ padding: "7px 16px", background: "#13151f", border: "1px solid #1e2130", color: "#e9c46a", borderRadius: 8, fontWeight: 600, fontSize: 12, display: "flex", alignItems: "center", gap: 6 }}>
                    ✦ {genNote ? "Generating note…" : "Generate Coordinator Review Note"}
                  </button>
                  {aiNote && <div style={{ marginTop: 10, background: "#e9c46a0a", border: "1px solid #e9c46a20", borderRadius: 8, padding: 12, fontSize: 13, color: "#b0b8d4", lineHeight: 1.6 }}>{aiNote}</div>}
                </div>

                {/* Actions */}
                <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                  {selected.status === "pending" && <>
                    <button className="btn" onClick={() => approve(selected)}
                      style={{ padding: "9px 20px", background: "#2a9d8f", color: "#fff", borderRadius: 8, fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
                      ✓ Approve & Notify Admin
                    </button>
                    <button className="btn" onClick={() => reject(selected)}
                      style={{ padding: "9px 20px", background: "#e74c3c18", color: "#e74c3c", border: "1px solid #e74c3c30", borderRadius: 8, fontWeight: 600, fontSize: 13 }}>
                      ✕ Reject
                    </button>
                  </>}
                  <button className="btn" onClick={() => downloadDoc(selected)}
                    style={{ padding: "9px 20px", background: "#4f8ef718", color: "#4f8ef7", border: "1px solid #4f8ef730", borderRadius: 8, fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
                    ⬇ Export DOCX
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── ADMIN VIEW ───────────────────────────────────────────────────────────────
function AdminView({ requests, updateRequest, notifications, setNotifications, onLogout }) {
  const [tab, setTab] = useState("dashboard");
  const [viewDoc, setViewDoc] = useState(null);
  const total    = requests.length;
  const urgent   = requests.filter(r => r.urgent).length;
  const approved = requests.filter(r => r.status === "approved").length;
  const pending  = requests.filter(r => r.status === "pending").length;
  const rejected = requests.filter(r => r.status === "rejected").length;

  const byCategory = TEMPLATES.reduce((acc, t) => {
    acc[t.category] = (acc[t.category] || 0) + requests.filter(r => r.category === t.category).length;
    return acc;
  }, {});

  const downloadDoc = req => {
    const b = new Blob([req.filledDocument || req.processedText || ""], { type: "text/plain" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(b);
    a.download = `FINAL_${req.templateName?.replace(/\s+/g,"_")}_${req.id}.txt`; a.click();
  };

  const finalApprove = req => { updateRequest(req.id, { status: "approved", finalApproved: true }); };

  const TABS = [["dashboard","Dashboard"],["requests","All Requests"],["templates","OJT Templates"],["users","Users"],["logs","Logs"]];

  return (
    <div>
      <TopBar roleLabel="Admin" roleColor="#e76f51" notifications={notifications} setNotifications={setNotifications} onLogout={onLogout} />
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "28px 20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 26, flexWrap: "wrap", gap: 16 }}>
          <div>
            <h1 style={{ fontFamily: "'DM Serif Display',serif", fontSize: 25, color: "#dde2f0", marginBottom: 4 }}>Admin — OJT System</h1>
            <p style={{ color: "#4b5472", fontSize: 13 }}>Manage all OJT document requests, templates, and users</p>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 4, background: "#13151f", border: "1px solid #1e2130", borderRadius: 10, padding: 4, marginBottom: 28, flexWrap: "wrap" }}>
          {TABS.map(([k,l]) => (
            <button key={k} className="btn" onClick={() => setTab(k)}
              style={{ padding: "8px 18px", borderRadius: 7, fontWeight: 600, fontSize: 13, background: tab === k ? "#e76f51" : "transparent", color: tab === k ? "#fff" : "#4b5472" }}>{l}</button>
          ))}
        </div>

        {tab === "dashboard" && (
          <div className="slide-in">
            {/* Stats */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(180px,1fr))", gap: 14, marginBottom: 28 }}>
              {[
                { label: "Total Requests", val: total, color: "#4f8ef7", icon: "📋" },
                { label: "Urgent Cases",   val: urgent,   color: "#e74c3c", icon: "🚨" },
                { label: "Approved",       val: approved, color: "#2a9d8f", icon: "✅" },
                { label: "Pending",        val: pending,  color: "#e9c46a", icon: "⏳" },
                { label: "Rejected",       val: rejected, color: "#e76f51", icon: "❌" },
              ].map(s => (
                <div key={s.label} style={{ background: "#13151f", border: "1px solid #1e2130", borderRadius: 14, padding: "18px 20px" }}>
                  <div style={{ fontSize: 22, marginBottom: 8 }}>{s.icon}</div>
                  <div style={{ fontSize: 34, fontFamily: "'DM Serif Display',serif", color: s.color, lineHeight: 1 }}>{s.val}</div>
                  <div style={{ fontSize: 12, color: "#4b5472", marginTop: 5, fontWeight: 500 }}>{s.label}</div>
                </div>
              ))}
            </div>

            {/* Category breakdown */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
              <Section title="Requests by OJT Stage" color="#e76f51">
                {Object.entries(byCategory).map(([cat, count]) => (
                  <div key={cat} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid #1a1d2a" }}>
                    <span className="tag" style={{ background: `${CAT_COLORS[cat]}15`, color: CAT_COLORS[cat] }}>{cat}</span>
                    <span style={{ fontWeight: 700, fontSize: 18, color: "#dde2f0", fontFamily: "'DM Serif Display',serif" }}>{count}</span>
                  </div>
                ))}
              </Section>
              <Section title="Recent Notifications" color="#e76f51">
                {notifications.slice(0,5).map(n => (
                  <div key={n.id} style={{ padding: "9px 0", borderBottom: "1px solid #1a1d2a", display: "flex", gap: 10 }}>
                    <div style={{ width: 6, height: 6, borderRadius: "50%", background: n.type === "urgent" ? "#e74c3c" : "#2a9d8f", marginTop: 5, flexShrink: 0 }} />
                    <div>
                      <div style={{ fontSize: 12.5, color: "#9ba3bb", lineHeight: 1.4 }}>{n.msg}</div>
                      <div style={{ fontSize: 11, color: "#2e3348", marginTop: 2 }}>{n.time}</div>
                    </div>
                  </div>
                ))}
              </Section>
            </div>

            {/* Urgent pending */}
            {requests.filter(r => r.urgent && r.status === "pending").length > 0 && (
              <Section title="🚨 Urgent — Awaiting Final Approval" color="#e74c3c">
                {requests.filter(r => r.urgent && r.status === "pending").map(r => (
                  <div key={r.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: "1px solid #1a1d2a", gap: 12, flexWrap: "wrap" }}>
                    <div>
                      <span style={{ fontWeight: 700, color: "#dde2f0", fontSize: 14 }}>{r.studentName}</span>
                      <span style={{ color: "#4b5472", fontSize: 13, marginLeft: 8 }}>{r.templateName}</span>
                    </div>
                    <div style={{ display: "flex", gap: 8 }}>
                      <button className="btn" onClick={() => finalApprove(r)}
                        style={{ padding: "6px 14px", background: "#2a9d8f", color: "#fff", borderRadius: 7, fontWeight: 600, fontSize: 12 }}>
                        Final Approve
                      </button>
                      <StatusBadge status={r.status} />
                    </div>
                  </div>
                ))}
              </Section>
            )}
          </div>
        )}

        {tab === "requests" && (
          <div className="slide-in">
            <div style={{ background: "#13151f", border: "1px solid #1e2130", borderRadius: 14, overflow: "hidden" }}>
              <div style={{ display: "grid", gridTemplateColumns: "2fr 2fr 1fr 1fr 1fr", padding: "12px 20px", borderBottom: "1px solid #1e2130", background: "#1a1d2a" }}>
                {["Student","Document","Category","Status","Action"].map(h => (
                  <div key={h} style={{ fontSize: 11, fontWeight: 700, color: "#3a4060", textTransform: "uppercase", letterSpacing: .6 }}>{h}</div>
                ))}
              </div>
              {requests.map(r => (
                <div key={r.id} className="hover-row" style={{ display: "grid", gridTemplateColumns: "2fr 2fr 1fr 1fr 1fr", padding: "13px 20px", borderBottom: "1px solid #1e2130", alignItems: "center", background: r.urgent ? "#e74c3c05" : "transparent" }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 13.5, color: "#dde2f0" }}>{r.studentName} {r.urgent && "🚨"}</div>
                    <div style={{ fontSize: 11, color: "#3a4060" }}>{r.studentId}</div>
                  </div>
                  <div style={{ fontSize: 12.5, color: "#6b7590" }}>{r.templateName}</div>
                  <div>{r.category && <span className="tag" style={{ background: `${CAT_COLORS[r.category]}15`, color: CAT_COLORS[r.category] }}>{r.category}</span>}</div>
                  <StatusBadge status={r.status} />
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    <button className="btn" onClick={() => setViewDoc(r)}
                      style={{ padding: "5px 12px", background: "#4f8ef718", color: "#4f8ef7", border: "1px solid #4f8ef730", borderRadius: 7, fontWeight: 600, fontSize: 11 }}>
                      👁 View
                    </button>
                    {r.status === "approved" && (
                      <button className="btn" onClick={() => downloadDoc(r)}
                        style={{ padding: "5px 12px", background: "#2a9d8f18", color: "#2a9d8f", border: "1px solid #2a9d8f30", borderRadius: 7, fontWeight: 600, fontSize: 11 }}>
                        ⬇ Download
                      </button>
                    )}
                    {r.status === "pending" && (
                      <button className="btn" onClick={() => finalApprove(r)}
                        style={{ padding: "5px 12px", background: "#e76f5118", color: "#e76f51", border: "1px solid #e76f5130", borderRadius: 7, fontWeight: 600, fontSize: 11 }}>
                        Approve
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === "templates" && (
          <div className="slide-in" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {TEMPLATES.map(t => (
              <div key={t.id} style={{ background: "#13151f", border: "1px solid #1e2130", borderRadius: 14, overflow: "hidden" }}>
                <div style={{ padding: "14px 20px", borderBottom: "1px solid #1e2130", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 10 }}>
                  <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                    <span style={{ fontWeight: 700, fontSize: 15, color: "#dde2f0" }}>{t.name}</span>
                    <span className="tag" style={{ background: `${CAT_COLORS[t.category]}15`, color: CAT_COLORS[t.category] }}>{t.category}</span>
                  </div>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {t.fields.map(f => <span key={f} className="tag" style={{ background: "#4f8ef715", color: "#4f8ef7" }}>{`{{${f}}}`}</span>)}
                  </div>
                </div>
                <pre style={{ padding: "14px 20px", fontSize: 12.5, color: "#4b5472", whiteSpace: "pre-wrap", fontFamily: "'DM Sans',sans-serif", lineHeight: 1.7, maxHeight: 150, overflow: "auto" }}>{t.content}</pre>
              </div>
            ))}
          </div>
        )}

        {tab === "users" && (
          <div className="slide-in">
            <Section title="Registered Users" color="#e76f51">
              {[
                { name: "Ana Reyes",     id: "2022-0041", role: "Student",     course: "BS Information Technology", status: "active" },
                { name: "Carlo Mendoza", id: "2021-0088", role: "Student",     course: "BS Accountancy",            status: "active" },
                ...COORDINATORS.map((c,i) => ({ name: c, id: `COORD-${i+1}`, role: "Coordinator", course: "Faculty",  status: "active" })),
                { name: "Admin User",    id: "ADMIN-01",  role: "Admin",       course: "System Administrator",      status: "active" },
              ].map((u, i) => (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: "1px solid #1a1d2a", flexWrap: "wrap", gap: 10 }}>
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <div style={{ width: 36, height: 36, borderRadius: "50%", background: u.role === "Student" ? "#4f8ef720" : u.role === "Coordinator" ? "#e9c46a20" : "#e76f5120", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>
                      {u.role === "Student" ? "👤" : u.role === "Coordinator" ? "👩‍🏫" : "⚙️"}
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 13.5, color: "#dde2f0" }}>{u.name}</div>
                      <div style={{ fontSize: 12, color: "#4b5472" }}>{u.course} · {u.id}</div>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <span className="tag" style={{ background: u.role === "Student" ? "#4f8ef718" : u.role === "Coordinator" ? "#e9c46a18" : "#e76f5118", color: u.role === "Student" ? "#4f8ef7" : u.role === "Coordinator" ? "#e9c46a" : "#e76f51" }}>{u.role}</span>
                    <span className="tag" style={{ background: "#2a9d8f18", color: "#2a9d8f" }}>Active</span>
                  </div>
                </div>
              ))}
            </Section>
          </div>
        )}

        {tab === "logs" && (
          <div className="slide-in">
            <Section title="System Activity Log" color="#e76f51">
              {[
                { time: "09:31 AM", event: "🚨 Urgent OJT endorsement request submitted", actor: "Ana Reyes",     type: "urgent" },
                { time: "09:30 AM", event: "New request created — OJT Endorsement Letter",  actor: "Ana Reyes",     type: "new" },
                { time: "02:20 PM", event: "OJT Completion request APPROVED",                actor: "Coordinator",   type: "approved" },
                { time: "02:15 PM", event: "Document edited by Coordinator",                 actor: "Prof. Santos",  type: "edit" },
                { time: "02:13 PM", event: "New request created — Completion Certificate",   actor: "Carlo Mendoza", type: "new" },
                { time: "10:00 AM", event: "System started",                                 actor: "System",        type: "info" },
                ...requests.map(r => ({ time: new Date(r.submittedAt).toLocaleTimeString("en-PH",{timeStyle:"short"}), event: `Request ${r.id} submitted (${r.status})`, actor: r.studentName, type: r.status })),
              ].map((l, i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "72px 1fr 120px", gap: 16, padding: "10px 0", borderBottom: "1px solid #1a1d2a", alignItems: "center" }}>
                  <div style={{ fontSize: 11, color: "#2e3348", fontWeight: 600 }}>{l.time}</div>
                  <div style={{ fontSize: 13, color: "#9ba3bb" }}>{l.event}</div>
                  <div style={{ fontSize: 12, color: "#3a4060", textAlign: "right" }}>{l.actor}</div>
                </div>
              ))}
            </Section>
          </div>
        )}
      </div>

      {/* Document Viewer Modal */}
      {viewDoc && (
        <div className="fade-in" onClick={() => setViewDoc(null)}
          style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.75)", zIndex: 500, display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
          <div onClick={e => e.stopPropagation()}
            style={{ background: "#13151f", border: "1px solid #1e2130", borderRadius: 18, width: "100%", maxWidth: 680, maxHeight: "85vh", display: "flex", flexDirection: "column", boxShadow: "0 32px 80px rgba(0,0,0,.6)" }}>
            {/* Modal Header */}
            <div style={{ padding: "16px 22px", borderBottom: "1px solid #1e2130", display: "flex", justifyContent: "space-between", alignItems: "center", flexShrink: 0 }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 3 }}>
                  <div style={{ width: 3, height: 18, background: "#e76f51", borderRadius: 2 }} />
                  <span style={{ fontWeight: 700, fontSize: 15, color: "#dde2f0" }}>{viewDoc.templateName}</span>
                  {viewDoc.category && <span className="tag" style={{ background: `${CAT_COLORS[viewDoc.category]}15`, color: CAT_COLORS[viewDoc.category] }}>{viewDoc.category}</span>}
                  {viewDoc.urgent && <span className="tag" style={{ background: "#e74c3c18", color: "#e74c3c" }}>🚨 URGENT</span>}
                </div>
                <div style={{ fontSize: 12, color: "#4b5472", paddingLeft: 13 }}>{viewDoc.studentName} · {viewDoc.studentId} · {fmtDate(viewDoc.submittedAt)}</div>
              </div>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <StatusBadge status={viewDoc.status} />
                <button className="btn" onClick={() => downloadDoc(viewDoc)}
                  style={{ padding: "6px 14px", background: "#2a9d8f18", color: "#2a9d8f", border: "1px solid #2a9d8f30", borderRadius: 7, fontWeight: 600, fontSize: 12, display: "flex", alignItems: "center", gap: 5 }}>
                  ⬇ Download
                </button>
                <button className="btn" onClick={() => setViewDoc(null)}
                  style={{ background: "#1a1d2a", border: "1px solid #1e2130", color: "#6b7590", width: 32, height: 32, borderRadius: 8, fontSize: 18, display: "flex", alignItems: "center", justifyContent: "center" }}>×</button>
              </div>
            </div>
            {/* Document Body */}
            <div style={{ padding: "22px 24px", overflowY: "auto" }}>
              <div 
                style={{ fontFamily: "'DM Sans',sans-serif", fontSize: 13.5, color: "#c8d0e8", lineHeight: 1.85, background: "#1a1d2a", border: "1px solid #252840", borderRadius: 10, padding: "20px 22px", minHeight: 200 }}
                dangerouslySetInnerHTML={{ __html: viewDoc.filledDocument || viewDoc.processedText || "No document content available." }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── SHARED ───────────────────────────────────────────────────────────────────
function Section({ title, color = "#4f8ef7", children, mt }) {
  return (
    <div className="card" style={{ marginTop: mt ? 28 : 0 }}>
      <div style={{ padding: "13px 20px", borderBottom: "1px solid #1e2130", display: "flex", alignItems: "center", gap: 8, background: `${color}08` }}>
        <div style={{ width: 3, height: 16, background: color, borderRadius: 2 }} />
        <span style={{ fontWeight: 700, fontSize: 14, color: "#dde2f0" }}>{title}</span>
      </div>
      <div style={{ padding: "16px 20px" }}>{children}</div>
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div style={{ background: "#13151f", border: `1px solid ${color}25`, borderRadius: 8, padding: "7px 14px", display: "flex", gap: 8, alignItems: "baseline" }}>
      <span style={{ fontFamily: "'DM Serif Display',serif", fontSize: 22, color, lineHeight: 1 }}>{value}</span>
      <span style={{ fontSize: 12, color: "#4b5472" }}>{label}</span>
    </div>
  );
}

function StatusBadge({ status }) {
  const s = STATUS_MAP[status] || { color: "#4b5472", bg: "#4b547218", label: status };
  return <span className="tag" style={{ background: s.bg, color: s.color }}>{s.label}</span>;
}

function Empty({ msg }) {
  return <div style={{ textAlign: "center", padding: "40px 20px", color: "#2e3348" }}>📄<div style={{ marginTop: 8, fontSize: 13, fontWeight: 500 }}>{msg}</div></div>;
}

// ─── CAREER COACH VIEW ────────────────────────────────────────────────────────
const PROFESSION_GROUPS = {
  "IT": ["IT Support Specialist", "Network Administrator", "Systems Analyst", "Cybersecurity Trainee", "Cloud Engineer Intern"],
  "CS": ["Full Stack Developer", "Backend Engineer", "Mobile App Developer", "Software QA Tester", "Data Scientist"],
  "TECH": ["Software Engineer", "Web Developer", "Data Analyst", "Database Admin", "Network Engineer"],
  "DESIGN": ["UI/UX Designer", "Graphic Designer", "Video Editor", "Motion Graphics Artist", "Digital Artist"],
  "BUSINESS": ["Marketing Intern", "Financial Analyst", "HR Assistant", "Accountant Trainee", "Operations Intern"],
  "ENGINEERING": ["Civil Engineer Intern", "Electrical Trainee", "Mechanical Apprentice", "Industrial Engineer", "Project Estimator"],
  "MARKETING": ["Social Media Manager", "Content Creator", "SEO Specialist", "Market Researcher", "Ads Manager"],
  "HOSPITALITY": ["Front Desk Intern", "Kitchen Apprentice", "Events Coordinator", "Hotel Management Trainee", "Tourism Assistant"],
};

function CareerCoachView() {
  const [step, setStep] = useState(1);
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [salary, setSalary] = useState("20,000");
  const [frequency, setFrequency] = useState("Monthly");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);
  const [applying, setApplying] = useState(null);
  const [saved, setSaved] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const query = jobTitle.toUpperCase().trim();
    if (query.length > 0) {
      const matched = [];
      Object.entries(PROFESSION_GROUPS).forEach(([key, roles]) => {
        if (key.includes(query) || roles.some(r => r.toUpperCase().includes(query))) {
          matched.push(...roles);
        }
      });
      // Filter out roles already containing the query or being part of the group
      setSuggestions([...new Set(matched)].filter(r => r.toUpperCase() !== query).slice(0, 6));
    } else {
      setSuggestions([]);
    }
  }, [jobTitle]);

  const performAnalysis = async () => {
    setLoading(true);
    try {
      const sys = `Expert Matchmaker. Find 5 companies in ${location} for ${jobTitle} at ₱${salary}. Return ONLY JSON: {"matches": [{"name": "...", "keyword": "Local/Salary Match"}]}`;
      const r = await callAI(`Match: ${jobTitle}, ${location}`, sys);
      const data = JSON.parse(r.replace(/```json|```/g, ""));
      const enhanced = data.matches.map(m => ({
        ...m,
        id: uid(),
        rating: (Math.random() * (5 - 3.8) + 3.8).toFixed(1),
        reviews: Math.floor(Math.random() * 50) + 10,
        requirements: ["Strong technical proficiency", "Basic " + jobTitle + " foundation", "Team collaboration", "Based in or near " + location],
        posted: "Recently"
      }));
      setAnalysis({ jobs: enhanced });
      setStep(4);
    } catch (e) {
      setAnalysis({ jobs: [
        { id: 'f1', name: "TechCorp " + location, keyword: "Top Local Match", rating: "4.8", reviews: 124, requirements: ["Basic Skills", "Good Communication", "Passion for " + jobTitle], posted: "1 day ago" },
        { id: 'f2', name: "Global Hub " + location, keyword: "Salary Match", rating: "4.5", reviews: 89, requirements: ["Motivated", "Understands " + jobTitle, "Proactive"], posted: "2 days ago" }
      ]});
      setStep(4);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(1); setJobTitle(""); setLocation(""); setAnalysis(null);
  };

  return (
    <div className="slide-in">
      <Section title="OJT Matchmaker & Career Path" color="#4f8ef7">
        
        {step === 1 && (
          <div className="fade-in">
            <div style={{ fontSize: 11, fontWeight: 700, color: "#4f8ef7", textTransform: "uppercase", letterSpacing: .8, marginBottom: 12 }}>Step 1: Profession</div>
            <p style={{ color: "#dde2f0", fontSize: 14, marginBottom: 16 }}>What OJT position or profession are you looking for?</p>
            <input className="inp" placeholder="e.g. IT, CS, Graphic Designer..." value={jobTitle} onChange={e => setJobTitle(e.target.value)} autoFocus />
            
            {/* Dynamic Suggestions */}
            {suggestions.length > 0 && (
              <div style={{ marginTop: 16, animation: "fIn .2s ease" }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#4f8ef7", textTransform: "uppercase", letterSpacing: .8, marginBottom: 10 }}>Related Roles Found</div>
                <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                  {suggestions.map(s => (
                    <button key={s} className="btn" onClick={() => { setJobTitle(s); setStep(2); }}
                      style={{ padding: "6px 14px", background: "#4f8ef715", border: "1px solid #4f8ef730", borderRadius: 20, color: "#4f8ef7", fontSize: 12, fontWeight: 600 }}>
                      + {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Quick Select (only show if no suggestions) */}
            {suggestions.length === 0 && (
              <div style={{ marginTop: 16, borderTop: "1px solid #1e2130", paddingTop: 16 }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#4b5472", textTransform: "uppercase", letterSpacing: .8, marginBottom: 10 }}>Quick Select</div>
                <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                  {["IT Support", "CS Representative", "Full Stack Developer", "Data Analyst"].map(role => (
                    <button key={role} className="btn" onClick={() => setJobTitle(role)}
                      style={{ padding: "6px 14px", background: "#1a1d2a", border: "1px solid #252840", borderRadius: 20, color: "#dde2f0", fontSize: 12 }}>
                      {role}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <button className="btn" onClick={() => setStep(2)} disabled={!jobTitle.trim()}
              style={{ marginTop: 20, padding: "10px 24px", background: "#4f8ef7", color: "#fff", borderRadius: 8, fontWeight: 700, width: "100%" }}>
              Next: Location →
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="fade-in">
            <div style={{ fontSize: 11, fontWeight: 700, color: "#4f8ef7", textTransform: "uppercase", letterSpacing: .8, marginBottom: 12 }}>Step 2: Location</div>
            <p style={{ color: "#dde2f0", fontSize: 14, marginBottom: 16 }}>Preferred location (e.g., Marikina, QC, Rizal)?</p>
            <input className="inp" placeholder="e.g. Marikina, Quezon City, Rizal, Pasig..." value={location} onChange={e => setLocation(e.target.value)} autoFocus />
            <div style={{ marginTop: 16, borderTop: "1px solid #1e2130", paddingTop: 16 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#4b5472", textTransform: "uppercase", letterSpacing: .8, marginBottom: 10 }}>Popular Areas</div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {["Marikina", "Quezon City", "Rizal", "Pasig", "Makati"].map(loc => (
                  <button key={loc} className="btn" onClick={() => setLocation(loc)}
                    style={{ padding: "6px 14px", background: "#1a1d2a", border: "1px solid #252840", borderRadius: 20, color: "#dde2f0", fontSize: 12 }}>
                    {loc}
                  </button>
                ))}
              </div>
            </div>
            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button className="btn" onClick={() => setStep(1)} style={{ flex: 1, padding: "10px", background: "#1a1d2a", color: "#6b7590", borderRadius: 8, fontWeight: 600 }}>Back</button>
              <button className="btn" onClick={() => setStep(3)} disabled={!location.trim()} style={{ flex: 2, padding: "10px", background: "#4f8ef7", color: "#fff", borderRadius: 8, fontWeight: 700 }}>Next: Salary →</button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="fade-in">
            <div style={{ fontSize: 11, fontWeight: 700, color: "#4f8ef7", textTransform: "uppercase", letterSpacing: .8, marginBottom: 12 }}>Step 3: Expected Allowance</div>
            <p style={{ color: "#dde2f0", fontSize: 14, marginBottom: 16 }}>Monthly allowance or salary expectation?</p>
            <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
              <input className="inp" type="text" value={salary} onChange={e => setSalary(e.target.value)} style={{ flex: 2 }} />
              <select className="inp" value={frequency} onChange={e => setFrequency(e.target.value)} style={{ flex: 1 }}>
                <option>Monthly</option>
                <option>Hourly</option>
                <option>Annual</option>
              </select>
            </div>
            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button className="btn" onClick={() => setStep(2)} style={{ flex: 1, padding: "10px", background: "#1a1d2a", color: "#6b7590", borderRadius: 8, fontWeight: 600 }}>Back</button>
              <button className="btn" onClick={performAnalysis} disabled={loading} style={{ flex: 2, padding: "10px", background: "#2a9d8f", color: "#fff", borderRadius: 8, fontWeight: 700 }}>
                {loading ? "Matching with Local AI..." : "Find My OJT Match →"}
              </button>
            </div>
          </div>
        )}

        {step === 4 && analysis && (
          <div className="fade-in">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <div style={{ color: "#4b5472", fontSize: 12, fontWeight: 600, textTransform: "uppercase" }}>Recommended for you ({jobTitle})</div>
              <button className="btn" onClick={reset} style={{ color: "#4f8ef7", fontSize: 11, fontWeight: 700, background: "transparent" }}>NEW SEARCH</button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {analysis.jobs.map(job => (
                <div key={job.id} className="card" style={{ padding: "16px", background: "#13151f" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                    <div style={{ fontWeight: 700, color: "#dde2f0", fontSize: 15 }}>{job.name}</div>
                    <div style={{ color: "#e9c46a", fontSize: 13, fontWeight: 700 }}>⭐ {job.rating} <span style={{ color: "#4b5472", fontWeight: 400, fontSize: 11 }}>({job.reviews})</span></div>
                  </div>
                  <div style={{ fontSize: 12, color: "#4f8ef7", marginBottom: 12, fontWeight: 600 }}>{job.keyword}</div>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button className="btn" onClick={() => setSelectedJob(job)}
                      style={{ flex: 2, padding: "8px", background: "#1a1d2a", border: "1px solid #252840", color: "#dde2f0", borderRadius: 6, fontSize: 12, fontWeight: 600 }}>View Details</button>
                    <button className="btn" onClick={() => { setApplying(job.id); setTimeout(() => setApplying(null), 2000); }}
                      style={{ flex: 3, padding: "8px", background: applying === job.id ? "#2a9d8f" : "#4f8ef7", color: "#fff", borderRadius: 6, fontSize: 12, fontWeight: 700 }}>
                      {applying === job.id ? "✓ Applied" : "Quick Apply"}
                    </button>
                    <button className="btn" onClick={() => setSaved(p => p.includes(job.id) ? p.filter(id => id !== job.id) : [...p, job.id])}
                      style={{ flex: 1, background: "#1a1d2a", borderRadius: 6, color: saved.includes(job.id) ? "#e74c3c" : "#6b7590", fontSize: 14 }}>
                      {saved.includes(job.id) ? "❤️" : "🤍"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </Section>

      {selectedJob && (
        <div className="fade-in" style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.85)", zIndex: 600, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
          <div className="card slide-in" style={{ maxWidth: 450, width: "100%", padding: 24, background: "#13151f", border: "1px solid #252840" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
              <div>
                <h2 style={{ fontSize: 18, color: "#4f8ef7", fontWeight: 700 }}>{selectedJob.name}</h2>
                <div style={{ fontSize: 12, color: "#4b5472", marginTop: 2 }}>{location} · {selectedJob.posted}</div>
              </div>
              <div style={{ color: "#e9c46a", fontSize: 14, fontWeight: 700 }}>⭐ {selectedJob.rating}</div>
            </div>
            
            <div style={{ marginBottom: 20, borderTop: "1px solid #1e2130", paddingTop: 16 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: "#dde2f0", textTransform: "uppercase", letterSpacing: .8, marginBottom: 10 }}>OJT Requirements</div>
              <ul style={{ paddingLeft: 18, color: "#b0b8d4", fontSize: 13, lineHeight: 1.8 }}>
                {selectedJob.requirements.map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>

            <div style={{ background: "#1a1d2a", padding: 14, borderRadius: 10, marginBottom: 24, border: "1px solid #252840" }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: "#e9c46a", textTransform: "uppercase", marginBottom: 6 }}>Recent Intern Review</div>
              <div style={{ fontStyle: "italic", fontSize: 12.5, color: "#6b7590", lineHeight: 1.5 }}>"The mentorship here is excellent. I worked on real projects using {jobTitle} skills. Highly recommended for students in {location}!"</div>
            </div>

            <button className="btn" onClick={() => setSelectedJob(null)}
              style={{ width: "100%", padding: "12px", background: "#4f8ef7", color: "#fff", borderRadius: 8, fontWeight: 700 }}>Close Details</button>
          </div>
        </div>
      )}
    </div>
  );
}
