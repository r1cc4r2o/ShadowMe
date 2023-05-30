<script>
    export let min = 0;
    export let max = 1;
    export let step;
    export let value;
</script>

{#if !step}
    <input type="range" min={min} max={max} bind:value
        class="h-4 bg-emerald-300 rounded-lg appearance-none cursor-pointer"
    />
{:else}
    <input type="range" min={min} max={max} step={step} bind:value
        class="h-4 bg-emerald-300 rounded-lg appearance-none cursor-pointer"
    />
{/if}