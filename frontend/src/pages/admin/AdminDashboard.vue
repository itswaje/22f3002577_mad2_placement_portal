<template>
  <div class="container mt-4">
    <h2>Welcome, Admin</h2>
    <p>Overview of the placement portal.</p>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>

      <!-- Stat Cards -->
      <div class="row mt-4 g-3">
        <div class="col-md-4">
          <div class="card text-center p-3">
            <h6 class="text-muted">Total Students</h6>
            <p class="fs-2 fw-bold mb-0">{{ stats.students ?? 0 }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-center p-3">
            <h6 class="text-muted">Total Companies</h6>
            <p class="fs-2 fw-bold mb-0">{{ stats.companies ?? 0 }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-center p-3">
            <h6 class="text-muted">Total Drives</h6>
            <p class="fs-2 fw-bold mb-0">{{ stats.drives ?? 0 }}</p>
          </div>
        </div>
      </div>

      <!-- Registered Companies -->
      <div class="mt-5">
        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
          <h5 class="mb-0">Registered Companies</h5>
          <div class="d-flex gap-2 align-items-center">
            <input
              type="text"
              class="form-control form-control-sm"
              style="min-width:220px"
              v-model="companySearch"
              placeholder="Search companies..."
            />
            <router-link to="/admin/companies" class="btn btn-outline-secondary btn-sm">View All</router-link>
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Company</th>
              <th>Industry</th>
              <th>HR Contact</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDashboardCompanies.length === 0">
              <td colspan="6" class="text-center text-muted">No companies match your search.</td>
            </tr>
            <tr v-for="(company, i) in filteredDashboardCompanies" :key="company.id">
              <td>{{ i + 1 }}</td>
              <td>{{ company.company_name }}</td>
              <td>{{ company.industry }}</td>
              <td>{{ company.hr_contact }}</td>
              <td><span :class="statusBadge(company.status)">{{ company.status }}</span></td>
              <td>
                <template v-if="company.status === 'pending'">
                  <button class="btn btn-success btn-sm me-1" :disabled="company._loading" @click="approveCompany(company)">Approve</button>
                  <button class="btn btn-danger btn-sm" :disabled="company._loading" @click="rejectCompany(company)">Reject</button>
                </template>
                <button
                  v-else-if="company.status !== 'blacklisted'"
                  class="btn btn-dark btn-sm"
                  :disabled="company._loading"
                  @click="blacklistCompany(company)"
                >
                  Blacklist
                </button>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Registered Students -->
      <div class="mt-5">
        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
          <h5 class="mb-0">Registered Students</h5>
          <div class="d-flex gap-2 align-items-center">
            <input
              type="text"
              class="form-control form-control-sm"
              style="min-width:220px"
              v-model="studentSearch"
              placeholder="Search students..."
            />
            <router-link to="/admin/students" class="btn btn-outline-secondary btn-sm">View All</router-link>
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Branch</th>
              <th>Year</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDashboardStudents.length === 0">
              <td colspan="7" class="text-center text-muted">No students match your search.</td>
            </tr>
            <tr v-for="(student, i) in filteredDashboardStudents" :key="student.id">
              <td>{{ i + 1 }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.branch }}</td>
              <td>{{ student.year }}</td>
              <td>{{ student.cgpa }}</td>
              <td>
                <span :class="studentStatusBadge(student)">
                  {{ student.is_active ? 'active' : 'blacklisted' }}
                </span>
              </td>
              <td>
                <button
                  v-if="student.is_active"
                  class="btn btn-dark btn-sm"
                  :disabled="student._loading"
                  @click="blacklistStudent(student)"
                >
                  Blacklist
                </button>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pending Drive Requests -->
      <div class="mt-5">
        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
          <h5 class="mb-0">Company Drive Requests</h5>
          <div class="d-flex gap-2 align-items-center">
            <input
              type="text"
              class="form-control form-control-sm"
              style="min-width:220px"
              v-model="driveRequestSearch"
              placeholder="Search drive requests..."
            />
            <router-link to="/admin/drives" class="btn btn-outline-secondary btn-sm">View All</router-link>
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Salary (₹)</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDashboardRequests.length === 0">
              <td colspan="7" class="text-center text-muted">No drive requests match your search.</td>
            </tr>
            <tr v-for="(req, i) in filteredDashboardRequests" :key="req.id">
              <td>{{ i + 1 }}</td>
              <td>{{ companyName(req.data?.company_id) }}</td>
              <td>{{ req.data?.job_title }}</td>
              <td>{{ req.data?.salary?.toLocaleString() ?? '—' }}</td>
              <td>{{ req.data?.application_deadline }}</td>
              <td><span :class="statusBadge(req.status)">{{ req.status }}</span></td>
              <td>
                <template v-if="req.status === 'pending'">
                  <button class="btn btn-success btn-sm me-1" :disabled="req._loading" @click="approveDrive(req)">Approve</button>
                  <button class="btn btn-danger btn-sm" :disabled="req._loading" @click="rejectDrive(req)">Reject</button>
                </template>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Ongoing Drives -->
      <div class="mt-5">
        <div class="d-flex align-items-center gap-3 mb-2 flex-wrap">
          <h5 class="mb-0">Ongoing Drives</h5>
          <input
            type="text"
            class="form-control form-control-sm"
            style="max-width: 260px"
            v-model="driveSearch"
            placeholder="Search drives..."
          />
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Drive Name</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Deadline</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDashboardDrives.length === 0">
              <td colspan="6" class="text-center text-muted">No drives match your search.</td>
            </tr>
            <tr v-for="(drive, i) in filteredDashboardDrives" :key="drive.id">
              <td>{{ i + 1 }}</td>
              <td>{{ drive.drive_name }}</td>
              <td>{{ companyName(drive.company_id) }}</td>
              <td>{{ drive.job_title }}</td>
              <td>{{ drive.application_deadline }}</td>
              <td><span :class="statusBadge(drive.status)">{{ drive.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Student Applications -->
      <div class="mt-5 mb-5">
        <div class="d-flex align-items-center gap-3 mb-2 flex-wrap">
          <h5 class="mb-0">Student Applications</h5>
          <input
            type="text"
            class="form-control form-control-sm"
            style="max-width: 260px"
            v-model="appSearch"
            placeholder="Search applications..."
          />
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Student</th>
              <th>Drive</th>
              <th>Company</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredDashboardApps.length === 0">
              <td colspan="5" class="text-center text-muted">No applications match your search.</td>
            </tr>
            <tr v-for="(app, i) in filteredDashboardApps" :key="app.id">
              <td>{{ i + 1 }}</td>
              <td>{{ studentName(app.student_id) }}</td>
              <td>{{ driveName(app.drive_id) }}</td>
              <td>{{ driveCompany(app.drive_id) }}</td>
              <td>
                <span :class="statusBadge(resolveApplicationStatus(app))">{{ resolveApplicationStatus(app) }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { lifecycleStatusBadgeClass, studentActiveBadgeClass, applicationStatusBadgeClass } from "@/utils/ui";

export default {
  name: "AdminDashboard",
  data() {
    return {
      loading: false,
      error: null,
      stats: {},
      companies: [],
      students: [],
      requests: [],
      drives: [],
      applications: [],
      companyMap: {},
      studentMap: {},
      driveMap: {},
      companySearch: '',
      studentSearch: '',
      driveRequestSearch: '',
      driveSearch: '',
      appSearch: '',
    };
  },
  computed: {
    filteredDashboardCompanies() {
      const q = this.companySearch.trim().toLowerCase();
      if (!q) return this.companies;
      return this.companies.filter(c =>
        (c.company_name || '').toLowerCase().includes(q) ||
        (c.industry || '').toLowerCase().includes(q) ||
        (c.status || '').toLowerCase().includes(q)
      );
    },
    filteredDashboardStudents() {
      const q = this.studentSearch.trim().toLowerCase();
      if (!q) return this.students;
      return this.students.filter(s =>
        (s.name || '').toLowerCase().includes(q) ||
        (s.branch || '').toLowerCase().includes(q) ||
        String(s.cgpa ?? '').includes(q)
      );
    },
    filteredDashboardRequests() {
      const q = this.driveRequestSearch.trim().toLowerCase();
      if (!q) return this.requests;
      return this.requests.filter(r =>
        (this.companyName(r.data?.company_id)).toLowerCase().includes(q) ||
        (r.data?.job_title || '').toLowerCase().includes(q) ||
        (r.status || '').toLowerCase().includes(q)
      );
    },
    filteredDashboardDrives() {
      const q = this.driveSearch.trim().toLowerCase();
      if (!q) return this.drives;
      return this.drives.filter(d =>
        (d.drive_name || '').toLowerCase().includes(q) ||
        (this.companyName(d.company_id)).toLowerCase().includes(q) ||
        (d.job_title || '').toLowerCase().includes(q) ||
        (d.status || '').toLowerCase().includes(q)
      );
    },
    filteredDashboardApps() {
      const q = this.appSearch.trim().toLowerCase();
      if (!q) return this.applications;
      return this.applications.filter(app =>
        (this.studentName(app.student_id)).toLowerCase().includes(q) ||
        (this.driveName(app.drive_id)).toLowerCase().includes(q) ||
        (this.driveCompany(app.drive_id)).toLowerCase().includes(q) ||
        (this.resolveApplicationStatus(app) || '').toLowerCase().includes(q)
      );
    },
  },
  async mounted() {
    this.loading = true;
    try {
      const [stats, companies, students, requests, drives, applications] =
        await Promise.all([
          api.get("/admin/dashboard"),
          api.get("/companies"),
          api.get("/students"),
          api.get("/admin/requests"),
          api.get("/drives"),
          api.get("/applications"),
        ]);

      this.stats = stats;
      this.companies = companies;
      this.students = students;
      this.requests = requests;
      this.drives = drives;
      this.applications = applications;

      companies.forEach((c) => {
        this.companyMap[c.id] = c.company_name;
      });
      students.forEach((s) => {
        this.studentMap[s.id] = s.name;
      });
      drives.forEach((d) => {
        this.driveMap[d.id] = {
          name: d.drive_name,
          company_id: d.company_id,
          status: d.status,
        };
      });
    } catch (err) {
      this.error = err.message || "Failed to load dashboard data.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    statusBadge(status) {
      const normalizedStatus = String(status ?? "").toLowerCase();
      if (["applied", "shortlisted", "selected", "waiting", "rejected", "cancelled"].includes(normalizedStatus)) {
        return ["badge", applicationStatusBadgeClass(normalizedStatus)];
      }
      return lifecycleStatusBadgeClass(normalizedStatus);
    },
    resolveApplicationStatus(application) {
      if (this.driveMap[application?.drive_id]?.status === "cancelled") {
        return "cancelled";
      }
      return application?.status || "applied";
    },
    studentStatusBadge(student) {
      return studentActiveBadgeClass(student);
    },
    companyName(id) {
      return this.companyMap[id] ?? `Company #${id}`;
    },
    studentName(id) {
      return this.studentMap[id] ?? `Student #${id}`;
    },
    driveName(id) {
      return this.driveMap[id]?.name ?? `Drive #${id}`;
    },
    driveCompany(driveId) {
      const companyId = this.driveMap[driveId]?.company_id;
      return companyId ? this.companyName(companyId) : "—";
    },

    // Company approve/reject
    async approveCompany(company) {
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/approve`, {});
        company.status = "approved";
        this.stats.companies = (this.stats.companies ?? 0);
      } catch (err) {
        alert(err.message || "Failed to approve company.");
      } finally {
        company._loading = false;
      }
    },
    async rejectCompany(company) {
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/reject`, {});
        company.status = "rejected";
      } catch (err) {
        alert(err.message || "Failed to reject company.");
      } finally {
        company._loading = false;
      }
    },
    async blacklistCompany(company) {
      if (!confirm(`Blacklist company "${company.company_name}"? This will cancel all active drives.`)) {
        return;
      }
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/blacklist`, {});
        company.status = "blacklisted";
        this.drives = this.drives.map((d) =>
          d.company_id === company.id && d.status !== "closed" ? { ...d, status: "cancelled" } : d
        );
      } catch (err) {
        alert(err.message || "Failed to blacklist company.");
      } finally {
        company._loading = false;
      }
    },
    async blacklistStudent(student) {
      if (!confirm(`Blacklist student "${student.name}"?`)) {
        return;
      }
      student._loading = true;
      try {
        await api.patch(`/admin/students/${student.id}/blacklist`, {});
        student.is_active = false;
      } catch (err) {
        alert(err.message || "Failed to blacklist student.");
      } finally {
        student._loading = false;
      }
    },

    // Drive request approve/reject
    async approveDrive(req) {
      req._loading = true;
      try {
        await api.patch(`/admin/drives/${req.id}/approve`, {});
        req.status = "approved";
        // reload drives so the new drive appears in Ongoing Drives
        this.drives = await api.get("/drives");
        this.drives.forEach((d) => {
          this.driveMap[d.id] = { name: d.drive_name, company_id: d.company_id };
        });
        this.stats.drives = this.drives.length;
      } catch (err) {
        alert(err.message || "Failed to approve drive request.");
      } finally {
        req._loading = false;
      }
    },
    async rejectDrive(req) {
      req._loading = true;
      try {
        await api.patch(`/admin/drives/${req.id}/reject`, {});
        req.status = "rejected";
      } catch (err) {
        alert(err.message || "Failed to reject drive request.");
      } finally {
        req._loading = false;
      }
    },
  },
};
</script>
