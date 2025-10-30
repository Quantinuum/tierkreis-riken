#!/usr/bin/env bash
set -x
set -eou pipefail

source $(dirname $0)/backend_setup.sh ibm-kobe-dacc
uv run g++ -O3 -Wall -shared -std=c++11 -fPIC $(uv run python -m pybind11 --includes) -I/vol0300/share/ra010014/jhpcq_modules/x86/SDK/SQC_library_0.9/include tkr_sqcsub.cpp -o tkr_sqcsub$(uv run python -m pybind11 --extension-suffix) \
    -L/vol0300/share/ra010014/jhpcq_modules/x86/SDK/SQC_library_0.9/lib -L/vol0300/share/ra010014/jhpcq_modules/x86/SDK/SQC_library_0.9/lib64 \
    -lsqc_api  -lsqc_rpc -lsqc_reqsched -lsqc_reqinvoker -lqtmd_sim_invoker -lsqc_dbmgr \
    -lsqc_util -lsqc_rpccommon -luuid -lsqlite3 -lprotobuf -labsl_leak_check -labsl_die_if_null \
    -labsl_log_initialize -lutf8_validity -lutf8_range -lgrpc++ -lgrpc -laddress_sorting -lupb_textformat_lib \
    -lupb_json_lib -lupb_wire_lib -lupb_message_lib -lutf8_range_lib -lupb_mini_descriptor_lib -lupb_mem_lib \
    -lupb_base_lib -labsl_statusor -lgpr -labsl_log_internal_check_op -labsl_flags_internal \
    -labsl_flags_reflection -labsl_flags_private_handle_accessor -labsl_flags_commandlineflag \
    -labsl_flags_commandlineflag_internal -labsl_flags_config -labsl_flags_program_name -labsl_raw_hash_set \
    -labsl_hashtablez_sampler -labsl_flags_marshalling -labsl_log_internal_conditions \
    -labsl_log_internal_message -labsl_examine_stack -labsl_log_internal_format -labsl_log_internal_proto \
    -labsl_log_internal_nullguard -labsl_log_internal_log_sink_set -labsl_log_internal_globals -labsl_log_sink \
    -labsl_log_entry -labsl_log_globals -labsl_hash -labsl_city -labsl_low_level_hash \
    -labsl_vlog_config_internal -labsl_log_internal_fnmatch -labsl_random_distributions \
    -labsl_random_seed_sequences -labsl_random_internal_pool_urbg -labsl_random_internal_randen \
    -labsl_random_internal_randen_hwaes -labsl_random_internal_randen_hwaes_impl \
    -labsl_random_internal_randen_slow -labsl_random_internal_platform -labsl_random_internal_seed_material \
    -labsl_random_seed_gen_exception -labsl_status -labsl_cord -labsl_cordz_info -labsl_cord_internal \
    -labsl_cordz_functions -labsl_exponential_biased -labsl_cordz_handle -labsl_crc_cord_state -labsl_crc32c \
    -labsl_crc_internal -labsl_crc_cpu_detect -labsl_bad_optional_access -labsl_strerror \
    -labsl_str_format_internal -labsl_synchronization -labsl_graphcycles_internal \
    -labsl_kernel_timeout_internal -labsl_stacktrace -labsl_symbolize -labsl_debugging_internal \
    -labsl_demangle_internal -labsl_malloc_internal -labsl_time -labsl_civil_time -labsl_strings \
    -labsl_strings_internal -labsl_string_view -labsl_base -labsl_spinlock_wait -labsl_int128 \
    -labsl_throw_delegate -labsl_time_zone -labsl_bad_variant_access -labsl_raw_logging_internal \
    -labsl_log_severity -lcares -lssl -lre2 -lz -lmunge -lcrypto -lsqc_rpccommon -lprotobuf-c -lrt \
    -lpthread -ldl -lnuma -pthread