<template>
  <div class="container py-5" style="max-width:720px">
    <div class="card shadow-sm">
      <div class="card-body">

        <h3 class="text-center mb-4">Create Account</h3>

        <!-- ROLE SWITCH -->
        <ul class="nav nav-pills justify-content-center mb-4">
          <li class="nav-item">
            <button
              class="nav-link"
              :class="{active: role==='student'}"
              @click="role='student'"
            >
              Student
            </button>
          </li>

          <li class="nav-item ms-2">
            <button
              class="nav-link"
              :class="{active: role==='company'}"
              @click="role='company'"
            >
              Company
            </button>
          </li>
        </ul>

        <form @submit.prevent="register">

          <div class="row g-3">

            <!-- USER FIELDS -->

            <div class="col-md-6">
              <label class="form-label">Name</label>
              <input v-model="name" class="form-control" required>
            </div>

            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input v-model="email" type="email" class="form-control" required>
            </div>

            <div class="col-md-6">
                <label class="form-label">Password</label>

                <div class="d-flex">
                    <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    required
                    >

                    <button
                    type="button"
                    class="btn btn-outline-secondary ms-2"
                    @click="showPassword = !showPassword"
                    >
                    👁
                    </button>
                </div>
            </div>

            <div class="col-md-6">
                <label class="form-label">Confirm Password</label>

                <div class="d-flex">
                    <input
                    v-model="confirmPassword"
                    :type="showConfirm ? 'text' : 'password'"
                    class="form-control"
                    required
                    >

                    <button
                    type="button"
                    class="btn btn-outline-secondary ms-2"
                    @click="showConfirm = !showConfirm"
                    >
                    👁
                    </button>
                </div>
            </div>
            <!-- STUDENT FIELDS -->

            <template v-if="role==='student'">

              <div class="col-md-6">
                <label class="form-label">Branch</label>
                <input v-model="branch" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">Year</label>
                <input v-model="year" type="number" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">CGPA</label>
                <input v-model="cgpa" type="number" step="0.01" class="form-control">
              </div>

            </template>

            <!-- COMPANY FIELDS -->

            <template v-if="role==='company'">

              <div class="col-md-6">
                <label class="form-label">Company Name</label>
                <input v-model="company_name" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">Industry</label>
                <input v-model="industry" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">Location</label>
                <input v-model="location" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">Website</label>
                <input v-model="website" class="form-control">
              </div>

              <div class="col-md-6">
                <label class="form-label">HR Contact</label>
                <input v-model="hr_contact" class="form-control">
              </div>

            </template>

            <div class="col-12 text-danger" v-if="error">
              {{error}}
            </div>

            <div class="col-12 d-grid">
              <button class="btn btn-primary" :disabled="loading">
                {{ loading ? "Registering..." : "Register" }}
              </button>
            </div>

            <div class="text-center mt-3">
              Already have an account?
              <router-link to="/login">Login</router-link>
            </div>

          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api"

export default {

  data(){
    return{

      role:"student",

      name:"",
      email:"",
      password:"",
      showPassword: false,
      confirmPassword:"",
      showConfirm: false,

      branch:"",
      year:"",
      cgpa:"",

      company_name:"",
      industry:"",
      location:"",
      website:"",
      hr_contact:"",

      loading:false,
      error:""
    }
  },

  methods:{

    async register(){

      this.error=""

      if(this.password!==this.confirmPassword){
        this.error="Passwords do not match"
        return
      }

      this.loading=true

      try{

        let payload={
          name:this.name,
          email:this.email,
          password:this.password,
          role:this.role
        }

        if(this.role==="student"){
          payload.branch = this.branch
          payload.year = this.year
          payload.cgpa = this.cgpa
        }

        if(this.role==="company"){
          payload.company_name = this.company_name
          payload.industry = this.industry
          payload.location = this.location
          payload.website = this.website
          payload.hr_contact = this.hr_contact
        }

        await api.post("/auth/register",payload)

        alert("Registration successful")
        this.$router.push("/login")

      }
      catch(err){

        this.error="Registration failed"

      }
      finally{
        this.loading=false
      }

    }

  }

}
</script>