# Multi-Concept Attribute Reduction

This project is an open-source implementation of the experimental code for the **Multi-Concept Attribute Reduction** paper.

First, the environment needs to be set up. Use the following command:

```shell
conda env create -f environment.yml
```

Modify the execution permissions of the **.sh** scripts:

```shell
chmod +x ./attribute_reduction/*.sh
```

Finally, run the **.sh** scripts as needed. An example is shown below:

```shell
nohup ./attribute_reduction/run_DAAR.sh > ./DAAR.log &
nohup ./attribute_reduction/run_heuri.sh > ./heuri.log &
nohup ./attribute_reduction/run_time.sh > ./time.log &
```

## Citation

```latex
@article{hu2026attribute,
  title={Attribute reduction for concept cognition over knowledge graphs},
  author={Hu, Xin and Huang, Denan and Duan, Jiangli and Zhao, Zhongying and Zhang, Sulan},
  journal={Engineering Applications of Artificial Intelligence},
  volume={176},
  pages={114740},
  year={2026},
  publisher={Elsevier}
}
```

