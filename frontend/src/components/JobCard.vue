<script setup>
defineProps({
  job: Object
});

const emit = defineEmits(["delete", "duplicate", "edit"]);
</script>

<template>
  <div class="card">

    <img v-if="job.profile_picture" :src="job.profile_picture" />

    <h2>{{ job.title }}</h2>

    <p>{{ job.description }}</p>

    <div>
      <strong>Location:</strong>
      {{ job.city }}, {{ job.state }}
    </div>

    <div>
      <span v-for="s in job.status_details" :key="s.id">
        {{ s.name }}
      </span>
    </div>

    <div>
      <span v-for="c in job.category_details" :key="c.id">
        {{ c.name }}
      </span>
    </div>

    <button @click="emit('edit', job)">
      Edit
    </button>

    <button @click="emit('duplicate', job.id)">
      Duplicate
    </button>

    <button @click="emit('delete', job.id)">
      Delete
    </button>

  </div>
</template>