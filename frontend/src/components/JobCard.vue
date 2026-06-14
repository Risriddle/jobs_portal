<script setup>
defineProps({
  job: {
    type: Object,
    required: true
  }
});

const emit = defineEmits([
  "delete",
  "duplicate"
]);
</script>

<template>
  <div class="card">

    <img
      v-if="job.profile_picture"
      :src="job.profile_picture"
      alt="job"
      class="image"
    >

    <h2>{{ job.title }}</h2>

    <p>
      {{ job.description }}
    </p>

    <div class="section">
      <strong>Location:</strong>
      {{ job.city }}, {{ job.state }}
    </div>

    <div class="section">
      <strong>Status:</strong>

      <span
        v-for="status in job.status_details"
        :key="status.id"
        class="badge"
      >
        {{ status.name }}
      </span>
    </div>

    <div class="section">
      <strong>Category:</strong>

      <span
        v-for="category in job.category_details"
        :key="category.id"
        class="badge"
      >
        {{ category.name }}
      </span>
    </div>

    <div class="actions">

      <button
        @click="emit('duplicate', job.id)"
      >
        Duplicate
      </button>

      <button
        @click="emit('delete', job.id)"
      >
        Delete
      </button>

    </div>

  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
}

.image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.section {
  margin-top: 12px;
}

.badge {
  display: inline-block;
  margin: 4px;
  padding: 4px 8px;
  border-radius: 8px;

  background: #efefef;

  color: #111;
  border: 1px solid #ccc;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}
</style>