#!/bin/bash
set -e


# ファイルenv.txt.inからenv.txtを生成する
# もとのファイルにはそれぞれ
# - @dbname@
# - @user@
# - @password@
# が含まれているため、ここを置き換える

gen_random_text() {
    length=${1:-16}
    charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ret=""
    for num in $(seq $length); do
        while :; do
            index=$(od -An -N2 -i /dev/urandom | awk -v len=${#charset} '{if($1!=""){print $1 % len}}')
            # indexが空や0ならやり直し
            if [ -z "$index" ]; then
                continue
            fi
            # indexが数字かつ0以上かつcharset長未満
            if echo "$index" | grep -Eq '^[0-9]+$' && [ "$index" -ge 0 ] && [ "$index" -lt "${#charset}" ]; then
                break
            fi
        done
        char="${charset:$index:1}"
        ret="${ret}${char}"
    done
    echo "$ret"
    return 0
}
if [ ! -f env.txt.in ]; then
    echo "env.txt.in not found"
    exit 1
fi
# env.txtを生成する
rm -f env.txt
sed -e "s/@dbname@/$(gen_random_text 8)/g" \
    -e "s/@user@/$(gen_random_text 8)/g" \
    -e "s/@password@/$(gen_random_text 16)/g" \
    env.txt.in > env.txt
    echo "===="
    cat env.txt
    echo "===="
if [ $? -ne 0 ]; then
    echo "Failed to generate env.txt"
    exit 1
fi
