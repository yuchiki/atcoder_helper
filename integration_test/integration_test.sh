#!/bin/bash

set -eu


function installed() {
    echo "atcoder_helper がインストールされていることを確認する"
    which atcoder_helper
    # atcoder_helper version

    echo "OK"
}

function can_init_task() {
    echo "タスクディレクトリが初期化できることを確かめる"
    atcoder_helper init_task
}

function can_fetch() {
    echo "タスクがfetchできることを確認する"

    echo "このテストでは実際にatcoderのページをたたいている。早急にmockに切り替えないといけない"
    atcoder_helper fetch abc102 a
    ls testcases.yaml
    echo "OK"
}

function can_execute() {
    echo "テストが実行できることを確認する"
    atcoder_helper exec

    echo "OK"
}

function main() {
    rm -rf sample_task

    export ATCODER_HELPER_CONFIG_FILEPATH="$(pwd)"/integration_test/config.yaml
    installed
    mkdir  -p sample_task
    cd sample_task
    can_init_task
    can_fetch
    can_execute
    cd ..

    rm -r sample_task

    echo "integration test succeeded."
}

main
