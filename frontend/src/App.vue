<script setup>
import JobCard from "./components/JobCard.vue"
import { ref, onMounted } from "vue";
import api from "./services/api";
import JobForm from "./components/JobForm.vue"

const showModal = ref(false);

const jobs = ref([]);
const loading = ref(true);

async function fetchJobs() {
  try {
    const response = await api.get("/jobs/");
    jobs.value = response.data;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchJobs();
});
</script>

<template>
  <div>

    <h1>Job Dashboard</h1>
 
<button @click="showModal = true">
  Post Job
</button>

    <div v-if="loading">
      Loading...
    </div>



    <div
      v-else
      class="grid"
    >
      <JobCard
        v-for="job in jobs"
        :key="job.id"
        :job="job"
      />
    
<JobForm
  v-if="showModal"
  @close="showModal = false"
  @created="fetchJobs"
/>
    </div>

  </div>
</template>
<style>
.grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(300px, 1fr));

  gap: 20px;
}
</style>