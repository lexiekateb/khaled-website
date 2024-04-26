#!/bin/bash

py_script=plotGraphProps.py
#py_script=plotNoise.py

outdir=plotGraphRepoWithOrig_k14_nolog
#outdir=plotNoiseRepo
#outdir=plotGraphRepo_k5_gpu
#outdir=plotGraphRepoWithOrig_k14_y_elog
outdir=testDump
outdir=testLoad
outdir=testNoise
outdir=testLoadNoise
outdir=testLoadNoiseLog2X
x0=0.999
x1=0.437
x2=0.437
x3=0.484

k=5

#GPU=--gpu
#GPU=""
start_time=$(date +%s)
#python $py_script $GPU --from_disk testDump --p $x0 $x1 $x2 $x3 --plots kde --props deg in-deg out-deg betweenness-centrality  --outdir $outdir

#CUDA_VISIBLE_DEVICES=1 python $py_script $GPU --p $x0 $x1 $x2 $x3 --plots kde --props deg in-deg out-deg betweenness-centrality  --outdir $outdir

#CUDA_VISIBLE_DEVICES=0 python $py_script $GPU --p $x0 $x1 $x2 $x3 --plots kde --props deg in-deg out-deg betweenness-centrality  --outdir $outdir

#CUDA_VISIBLE_DEVICES=0 python $py_script $GPU  --p $x0 $x1 $x2 $x3 --plots kde --props deg in-deg out-deg betweenness-centrality eigenvector-centrality katz-centrality edge-betweenness-centrality scree  --outdir $outdir

#python $py_script --p $x0 $x1 $x2 $x3 --props scree --k $k --outdir scree_only_k5

python $py_script --p $x0 $x1 $x2 $x3 --k $k --plots kde --props deg --outdir newout

end_time=$(date +%s)
exec_time=$((end_time - start_time))
echo "Execution time: $exec_time seconds"
#python $py_script --p $x0 $x1 $x2 $x3 --plots kde --props deg in-deg out-deg clustering betweenness-centrality laplacian-centrality closeness-centrality scree --k $k --outdir $outdir
