#
# avconv -i sample_iTunes.mov -c:v libx264 -strict experimental output.mp4
#
# find ./ -name '*.mov' -exec bash -c 'avconv -i "$0" -c:v libx264 -strict experimental -cpu-used 5 -threads 3 "${0%%.mov}.mp4"' {} \;