<script>
    import Slider from '$lib/components/Slider.svelte';
    import Checkbox from '$lib/components/Checkbox.svelte';
    import {
        modelComplexity,
        smoothLandmarks,
        minDetectionConfidence,
        minTrackingConfidence,
        refineFaceLandmarks
    } from '$lib/script/stores.js';
</script>

<div class="bg-emerald-100 p-5 rounded-2xl fixed bottom-20 left-5">
    <div>
        <span>Model Complexity</span>
        <Slider bind:value={$modelComplexity} min=0 max=2 step=1/>
        {$modelComplexity}
    </div>

    <div>
        <span>Min Detection Confidence</span>
        <Slider bind:value={$minDetectionConfidence} min=0 max=1 step=0.01/>
        {$minDetectionConfidence}
    </div>

    <div>
        <span>Min Tracking Confidence</span>
        <Slider bind:value={$minTrackingConfidence} min=0 max=1 step=0.01/>
        {$minTrackingConfidence}
    </div>

    <div>
        <span>Smooth Landmarks</span>
        <Checkbox bind:value={$smoothLandmarks}/>
    </div>

    <div>
        <span>Refine Face Landmarks</span>
        <Checkbox bind:value={$refineFaceLandmarks}/>
    </div>
</div>