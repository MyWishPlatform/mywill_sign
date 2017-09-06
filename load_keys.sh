if [ $# -eq 0 ]; then
    echo "file to load argument required: load_keys result-0-to-1000.bin"
    exit 1
fi


echo "enter password to decrypt keys"

openssl aes-256-cbc -d -a -in $1 -out - | ./loader.py
