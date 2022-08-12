#!/bin/bash

set -eu


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

function can_task_init() {
    echo "現在のタスクディレクトリが初期化できることを確かめる"
    atcoder_helper task init
}

function can_fetch() {
    contest=$1
    task=$2

    echo "タスクがfetchできることを確認する"

    echo "このテストでは実際にatcoderのページをたたいている。早急にmockに切り替えないといけない"
    atcoder_helper fetch $contest $task
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

    installed
    can_config_init
    mkdir sample_task

    cd sample_task
    can_task_init
    can_fetch abc102 a
    can_execute
    cd ..

    can_task_create abc102 a
    cd abc102/a
    can_fetch abc102 a
    can_execute


    echo "integration test succeeded."
}

main
