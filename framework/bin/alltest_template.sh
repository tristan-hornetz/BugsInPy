usage="-w work_dir
             The working directory to run the test. Default will be the current directory.
"


run_all="0"
relevant="0"
case $1 in
 -[h?] | --help)
    cat <<-____HALP
        Usage: ${0##*/} [ --help ]
        $usage
____HALP
        exit 0;;
esac

single_test=""
###Read the flag of checkout
while getopts t:w: flag
do
    case "${flag}" in
        w) work_dir=${OPTARG};;
        t) single_test=${OPTARG};;
    esac
done

###Update the work directory
if [ "$work_dir" == "" ]; then
   work_dir=$(pwd)
fi

if [[ $work_dir == */ ]]; then
   temp_work_dir="$work_dir"
   work_dir=${temp_work_dir::-1}
fi

if [[ ! -e "$work_dir/bugsinpy_run_test.sh" ]]; then
   echo "This is not a checkout project folder"
   exit
fi

if [[ ! -e "$work_dir/bugsinpy_compile_flag" ]]; then
   echo "You have not compiled this project"
   exit
fi

if [[ "$relevant" == "1" ]]; then
   run_all="0"
   single_test=""
fi

###Initialize pyenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv deactivate


###Read bug.info file
buggy_commit=""
python_version=""

DONE=false
until $DONE ;do
read || DONE=true
if [[ "$REPLY" == "buggy_commit_id"* ]]; then
   buggy_commit="$(cut -d'"' -f 2 <<< $REPLY)"
elif [[ "$REPLY" == "python_version"* ]]; then
   python_version="$(cut -d'"' -f 2 <<< $REPLY)"
fi
done < "$work_dir/bugsinpy_bug.info"


shasum_output=$(sha1sum "$work_dir/bugsinpy_requirements.txt")
shas_split=($shasum_output)
requirement_hash=${shas_split[0]}

###Activate environment
env_name="_bugsinpy_${python_version}_${requirement_hash}"
pyenv activate $env_name

cd "$work_dir"

