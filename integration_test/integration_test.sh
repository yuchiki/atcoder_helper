#!/bin/bash

set -eux


function installed() {
    echo "atcoder_helper がインストールされていることを確認する"
    which atcoder_helper
    # atcoder_helper version

    echo "OK"
}

function can_config_init() {
    echo "atcoder_helper config initができることを確認する"
    atcoder_helper config init
}

function can_show_languages() {
    echo "atcoder_helper config languagesは動く"
    atcoder_helper config languages
}

function can_show_default_language() {
    if [ -z "${1+UNDEF}" ]; then
        echo "atcoder_helper config defaultが動く"
        atcoder_helper config default
    else
        echo "atcoder_helper config defaultが$1を返す"

        test "$(atcoder_helper config default)" = $1
    fi
}

function can_set_default_language() {
    language=$1
    echo "atcoder_helper config useが動く"
    atcoder_helper config use $language
}

function can_task_init() {
    echo "現在のタスクディレクトリが初期化できることを確かめる"
    atcoder_helper task init
}

function can_fetch() {
    echo "タスクがfetchできることを確認する"

    echo "このテストでは実際にatcoderのページをたたいている。早急にmockに切り替えないといけない"

    if [ -z "${1+UNDEF}" ]; then
        contest_flag=""
    else
        contest_flag="--contest $1"
    fi

    if [ -z "${2+UNDEF}" ]; then
        task_flag=""
    else
        task_flag="--task $2"
    fi

    atcoder_helper fetch $contest_flag $task_flag
    ls testcases.yaml
    echo "OK"
}

function can_execute() {
    echo "テストが実行できることを確認する"
    atcoder_helper exec

    echo "OK"
}

function can_task_create() {
    contest=$1
    task=$2

    echo "task ディレクトリを新規作成して初期化できる"
    atcoder_helper task create $contest $task
    echo "OK"
}

function main() {
    cd integration_test

    rm -rf workdir
    mkdir workdir
    cd workdir

    export ATCODER_HELPER_CONFIG_FILEPATH="$(pwd)"/config.yaml

    # 初期設定
    installed
    can_config_init
    can_show_languages
        can_show_default_language cpp-gcc

    can_set_default_language python
    can_show_default_language python

    can_set_default_language cpp-gcc
    can_show_default_language cpp-gcc

    # 既存のディレクトリを初期化して使うケース
    mkdir sample_task
    cd sample_task
    can_task_init
    can_fetch abc102 a
    can_execute
    cd ..

    # 新規にディレクトリを作成して使うケース
    can_task_create abc102 a
    cd abc102/a
    can_fetch
    can_execute


    echo "integration test succeeded."
}

main
