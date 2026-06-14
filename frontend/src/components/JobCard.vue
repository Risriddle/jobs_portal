<script setup>
defineProps({
  job: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  "edit",
  "delete",
  "duplicate"
])
</script>

<template>
  <div class="job-card">

    <img
      v-if="job.profile_picture"
      :src="job.profile_picture"
      alt="Job"
      class="job-image"
    >

    <h2>{{ job.title }}</h2>

    <p>
      {{ job.description }}
    </p>

    <p>
      <strong>City:</strong>
      {{ job.city }}
    </p>

    <p>
      <strong>State:</strong>
      {{ job.state }}
    </p>

    <button @click="emit('edit', job)">
      Edit
    </button>

    <button @click="emit('delete', job.id)">
      Delete
    </button>

    <button @click="emit('duplicate', job.id)">
      Duplicate
    </button>

  </div>
</template>

<style scoped>
.job-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 16px;
}

.job-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
</style>