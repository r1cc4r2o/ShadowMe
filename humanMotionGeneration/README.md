# Human Motion Generation

The notebooks provided are self-contained and include all the needed requirements. To generate motion, you can simply upload the notebook in Google Colaboratory and condition it with the latent representation of a textual prompt. Our first notebook it includes experiments based on the work of [Zhang et al.](https://mingyuan-zhang.github.io/projects/MotionDiffuse.html), and we recommend further reading for a deeper understanding. Initially, we aimed to support motion generation from textual prompts on our platform. However, due to the computational complexity involved, this is not feasible on low-power platforms. Despite using models with minimal architecture compared to the previous state of the art, they are still pushing the boundaries of the state-of-the-art. Unfortunately, the computational complexity remains too high to integrate these models into a low-power solution. Here, we leave the link to our presentation we have made at the University of Trento related to [Human Motion Generation](https://drive.google.com/file/d/1aRbJiOGDHxW6zz7HDkFtvltjWuvs4IXJ).

# Requirements

* Google Colaboratory Free Plan

# Installation & How to run

* Clone the notebook
* Upload the notebook on Google Colaboratory


# References

```bibtex
@article{zhang2022motiondiffuse,
      title   =   {MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model}, 
      author  =   {Zhang, Mingyuan and
                   Cai, Zhongang and
                   Pan, Liang and
                   Hong, Fangzhou and
                   Guo, Xinying and
                   Yang, Lei and
                   Liu, Ziwei},
      year    =   {2022},
      journal =   {arXiv preprint arXiv:2208.15001},
}
```


```bibtex
@article{tevet2022human,
  title={Human Motion Diffusion Model},
  author={Tevet, Guy and Raab, Sigal and Gordon, Brian and Shafir, Yonatan and Bermano, Amit H and Cohen-Or, Daniel},
  journal={arXiv preprint arXiv:2209.14916},
  year={2022}
}
```


```bibtex
@misc{shafir2023human,
      title={Human Motion Diffusion as a Generative Prior}, 
      author={Yonatan Shafir and Guy Tevet and Roy Kapon and Amit H. Bermano},
      year={2023},
      eprint={2303.01418},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```