# ShadowMe

### Pipeline
![pipeline](poseExtraction/img/pipeline.svg)



> [**Shadow Me: Low-power 2D Motion Emulation and 3D Renders**](https://github.com/404/),            
> [Marco Garosi](https://www.instagram.com/marco_garosi/), [Riccardo Tedoldi](https://www.instagram.com/riccardotedoldi/)
>
> Supervisor: [Giulia Martinelli](https://www4.unitn.it/du/it/Persona/PER0202241/Didattica), [Nicola Conci](https://scholar.google.it/citations?user=mR1GK28AAAAJ&hl=it)   
> *Computer Vision Project, Spring 2023* 


With `ShadowMe` is possible to perform low-power 2D video-guided pose emulation from pose-free videos. Additionally, we provide a web interface which enable to perform the pose emulation of a video via web browser real-time. It works on smartphones and iPads!!

## Overview
Our solution is highly efficient because it is based on the Mediapipe library, which offers a variety of tools that balance performance with available hardware resources. Using our pipeline, which leverages Mediapipe, we can easily track human poses in 2D videos and reproduce their motion in a virtual environment with real-time performance. Compared to high-resource models, our solution appears to be a reasonable alternative. We tested our solution on an iPad and were able to achieve real-time performance of the tracked motion in the virtual environment at 25/30 fps. The pre-compiled web interface has been implemented to minimize the overhead of the pipeline as much as possible.
## Features
The `poseExtraction` folder contains some of the experiments we have conducted, which have helped us gain a deeper understanding of the field. Meanwhile, the `ShadowMe` folder contains the implemented pipeline. The code has been documented thoroughly, and more detailed explanations can be found within the code itself.
## Installation
In order to test `ShadowMe`, it is necessary to install the dependencies and execute a few lines of code on the bash.
### Install the Dependencies

To install the necessary dependencies, download the requirements listed in the `./requirements.txt` file by executing the following command.

```bash
pip install -r requirements.txt
```

### Usage

To run `ShadowMe` on a 2D video, execute the following command.
```bash
./run video.mp4
```
To run real-time `ShadowMe` on your camera, execute the following command.

```bash
./run
```

## Contributing

We have made our implementation publicly available, and we welcome anyone who would like to join us and contribute to the project.
### Contact
If you have suggestions or ideas for further improvemets please contact us.
- riccardo tedoldi: [@riccardotedoldi](https://www.instagram.com/riccardotedoldi/)
- marco garosi: [@marcogarosi](https://www.instagram.com/marco_garosi/)

Also, if you find any bugs or issues, please let us know. We are happy to fix them!

## License


### To cite our work
```bibtex
@misc{GarosiTedoldi2022,
    title   = {Shadow Me: Low-power 2D Motion Emulation and 3D Renders},
    author  = {Marco Garosi, Riccardo Tedoldi, Giulia Martinelli},
    year    = {2023},
    url  = {https://github.com/r1cc4r2o/PoseEstimationTo3Drender}
}
```
