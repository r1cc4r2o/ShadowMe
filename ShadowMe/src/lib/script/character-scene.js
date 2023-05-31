import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { CharacterAnimator } from "./character-animator.js";

/**
 * Class representing a 3D scene with a character inside it
 */
export class CharacterScene {
    /**
     * Create a Character Scene given the video element, which is stored for later usage
     * @param {*} videoElement The HTML element from which video is being streamed
     */
    constructor(videoElement) {
        this.setup()

        // Store videoElement for later usage
        this.videoElement = videoElement
    }

    /**
     * Setup the 3D scene using three.js. The camera, controls and lights are setup, too.
     */
    setup() {
        // Setup Renderer
        this.renderer = new THREE.WebGLRenderer({ alpha: true, powerPreference: "high-performance" });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(this.renderer.domElement);

        // Setup Camera
        this.orbitCamera = new THREE.PerspectiveCamera(35, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.orbitCamera.position.set(0.0, 1.4, 0.7);

        // Setup Controls
        this.orbitControls = new OrbitControls(this.orbitCamera, this.renderer.domElement);
        this.orbitControls.screenSpacePanning = true;
        this.orbitControls.target.set(0.0, 1.4, 0.0);
        this.orbitControls.update();

        // Create the actual Scene
        this.scene = new THREE.Scene();

        // Add light/illumination to the scene
        this.light = new THREE.DirectionalLight(0xffffff);
        this.light.position.set(1.0, 1.0, 1.0).normalize();
        this.scene.add(this.light);
    }

    /**
     * Add a character to the 3D scene. The character is automatically rotated as to
     * face the camera
     * @param {*} character The VMF character to utilize
     */
    addCharacter(character) {
        // Add character to the scene and store it
        this.scene.add(character.scene);
        this.character = character
        
        // Face the camera
        this.character.scene.rotation.y = Math.PI;

        // Setup character animator
        this.characterAnimator = new CharacterAnimator(this.character, this.videoElement)
    }

    /**
     * Perform character update to animate it
     */
    animate() {
        requestAnimationFrame(this.animate.bind(this));

        if (this.character) {
            // Update model to render physics
            this.character.update(this.clock.getDelta());
        }

        this.renderer.render(this.scene, this.orbitCamera);
    }

    /**
     * Start the render loop
     */
    start() {
        this.clock = new THREE.Clock();
        
        // Start animating the character
        this.animate();
    }

    /**
     * Stop the render loop and remove the canvas from the document, so that
     * it goes back to its initial state
     */
    stop() {
        document.body.removeChild(this.renderer.domElement);
        this.clock.stop();
    }
}