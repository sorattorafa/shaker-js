#!/bin/sh

cp -r "/__shaker" "./"
python3 "./__shaker/shaker.py" $INPUT_TOOL "." -o "$INPUT_OUTPUT_FOLDER" -nsr $INPUT_NO_STRESS_RUNS -sr $INPUT_RUNS -tc "$INPUT_TESTS_COMMAND"
ret=$?

#counting the tests
collection=$(find . -type f -iname __results.json)
tests=0
for i in $collection;
do
  for j in $(ls "$i"/*.txt 2> /dev/null);
  do
    h=$(grep -e "Tests run: [0-9]*" "$j" | awk '{print $3}' | sed 's/.$//')
    tests=$(($tests + $h))
  done
done
ls
cd output
ls
cd ..
cat ./output/exec_setup.err
cat ./output/exec_setup.out
exit $ret
