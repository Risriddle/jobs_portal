<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import "../css/Analytics.css"
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from "chart.js";

import { Pie, Bar } from "vue-chartjs";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const statusChart = ref(null);
const cityChart   = ref(null);
const stateChart  = ref(null);
const loading     = ref(true);

/* Shared chart palette */
const PALETTE = [
  "#3b82f6", "#f59e0b", "#22c55e", "#a855f7",
  "#ef4444", "#06b6d4", "#f97316", "#64748b"
];

const barOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 15
        }
      }
    },
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1, 
        precision: 0 
      },
      grid: {
        color: "rgba(100,116,139,0.1)"
      }
    }
  }
};

const pieOptions = {
  responsive: true,
  plugins: {
    legend: { position: "bottom", labels: { padding: 16, font: { size: 15 } } }
  }
};

async function fetchAnalytics() {
  try {
    const response = await api.get("/analytics/");
    const data = response.data;

    statusChart.value = {
      labels: data.status_distribution.map(i => i.name),
      datasets: [{
        data: data.status_distribution.map(i => i.total),
        backgroundColor: PALETTE,
        borderWidth: 2,
        borderColor: "#fff"
      }]
    };

    cityChart.value = {
      labels: data.city_distribution.map(i => i.city),
      datasets: [{
        label: "Jobs",
        data: data.city_distribution.map(i => i.total),
        backgroundColor: PALETTE[0],
        borderRadius: 6,
        borderSkipped: false,
        maxBarThickness:30,
        categoryPercentage:0.7,
        barPercentage:0.8
      }]
    };

    stateChart.value = {
      labels: data.state_distribution.map(i => i.state),
      datasets: [{
        label: "Jobs",
        data: data.state_distribution.map(i => i.total),
        backgroundColor: PALETTE[1],
        borderRadius: 6,
        borderSkipped: false,
        maxBarThickness:30,
        categoryPercentage:0.7,
        barPercentage:0.8
      }]
    };

  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAnalytics);
</script>

<template>
  <div class="analytics-page">

    <!-- Top bar -->
    <header class="topbar">
      <div class="topbar-brand">
        <span class="topbar-logo">&#9670;</span>
        <span class="topbar-title">JobBoard</span>
      </div>
      <router-link to="/" class="nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        Back to Dashboard
      </router-link>
    </header>

    <main class="page-content">

      <div class="page-heading">
        <h1>Analytics</h1>
        <p class="page-subtitle">Visual breakdown of your job listings</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-wrap">
        <div class="spinner"></div>
        <span>Crunching the numbers…</span>
      </div>

      <!-- Charts -->
      <div v-else class="charts-grid">

        <!-- Status distribution (Pie) -->
        <div class="chart-card card">
          <div class="chart-card-header">
            <h2>Status Distribution</h2>
            <p class="chart-subtitle">Breakdown of listing statuses</p>
          </div>
          <div class="pie-wrap">
            <Pie :data="statusChart" :options="pieOptions" />
          </div>
        </div>

        <!-- City distribution (Bar) -->
        <div class="chart-card card">
          <div class="chart-card-header">
            <h2>Jobs by City</h2>
            <p class="chart-subtitle">Top cities with active listings</p>
          </div>
          <Bar :data="cityChart" :options="barOptions" />
        </div>

        <!-- State distribution (Bar) -->
        <div class="chart-card card">
          <div class="chart-card-header">
            <h2>Jobs by State</h2>
            <p class="chart-subtitle">Regional distribution of listings</p>
          </div>
          <Bar :data="stateChart" :options="barOptions" />
        </div>

      </div>

    </main>
  </div>
</template>

