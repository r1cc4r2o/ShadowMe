<script>
    import VideoStream from '$lib/components/VideoStream.svelte';
    import Navbar from '$lib/components/Navbar.svelte';
    import MediapipeSettings from '$lib/components/MediapipeSettings.svelte';

    import { onMount } from 'svelte';

    let modelComplexity = 1;
    let smoothLandmarks = true;
    let minDetectionConfidence = 0.7;
    let minTrackingConfidence = 0.7;
    let refineFaceLandmarks = true;

	onMount(async () => {
	    await import('$lib/script/main.js');
	});
</script>

<Navbar showPlayPause/>

<VideoStream/>

<div class="hidden md:block">
    <MediapipeSettings/>
</div>