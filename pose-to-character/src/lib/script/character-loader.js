import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { VRMUtils, VRM, VRMSchema } from '@pixiv/three-vrm';

/**
 * Class representing a loader for VMF 3D models (aka `characters`, in this project)
 */
export class CharacterLoader {
    /**
     * Create a loader, storing the URL from which the 3D model will be fetched on request
     * @param {*} url The URL from which the 3D model will be fetched
     */
    constructor(url) {
        this.url = url
    }

    /**
     * Load (download) the 3D model from the URL previously stored and call the callback function,
     * which can then do anything with the actual 3D VMF model
     * @param {*} callback The function which will be called after successfully loading the 3D model
     */
    load(callback) {
        // Import Character VRM
        const loader = new GLTFLoader();
        loader.crossOrigin = "anonymous";

        loader.load(
            this.url,

            (gltf) => {
                VRMUtils.removeUnnecessaryJoints(gltf.scene);

                VRM.from(gltf).then(vrm => {
                    callback(vrm)
                });        
            },

            progress =>
                console.log(
                    "Loading model...",
                    100.0 * (progress.loaded / progress.total),
                    "%"
                ),

            error => console.error(error)
        );
    }
}