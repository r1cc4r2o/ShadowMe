import * as THREE from 'three';
import { VRMSchema } from '@pixiv/three-vrm';
import * as Kalidokit from 'kalidokit';

// Kalidokit helper functions
const clamp = Kalidokit.Utils.clamp;
const lerp = Kalidokit.Vector.lerp;

/**
 * Class representing an animator for 3D models ('characters')
 */
export class CharacterAnimator {
    /**
     * Create a new animator, storing the character and the video element for later usage
     * @param {*} character The 3D model to animate
     * @param {*} videoElement The HTML element from which the video is being streamed
     */
    constructor(character, videoElement) {
        this.character = character
        this.videoElement = videoElement
        this.oldLookTarget = new THREE.Euler()
    }

    /**
     * Compute the rig rotation given the parameters and dampen it in order to smoothen the result.
     * Update of the model is performed within this function, therefore the return value is intended
     * only for further processing usage (e.g. for storing on an external file).
     * @param {string} name Bone name, to retreive the actual bone to animate in the model
     * @param {*} rotation Rotation angles on the three axis, x, y and z respectively. Expressed in degrees
     * @param {*} dampener Dampening/smoothing factor, default at 1
     * @param {*} lerpAmount Linear interpolation amount, default at 0.3
     * @returns The interpolated rotation
     */
    rigRotation(name, rotation = { x: 0, y: 0, z: 0 }, dampener = 1, lerpAmount = 0.3) {
        if (!this.character) { return }

        // Get body part and check if it is available on the current model
        const Part = this.character.humanoid.getBoneNode(
            VRMSchema.HumanoidBoneName[name]
        );
        if (!Part) { return }
    
        let euler = new THREE.Euler(
            rotation.x * dampener,
            rotation.y * dampener,
            rotation.z * dampener
        );
        let quaternion = new THREE.Quaternion().setFromEuler(euler);

        // Compute the interpolated rotation. Value is stored but unused
        // because it may be helpful for additional processing (e.g. to store
        // it on an external file)
        let interpolated = Part.quaternion.slerp(quaternion, lerpAmount);
    };
    
    
    /**
     * Compute the rig position given the parameters and dampen it in order to smoothen the result.
     * Update of the model is performed within this function, therefore the return value is intended
     * only for further processing usage (e.g. for storing on an external file).
     * @param {string} name Bone name, to retreive the actual bone to animate in the model
     * @param {*} position New position on the three axis, x, y and z respectively
     * @param {*} dampener Dampening/smoothing factor, default at 1
     * @param {*} lerpAmount Linear interpolation amount, default at 0.3
     * @returns The interpolated position
     */
    rigPosition(name, position = { x: 0, y: 0, z: 0 }, dampener = 1, lerpAmount = 0.3) {
        if (!this.character) { return }

        // Get body part and check if it is available on the current model
        const Part = this.character.humanoid.getBoneNode(
            VRMSchema.HumanoidBoneName[name]
        );
        if (!Part) { return }

        let vector = new THREE.Vector3(
            position.x * dampener,
            position.y * dampener,
            position.z * dampener
        );

        // Compute the interpolated position. Value is stored but unused
        // because it may be helpful for additional processing (e.g. to store
        // it on an external file)
        let interpolated = Part.position.lerp(vector, lerpAmount);
    };
    
