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
@article{huang2026attribute,
  title = {Attribute Reduction for Concept Cognition Over Knowledge Graphs},
  author = {Huang, Denan and Duan, Jiangli and others},
  journal = {Engineering Applications of Artificial Intelligence},
  year = {2026},
  note = {In press}
}
```

