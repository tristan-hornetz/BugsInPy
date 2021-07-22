while read -r line
do
  line_arr=($line)
  dname=$(dirname "${line_arr[1]}")
  fdname=$(readlink -f $dname)
  bname=$(basename "${line_arr[1]}")

  ln -s "$(readlink -f "${line_arr[1]}")" "$fdname/test_$bname"
done < <(du -a | grep ".*/tests_.*py$")

pytest
