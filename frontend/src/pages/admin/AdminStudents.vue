<template>
  <div class="container mt-4">
    <h2>Manage Students</h2>
    <p>View and manage registered students.</p>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div class="mb-3 mt-3">
        <input
          type="text"
          class="form-control"
          v-model="searchQuery"
          placeholder="Search by name, branch, year or CGPA..."
        />
      </div>
      <table class="table mt-2">
      <thead>
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
        <tr v-if="filteredStudents.length === 0">
          <td colspan="7" class="text-center text-muted">No students match your search.</td>
        </tr>
        <tr v-for="(student, index) in filteredStudents" :key="student.id">
          <td>{{ index + 1 }}</td>
          <td>{{ student.name }}</td>
          <td>{{ student.branch }}</td>
          <td>{{ student.year }}</td>
          <td>{{ student.cgpa }}</td>
          <td>
            <span :class="statusBadgeClass(student)">
              {{ student.is_active ? 'active' : 'blacklisted' }}
            </span>
          </td>
          <td>
            <button
              v-if="student.is_active"
              class="btn btn-dark btn-sm me-2"
              :disabled="student._loading"
              @click="blacklistStudent(student)"
            >
              Blacklist
            </button>
            <button
              class="btn btn-danger btn-sm"
              :disabled="student._loading"
              @click="deleteStudent(student)"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { studentActiveBadgeClass } from "@/utils/ui";

export default {
  name: "AdminStudents",
  data() {
    return {
      students: [],
      loading: false,
      error: null,
      searchQuery: '',
    };
  },
  computed: {
    filteredStudents() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) return this.students;
      return this.students.filter(s =>
        (s.name || '').toLowerCase().includes(q) ||
        (s.branch || '').toLowerCase().includes(q) ||
        String(s.year ?? '').includes(q) ||
        String(s.cgpa ?? '').includes(q)
      );
    },
  },
  async mounted() {
    this.loading = true;
    try {
      this.students = await api.get("/students");
    } catch (err) {
      this.error = err.message || "Failed to load students.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    statusBadgeClass(student) {
      return studentActiveBadgeClass(student);
    },
    async blacklistStudent(student) {
      if (!confirm(`Blacklist student "${student.name}"?`)) return;
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
    async deleteStudent(student) {
      if (!confirm(`Delete student "${student.name}"? This cannot be undone.`)) return;
      student._loading = true;
      try {
        await api.delete(`/students/${student.id}`);
        this.students = this.students.filter((s) => s.id !== student.id);
      } catch (err) {
        alert(err.message || "Failed to delete student.");
        student._loading = false;
      }
    },
  },
};
</script>
