import { Camera } from '@mediapipe/camera_utils';
import { Holistic } from '@mediapipe/holistic';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import {
    POSE_CONNECTIONS,
    FACEMESH_TESSELATION,
    HAND_CONNECTIONS,
} from '@mediapipe/holistic'

/**
 * Class representing an instance of `mediapipe` PoseEstimator using
 * the `holistic` solution
 */
export class PoseEstimator {
    /**
     * Create a Pose Estimator using `mediapipe`
     * @param {*} videoElement - The HTML object to stream the video from
     * @param {*} guideCanvas - The canvas to draw on
     * @param {*} videoResolution  - The resolution to which the video stream will be scaled, as an array [width, height]
     */
    constructor(videoElement, guideCanvas, videoResolution) {
        this.videoElement = videoElement;
        this.guideCanvas = guideCanvas;
        this.videoResolution = videoResolution;
    }

    /**
     * Initialize the holistic model from mediapipe and set the callback function
     * @param {function} onResults - The callback function which will be called every time mediapipe makes new results available
     */
    setOnResults(onResults) {
        this.onResults = onResults;
    }

    /**
     * Initialize the holistic model from mediapipe
     */
    initializeHolistic() {
        this.holistic = new Holistic({
            locateFile: file => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic@0.5.1635989137/${file}`;
            }
        })

        // Model settings
        this.holistic.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.7,
            refineFaceLandmarks: true,
        })

        // Callback function
        this.holistic.onResults(this.onResults);
    }

    /**
     * Initialize the pose model from mediapipe
     */
    initializePose() {
        this.pose = new Pose({
            locateFile: file => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
            }
        })

        // Model settings
        this.pose.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.7,
        })

        // Callback function
        this.pose.onResults(this.onResults);
    }

    /**
     * Initialize the camera to capture real-time video
     */
    initializeCamera() {
        this.camera = new Camera(this.videoElement, {
            onFrame: async () => {
                await this.holistic.send({ image: this.videoElement });
                // await this.pose.send({ image: this.videoElement });
            },
            width: this.videoResolution[0],
            height: this.videoResolution[1]
        })
    }

    /**
     * Start real-time video acquisition
     */
    start() {
        this.initializeHolistic();
        // this.initializePose();
        this.initializeCamera();
        this.camera.start();
    }

    /**
     * Stop real-time video acquisition
     */
    stop() {
        this.camera.stop();
        this.clearCanvas();
    }

    /**
     * Clear the canvas on which markers are drawn. The canvas' context
     * is returned for further usage
     * @returns The canvas' usage
     */
    clearCanvas() {
        // Clear Canvas
        let canvasCtx = this.guideCanvas.getContext('2d');
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, this.guideCanvas.width, this.guideCanvas.height);

        return canvasCtx
    }

    /**
     * Draw landmarks on the video to display what mediapipe is processing
     * @param {*} results Results computed by mediapipe
     */
    drawResults(results) {
        this.guideCanvas.width = this.videoElement.videoWidth;
        this.guideCanvas.height = this.videoElement.videoHeight;
        
        let canvasCtx = this.clearCanvas();

        // Mediapipe drawing functions are utilized

        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
            color: "#00cff7",
            lineWidth: 4
        });
        drawLandmarks(canvasCtx, results.poseLandmarks, {
            color: "#ff0364",
            lineWidth: 2
        });
        drawConnectors(canvasCtx, results.faceLandmarks, FACEMESH_TESSELATION, {
            color: "#C0C0C070",
            lineWidth: 1
        });
        
        if (results.faceLandmarks && results.faceLandmarks.length === 478) {
            // Pupils
            drawLandmarks(canvasCtx, [results.faceLandmarks[468], results.faceLandmarks[468 + 5]], {
                color: "#ffe603",
                lineWidth: 2
            });
        }
        drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS, {
            color: "#eb1064",
            lineWidth: 5
        });
        drawLandmarks(canvasCtx, results.leftHandLandmarks, {
            color: "#00cff7",
            lineWidth: 2
        });
        drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS, {
            color: "#22c3e3",
            lineWidth: 5
        });
        drawLandmarks(canvasCtx, results.rightHandLandmarks, {
            color: "#ff0364",
            lineWidth: 2
        });
    }
}