<script lang="ts">
  import { onMount } from 'svelte';
  import type { SensorReading } from '$lib/types';

  let currentReading = $state<SensorReading | null>(null);
  let eventSource = $state<EventSource | undefined>(undefined);

  onMount(async () => {
    // Initial data fetch
    const response = await fetch('http://localhost:8000/current');
    currentReading = await response.json();

    // Set up SSE connection
    eventSource = new EventSource('http://localhost:8000/stream');
    eventSource.addEventListener('sensor_update', (event) => {
      currentReading = JSON.parse(event.data);
    });

    return () => {
      if (eventSource) eventSource.close();
    };
  });
</script>

<main class="container">
  <h1>Sensor Dashboard</h1>

  {#if currentReading}
    <div class="dashboard-grid">
      <div class="card">
        <h2>Temperature</h2>
        <p class="reading">{currentReading.temperature}°C</p>
      </div>

      <div class="card">
        <h2>Humidity</h2>
        <p class="reading">{currentReading.humidity}%</p>
      </div>

      <div class="card">
        <h2>Status</h2>
        <p class="status {currentReading.status}">{currentReading.status}</p>
      </div>
    </div>
  {/if}
</main>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .card {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .reading {
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem 0;
  }

  .status {
    text-transform: uppercase;
    font-weight: bold;
  }

  .status.normal { color: #2ecc71; }
  .status.warning { color: #f1c40f; }
  .status.critical { color: #e74c3c; }
</style>