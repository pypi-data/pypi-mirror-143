# LERG

LERG (Local Explanation of Response Generation) is a unified approach to explain why a conditional text generation model will predict a text.
For more details, please refer to the paper [Local Explanation of Dialogue Response Generation, Neurips 2021](https://arxiv.org/pdf/2106.06528.pdf). 


## Install

LERG can be installed from PyPI
```
pip install lerg
```

## Usage

The overall idea is to first import a purtabation model and an explanation method, then you can use LERG as:

```
from lerg.perturbation_models import RandomPM
from lerg.RG_explainers import LERG_SHAP_log as LERG_S

PM = RandomPM()
perturb_f = PM.perturb_inputs
local_exp  = LERG_S(<replace_with_your_model_forward_function>, input_str, output_str, perturb_f, your_tokenizer)
phi_set, phi_map, input_segments, output_segments = local_exp.get_local_exp()
```

## Citation
If you find LERG is helpful to your research, we would appreciate a citation of this paper.
```
@article{tuan2021local,
  title={Local Explanation of Dialogue Response Generation},
  author={Tuan, Yi-Lin and Pryor, Connor and Chen, Wenhu and Getoor, Lise and Wang, William Yang},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  year={2021}
}
```
