import { PoseEstimator } from "./pose-estimator.js";
import { CharacterLoader } from "./character-loader.js";
import { CharacterScene } from "./character-scene.js";
import { get } from "svelte/store";
import {
    modelComplexity,
    smoothLandmarks,
    minDetectionConfidence,
    minTrackingConfidence,
    refineFaceLandmarks
} from "$lib/script/stores.js";


/**
 * Play-Pause Button
 */

var isPause = false;

var playPauseButton = document.querySelector('#play-pause-button');
playPauseButton.onclick = () => {
    clickHandler()
}

var aboutButton = document.querySelector('#about-button');
aboutButton.onclick = () => {
    clickHandler()
}

function clickHandler() {
    if (isPause) {
        start();
    } else {
        pause();
    }

    isPause = !isPause;
}

function pause() {
    playPauseButton.firstChild.setAttribute('src', '/play.png');

    characterScene.stop();
    poseEstimator.stop();
}

function start() {
    playPauseButton.firstChild.setAttribute('src', '/pause.png')

    // Re-initialize the scene and re-load the character
    characterScene.start()
    characterScene.setup();
    characterLoader.load((character) => {
        characterScene.addCharacter(character)
    })

    // Re-initialize the pose estimator
    poseEstimator = new PoseEstimator(videoElement, guideCanvas, [640, 480]);
    poseEstimator.setOnResults((results) => {
        // Add landmarks on top of video stream
        poseEstimator.drawResults(results);

        // Model animation
        characterScene.characterAnimator.animateCharacter(results);
    })
    poseEstimator.start();
}


/**
 * Pose Estimation and 3D Rendering
 */

// UI Elements
let videoElement = document.querySelector('.input-video');
videoElement.setAttribute('autoplay', '');
videoElement.setAttribute('muted', '');
videoElement.setAttribute('playsinline', '')
let guideCanvas = document.querySelector('canvas.guides');

// Setup 3D scene
var characterScene = new CharacterScene(videoElement)
characterScene.start()

// Setup pose estimator
var poseEstimator = new PoseEstimator(videoElement, guideCanvas, [640, 480])
poseEstimator.setOnResults((results) => {
    // Add landmarks on top of video stream
    poseEstimator.drawResults(results);

    // Model animation
    characterScene.characterAnimator.animateCharacter(results);
})
poseEstimator.start();

// Load the character
var characterLoader = new CharacterLoader('/models/vrm_test.vrm');
characterLoader.load((character) => {
    characterScene.addCharacter(character)
})


/**
 * Model Updaters (responding to UI changes)
 */

function updatePoseEstimatorModel() {
    poseEstimator.holistic.setOptions({
        modelComplexity: get(modelComplexity),
        smoothLandmarks: get(smoothLandmarks),
        minDetectionConfidence: get(minDetectionConfidence),
        minTrackingConfidence: get(minTrackingConfidence),
        refineFaceLandmarks: get(refineFaceLandmarks),
    })
}

modelComplexity.subscribe(value => {
    updatePoseEstimatorModel()
})
smoothLandmarks.subscribe(value => {
    updatePoseEstimatorModel()
})
minDetectionConfidence.subscribe(value => {
    updatePoseEstimatorModel()
})
minTrackingConfidence.subscribe(value => {
    updatePoseEstimatorModel()
})
refineFaceLandmarks.subscribe(value => {
    updatePoseEstimatorModel()
})