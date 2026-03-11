import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores/user";

import HomePage from "@/pages/HomePage.vue";
import Login from "@/pages/Login.vue";
import Register from "@/pages/Register.vue";

// Admin pages
import AdminDashboard from "@/pages/admin/AdminDashboard.vue";
import AdminCompanies from "@/pages/admin/AdminCompanies.vue";
import AdminDrives from "@/pages/admin/AdminDrives.vue";
import AdminStudents from "@/pages/admin/AdminStudents.vue";

// Company pages
import CompanyDashboard from "@/pages/company/CompanyDashboard.vue";
import CompanyApplications from "@/pages/company/CompanyApplications.vue";
import CreateDrive from "@/pages/company/CreateDrive.vue";

// Student pages
import StudentDashboard from "@/pages/student/StudentDashboard.vue";
import DriveList from "@/pages/student/DriveList.vue";
import DriveDetails from "@/pages/student/DriveDetails.vue";
import ApplicationHistory from "@/pages/student/ApplicationHistory.vue";
import StudentEditProfile from "@/pages/student/StudentEditProfile.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // Public Routes
    { path: "/", redirect: "/homepage" },
    { path: "/homepage", component: HomePage },
    { path: "/login", component: Login },
    { path: "/register", component: Register },

    // Student Routes
    { path: "/student/dashboard", component: StudentDashboard },
    { path: "/student/edit-profile", component: StudentEditProfile },
    { path: "/student/drives", component: DriveList },
    { path: "/student/drives/:id", component: DriveDetails },
    { path: "/student/applications", component: ApplicationHistory },

    // Company Routes
    { path: "/company/dashboard", component: CompanyDashboard },
    { path: "/company/applications", component: CompanyApplications },
    { path: "/company/create-drive", component: CreateDrive },

    // Admin Routes
    { path: "/admin/dashboard", component: AdminDashboard },
    { path: "/admin/companies", component: AdminCompanies },
    { path: "/admin/drives", component: AdminDrives },
    { path: "/admin/students", component: AdminStudents },
  ],
});

router.beforeEach((to, from, next) => {
  const user = useUserStore();

  // Redirect already-authenticated users away from login/register
  if ((to.path === "/login" || to.path === "/register") && user.isAuthenticated) {
    if (user.isAdmin) return next("/admin/dashboard");
    if (user.isCompany) return next("/company/dashboard");
    return next("/student/dashboard");
  }

  if (to.path.startsWith("/admin") && !user.isAdmin) return next("/login");
  if (to.path.startsWith("/student") && !user.isStudent) return next("/login");
  if (to.path.startsWith("/company") && !user.isCompany) return next("/login");

  next();
});

export default router;