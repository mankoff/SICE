
# 2017 & 2018
# 15 March (074) - 30 Sep (274)

# CREODIAS
SEN3_source=/eodata/Sentinel-3
dest_root=/sice-data/SICE/S3
proc_root=/sice-data/SICE/proc
mosaic_root=/sice-data/SICE/mosaic

# # dev
# dest_root=./SEN3
# proc_root=./out
# mosaic_root=./mosaic

set -o errexit
set -o nounset
set -o pipefail

LD_LIBRARY_PATH=. # SNAP requirement

for year in 2018 2017; do
  for doy in $(seq -w 74 274); do

#     ## DEBUG
# for year in 2017; do
#   for doy in 227 180; do  # 2017-08-15=227

    date=$(date -d "${year}-01-01 +$(( 10#${doy}-1 )) days" "+%Y-%m-%d")

    # Fetch one day of OLCI & SLSTR scenes over Greenland
    mkdir -p ${dest_root}/${year}/${date}
    ./dhusget_wrapper.sh -d ${date} -l ${SEN3_source} -o ${dest_root}/${year}/${date}
    # ./dhusget_wrapper.sh -d ${date} -o ${dest_root}/${year}/${date}

    # SNAP: Reproject, calculate reflectance, extract bands, etc.
    ./S3_proc.sh -i ${dest_root}/${year}/${date} -o ${proc_root}/${date} -X S3.xml -t

    # SICE
    parallel --verbose --lb -j 5 \
    	     python ./sice.py ${proc_root}/${date}/{} \
    	     ::: $(ls ${proc_root}/${date}/)

    # Mosaic
    ./dm.sh ${date} ${proc_root}/${date} ${mosaic_root}

    # Extra
   tmpdir=./G_$$
    grass -c ${mosaic_root}/${date}/SZA.tif ${tmpdir} --exec <<EOF
r.external input=r_TOA_01.tif output=r01
r.external input=r_TOA_06.tif output=r06
r.external input=r_TOA_16.tif output=r16
r.external input=r_TOA_21.tif output=r21
r.mapcalc "ndsi = (r16-r21)/(r16+r21)"
r.mapcalc "ndbi = (r01-r21)/(r01+r21)"
r.mapcalc "bba_emp = (r01 + r06 + r17 + r21) / (4.0 * 0.945 + 0.055)"
gdal_opts='type=Float32 createopt=COMPRESS=DEFLATE,PREDICTOR=2,TILED=YES --q'
r.out.gdal -m -c input=ndsi output=${mosaic_root}/${date}/NDSI.tif ${tifopts}
r.out.gdal -m -c input=ndbi output=${mosaic_root}/${date}/NDBI.tif ${tifopts}
r.out.gdal -m -c input=bba_emp output=${mosaic_root}/${date}/BBA_emp.tif ${tifopts}
EOF
    rm -fR ${tmpdir}

  done
done
