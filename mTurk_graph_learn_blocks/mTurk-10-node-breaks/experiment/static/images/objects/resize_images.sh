# angles=( 15 30 45 60 75 )

size=300

cd base_full
for in_image in *600.jpg
do
    out_image="${in_image%.jpg}_small.jpg" # rename for the new size
    convert "${in_image}" -resize "${size}" "../base/${out_image}"
done

cd ../rotated_full
for in_image in *600.jpg
do
    out_image="${in_image%.jpg}_small.jpg" # rename for the new size
    convert "${in_image}" -resize "${size}" "../rotated/${out_image}"
done