    /**
     * Rig the face
     * @param {*} riggedFace Face landmarks as computed/extracted by mediapipe
     */
    rigFace(riggedFace) {
        if (!this.character) { return }
        
        // Rotate the neck
        this.rigRotation("Neck", riggedFace.head, 0.7);
    
        // Blendshapes and Preset Name Schema
        const Blendshape = this.character.blendShapeProxy;
        const PresetName = VRMSchema.BlendShapePresetName;
    
        // Simple example without winking. Interpolate based on old blendshape, then stabilize blink with `Kalidokit` helper function.
        // for VRM, 1 is closed, 0 is open.
        riggedFace.eye.l = lerp(clamp(1 - riggedFace.eye.l, 0, 1), Blendshape.getValue(PresetName.Blink), .5)
        riggedFace.eye.r = lerp(clamp(1 - riggedFace.eye.r, 0, 1), Blendshape.getValue(PresetName.Blink), .5)
        riggedFace.eye = Kalidokit.Face.stabilizeBlink(riggedFace.eye, riggedFace.head.y)
        Blendshape.setValue(PresetName.Blink, riggedFace.eye.l);
    
        // Interpolate and set mouth blendshapes
        Blendshape.setValue(PresetName.I, lerp(riggedFace.mouth.shape.I, Blendshape.getValue(PresetName.I), .5));
        Blendshape.setValue(PresetName.A, lerp(riggedFace.mouth.shape.A, Blendshape.getValue(PresetName.A), .5));
        Blendshape.setValue(PresetName.E, lerp(riggedFace.mouth.shape.E, Blendshape.getValue(PresetName.E), .5));
        Blendshape.setValue(PresetName.O, lerp(riggedFace.mouth.shape.O, Blendshape.getValue(PresetName.O), .5));
        Blendshape.setValue(PresetName.U, lerp(riggedFace.mouth.shape.U, Blendshape.getValue(PresetName.U), .5));
    
        // Pupil interpolation (+ store a copy of the value)
        let lookTarget =
            new THREE.Euler(
                lerp(this.oldLookTarget.x, riggedFace.pupil.y, .4),
                lerp(this.oldLookTarget.y, riggedFace.pupil.x, .4),
                0,
                "XYZ"
            )
        this.oldLookTarget.copy(lookTarget)
        this.character.lookAt.applyer.lookAt(lookTarget);
    }

