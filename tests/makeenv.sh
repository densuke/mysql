#!/bin/sh
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
    # charsetを使って、$length文の長さの文字列を生成する
    ret=""
    for num in $(seq $length); do
        # 0から$((${#charset} - 1))の範囲のランダムな数値を生成する
        index=$(od -An -N2 -i /dev/urandom | awk -v len=${#charset} '{print $1 % len}')
        # charsetのindex番目の文字をretに追加する (POSIX互換)
        char=$(expr substr "$charset" $(($index + 1)) 1)
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
if [ $? -ne 0 ]; then
    echo "Failed to generate env.txt"
    exit 1
fi
