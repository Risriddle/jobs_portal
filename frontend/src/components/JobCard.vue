<script setup>
defineProps({
  job: Object
});
import "../css/JobCard.css"

const emit = defineEmits(["delete", "duplicate", "edit"]);

/* Map status names to badge colour classes */
function statusClass(name = "") {
  const n = name.toLowerCase();
  if (n.includes("open") || n.includes("active"))  return "badge-green";
  if (n.includes("close") || n.includes("filled")) return "badge-slate";
  if (n.includes("draft"))                          return "badge-amber";
  return "badge-blue";
}
</script>

<template>
  <article class="job-card card">

    <!-- Accent bar (colour driven by first status) -->
    <span
      class="card-accent"
      :class="statusClass(job.status_details?.[0]?.name)"
    ></span>

    <!-- Header: avatar + title -->
    <div class="card-header">
      <div class="avatar">
        <img v-if="job.profile_picture" :src="job.profile_picture" alt="" />
        <span v-else class="avatar-fallback">{{ job.title?.charAt(0) }}</span>
      </div>
      <div class="card-title-group">
        <h2 class="card-title">{{ job.title }}</h2>
        <span class="card-location">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ job.city }}, {{ job.state }}
        </span>
      </div>
    </div>

    <!-- Description -->
    <p class="card-description">{{ job.description }}</p>

    <!-- Status badges -->
    <div v-if="job.status_details?.length" class="card-badges">
      <span
        v-for="s in job.status_details"
        :key="s.id"
        class="badge"
        :class="statusClass(s.name)"
      >{{ s.name }}</span>
    </div>

    <!-- Category tags -->
    <div v-if="job.category_details?.length" class="card-tags">
      <span
        v-for="c in job.category_details"
        :key="c.id"
        class="tag"
      >{{ c.name }}</span>
    </div>

    <!-- Divider -->
    <hr class="card-divider" />

    <!-- Actions -->
    <div class="card-actions">
      <button class="btn-ghost btn-sm" @click="emit('edit', job)">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        Edit
      </button>
      <button class="btn-ghost btn-sm" @click="emit('duplicate', job.id)">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        Duplicate
      </button>
      <button class="btn-danger btn-sm card-delete" @click="emit('delete', job.id)">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>
        Delete
      </button>
    </div>

  </article>
</template>