    /**
     * Animate the character by processing the results provided by mediapipe. Inverse kinematics
     * algorithms are employed in order to solve the contraints which hold among the joints and
     * compute actual bones rotations.
     * The code is quite repetitive, as there are several bones to compute rotations for (e.g. all the
     * bones in the hands/fingers), however it is quite simple from an overall point of view.
     * @param {*} results The results provided by mediapipe
     */
    animateCharacter = (results) => {
        if (!this.character) {
            return;
        }
    
        let riggedPose, riggedLeftHand, riggedRightHand, riggedFace;
    
        // Face landmarks extracted by mediapipe
        const faceLandmarks = results.faceLandmarks;
        
        // Pose 3D landmarks extracted by mediapipe
        // They are expressed with respect to the hips and the unit of measure is metres
        const pose3DLandmarks = results.ea;

        // Pose 2D landmarks extracted by mediapipe
        // They are expressed with respect to the input video's width and height
        const pose2DLandmarks = results.poseLandmarks;

        // Left and right hand landmarks extracted by mediapipe
        const leftHandLandmarks = results.rightHandLandmarks;
        const rightHandLandmarks = results.leftHandLandmarks;
    
        // Face animation, if mediapipe was able to compute landmarks
        if (faceLandmarks) {
            riggedFace = Kalidokit.Face.solve(faceLandmarks, {
                runtime: "mediapipe",
                video: this.videoElement
            });

            this.rigFace(riggedFace)
        }
    
        // Pose animation, if mediapipe was able to compute landmarks
        if (pose2DLandmarks && pose3DLandmarks) {
            riggedPose = Kalidokit.Pose.solve(pose3DLandmarks, pose2DLandmarks, {
                runtime: "mediapipe",
                video: this.videoElement,
            });
            
            this.rigRotation("Hips", riggedPose.Hips.rotation, 0.7);
            this.rigPosition(
                "Hips",
                {
                    x: -riggedPose.Hips.position.x,
                    y: riggedPose.Hips.position.y + 1,
                    z: -riggedPose.Hips.position.z
                },
                1,
                0.07
            );
    
            this.rigRotation("Chest", riggedPose.Spine, 0.25, .3);
            this.rigRotation("Spine", riggedPose.Spine, 0.45, .3);
            this.rigRotation("RightUpperArm", riggedPose.RightUpperArm, 1, .3);
            this.rigRotation("RightLowerArm", riggedPose.RightLowerArm, 1, .3);
            this.rigRotation("LeftUpperArm", riggedPose.LeftUpperArm, 1, .3);
            this.rigRotation("LeftLowerArm", riggedPose.LeftLowerArm, 1, .3);
    
            this.rigRotation("LeftUpperLeg", riggedPose.LeftUpperLeg, 1, .3);
            this.rigRotation("LeftLowerLeg", riggedPose.LeftLowerLeg, 1, .3);
            this.rigRotation("RightUpperLeg", riggedPose.RightUpperLeg, 1, .3);
            this.rigRotation("RightLowerLeg", riggedPose.RightLowerLeg, 1, .3);
        }
    
        // Left hand animation, if mediapipe was able to compute landmarks
        if (leftHandLandmarks) {
            riggedLeftHand = Kalidokit.Hand.solve(leftHandLandmarks, "Left");
            this.rigRotation("LeftHand", {
                z: riggedPose.LeftHand.z,
                y: riggedLeftHand.LeftWrist.y,
                x: riggedLeftHand.LeftWrist.x
            });
            
            // All the bones in the left hand
            this.rigRotation("LeftRingProximal", riggedLeftHand.LeftRingProximal);
            this.rigRotation("LeftRingIntermediate", riggedLeftHand.LeftRingIntermediate);
            this.rigRotation("LeftRingDistal", riggedLeftHand.LeftRingDistal);
            this.rigRotation("LeftIndexProximal", riggedLeftHand.LeftIndexProximal);
            this.rigRotation("LeftIndexIntermediate", riggedLeftHand.LeftIndexIntermediate);
            this.rigRotation("LeftIndexDistal", riggedLeftHand.LeftIndexDistal);
            this.rigRotation("LeftMiddleProximal", riggedLeftHand.LeftMiddleProximal);
            this.rigRotation("LeftMiddleIntermediate", riggedLeftHand.LeftMiddleIntermediate);
            this.rigRotation("LeftMiddleDistal", riggedLeftHand.LeftMiddleDistal);
            this.rigRotation("LeftThumbProximal", riggedLeftHand.LeftThumbProximal);
            this.rigRotation("LeftThumbIntermediate", riggedLeftHand.LeftThumbIntermediate);
            this.rigRotation("LeftThumbDistal", riggedLeftHand.LeftThumbDistal);
            this.rigRotation("LeftLittleProximal", riggedLeftHand.LeftLittleProximal);
            this.rigRotation("LeftLittleIntermediate", riggedLeftHand.LeftLittleIntermediate);
            this.rigRotation("LeftLittleDistal", riggedLeftHand.LeftLittleDistal);
        }

        // Right hand animation, if mediapipe was able to compute landmarks
        if (rightHandLandmarks) {
            riggedRightHand = Kalidokit.Hand.solve(rightHandLandmarks, "Right");
            this.rigRotation("RightHand", {
                z: riggedPose.RightHand.z,
                y: riggedRightHand.RightWrist.y,
                x: riggedRightHand.RightWrist.x
            });

            // All the bones in the right hand
            this.rigRotation("RightRingProximal", riggedRightHand.RightRingProximal);
            this.rigRotation("RightRingIntermediate", riggedRightHand.RightRingIntermediate);
            this.rigRotation("RightRingDistal", riggedRightHand.RightRingDistal);
            this.rigRotation("RightIndexProximal", riggedRightHand.RightIndexProximal);
            this.rigRotation("RightIndexIntermediate", riggedRightHand.RightIndexIntermediate);
            this.rigRotation("RightIndexDistal", riggedRightHand.RightIndexDistal);
            this.rigRotation("RightMiddleProximal", riggedRightHand.RightMiddleProximal);
            this.rigRotation("RightMiddleIntermediate", riggedRightHand.RightMiddleIntermediate);
            this.rigRotation("RightMiddleDistal", riggedRightHand.RightMiddleDistal);
            this.rigRotation("RightThumbProximal", riggedRightHand.RightThumbProximal);
            this.rigRotation("RightThumbIntermediate", riggedRightHand.RightThumbIntermediate);
            this.rigRotation("RightThumbDistal", riggedRightHand.RightThumbDistal);
            this.rigRotation("RightLittleProximal", riggedRightHand.RightLittleProximal);
            this.rigRotation("RightLittleIntermediate", riggedRightHand.RightLittleIntermediate);
            this.rigRotation("RightLittleDistal", riggedRightHand.RightLittleDistal);
        }
    }
}