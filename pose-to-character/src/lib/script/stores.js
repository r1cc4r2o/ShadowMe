import { writable } from 'svelte/store';

function createCount() {
	const { subscribe, set, update } = writable(0);

	return {
		subscribe,
		reset: () => set(0)
	};
}

// export const count = createCount();
export const modelComplexity = writable(1);
export const smoothLandmarks = writable(true);
export const minDetectionConfidence = writable(0.7);
export const minTrackingConfidence = writable(0.7);
export const refineFaceLandmarks = writable(true);