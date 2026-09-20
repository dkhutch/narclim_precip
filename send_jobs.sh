#!/bin/bash

for x in {1..151..50}; do
y=$(( x + 49 ))
sed -n ${x},${y}p file_dump.txt > split_${x}

cat << EOF > job_${x}
#!/bin/bash
#PBS -P y99
#PBS -q copyq
#PBS -l walltime=03:00:00
#PBS -l ncpus=1
#PBS -l mem=2GB
#PBS -l storage=gdata/y99+scratch/y99+gdata/vk83+gdata/xp65
#PBS -l wd
#PBS -j oe
#PBS -N split_${x}

module use /g/data/xp65/public/modules
module load conda/analysis3-26.03

./calc_pr_rx1day.py split_${x}

EOF

qsub job_${x}

done
