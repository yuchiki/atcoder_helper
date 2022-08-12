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
    cd integration_test

    rm -rf workdir
    mkdir workdir
    cd workdir

    export ATCODER_HELPER_CONFIG_FILEPATH="$(pwd)"/config.yaml

    installed
    can_config_init
    mkdir sample_task
    cd sample_task
    can_init_task
    can_fetch
    can_execute

    echo "integration test succeeded."
}

main
