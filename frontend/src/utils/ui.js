export function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;
  return d.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function applicationStatusBadgeClass(status) {
  const map = {
    applied: "bg-secondary",
    shortlisted: "bg-info text-dark",
    selected: "bg-success",
    rejected: "bg-danger",
    pending: "bg-warning text-dark",
    cancelled: "bg-dark",
    waiting: "bg-warning text-dark",
  };
  return map[String(status || "").toLowerCase()] || "bg-secondary";
}

export function lifecycleStatusBadgeClass(status) {
  return {
    badge: true,
    "bg-warning text-dark": status === "pending",
    "bg-success": status === "approved",
    "bg-danger": status === "rejected",
    "bg-dark": status === "blacklisted" || status === "closed",
    "bg-secondary": status === "cancelled",
  };
}

export function studentActiveBadgeClass(student) {
  return {
    badge: true,
    "bg-success": !!student?.is_active,
    "bg-dark": !student?.is_active,
  };
}
