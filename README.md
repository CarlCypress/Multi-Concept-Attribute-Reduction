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

