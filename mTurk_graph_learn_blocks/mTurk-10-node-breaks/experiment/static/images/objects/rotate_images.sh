# angles=( 15 30 45 60 75 )
cd original
size=300

for in_image in *600.jpg
do
    degrees=$(( ( RANDOM % 72 ) * 5 ))
    degrees_rotated=$(( degrees + 60 ))
    out_image="${in_image%600.jpg}${size}.jpg" # rename for the new size
    convert "${in_image}" -rotate "${degrees}" -gravity center -crop '150x150' -resize "${size}" "../base/${out_image}"
    convert "${in_image}" -rotate "${degrees_rotated}" -gravity center -crop '150x150' -resize "${size}" "../rotated/${out_image}"
done
