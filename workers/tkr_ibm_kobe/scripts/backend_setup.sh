#!/usr/bin/env bash
set -xeuo pipefail

#Setting up Remote Procedure Call (RPC)
# 1. Set up IP address of quantum computer to SQC_RPC_SERVER according to a argument
if [ "$#" -eq 1 ]; then
  QPU="$1"
  if [ $QPU = "reimei" ]; then
     # The server port number will be changed for different target
     export SQC_RPC_SERVER=10.132.0.10:30011
  elif [ $QPU = "reimei-simulator" ]; then
     export SQC_RPC_SERVER=10.132.0.10:30001
  elif [ $QPU = "ibm-kobe-dacc" ]; then
     export SQC_RPC_SERVER=10.132.0.11:30001
  else
     echo "invalid qpu $QPU"
  fi
else
 echo "usage: /path/to/backend_setup.sh <target-qpu-name>"
fi

# 2. Set up environment variables
source $(dirname $0)/config.sh

# 3. Load related packages with Spack
source /vol0004/apps/oss/spack-v0.21/share/spack/setup-env.sh
spack load ${SPACK_PKG}

# 4. Add SQC library paths to the LD_LIBRARY_PATH and PKG_CONFIG_PATH environment variable
export LD_LIBRARY_PATH=${SQC_DIR}/lib:${SQC_DIR}/lib64:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=${SQC_DIR}/lib64/pkgconfig

# 5. Set SQC_COMPILE_OPTIONS variable to compile program using SQC C-API.
SQC_LIBS="-lsqc_api  -lsqc_rpc -lsqc_reqsched -lsqc_reqinvoker -lqtmd_sim_invoker -lsqc_dbmgr\
 -lsqc_util -lsqc_rpccommon -luuid -lsqlite3 -lprotobuf -labsl_leak_check -labsl_die_if_null\
 -labsl_log_initialize -lutf8_validity -lutf8_range -lgrpc++ -lgrpc -laddress_sorting -lupb_textformat_lib\
 -lupb_json_lib -lupb_wire_lib -lupb_message_lib -lutf8_range_lib -lupb_mini_descriptor_lib -lupb_mem_lib\
 -lupb_base_lib -labsl_statusor -lgpr -labsl_log_internal_check_op -labsl_flags_internal\
 -labsl_flags_reflection -labsl_flags_private_handle_accessor -labsl_flags_commandlineflag\
 -labsl_flags_commandlineflag_internal -labsl_flags_config -labsl_flags_program_name -labsl_raw_hash_set\
 -labsl_hashtablez_sampler -labsl_flags_marshalling -labsl_log_internal_conditions\
 -labsl_log_internal_message -labsl_examine_stack -labsl_log_internal_format -labsl_log_internal_proto\
 -labsl_log_internal_nullguard -labsl_log_internal_log_sink_set -labsl_log_internal_globals -labsl_log_sink\
 -labsl_log_entry -labsl_log_globals -labsl_hash -labsl_city -labsl_low_level_hash\
 -labsl_vlog_config_internal -labsl_log_internal_fnmatch -labsl_random_distributions\
 -labsl_random_seed_sequences -labsl_random_internal_pool_urbg -labsl_random_internal_randen\
 -labsl_random_internal_randen_hwaes -labsl_random_internal_randen_hwaes_impl\
 -labsl_random_internal_randen_slow -labsl_random_internal_platform -labsl_random_internal_seed_material\
 -labsl_random_seed_gen_exception -labsl_status -labsl_cord -labsl_cordz_info -labsl_cord_internal\
 -labsl_cordz_functions -labsl_exponential_biased -labsl_cordz_handle -labsl_crc_cord_state -labsl_crc32c\
 -labsl_crc_internal -labsl_crc_cpu_detect -labsl_bad_optional_access -labsl_strerror\
 -labsl_str_format_internal -labsl_synchronization -labsl_graphcycles_internal\
 -labsl_kernel_timeout_internal -labsl_stacktrace -labsl_symbolize -labsl_debugging_internal\
 -labsl_demangle_internal -labsl_malloc_internal -labsl_time -labsl_civil_time -labsl_strings\
 -labsl_strings_internal -labsl_string_view -labsl_base -labsl_spinlock_wait -labsl_int128\
 -labsl_throw_delegate -labsl_time_zone -labsl_bad_variant_access -labsl_raw_logging_internal\
 -labsl_log_severity -lcares -lssl -lre2 -lz -lmunge -lcrypto -lsqc_rpccommon -lprotobuf-c -lrt\
 -lpthread -ldl -lnuma -pthread"
SQC_INCS="-I${SQC_DIR}/include/ -I${SQC_DIR}/include"
PY_PATH=$(readlink -f $(which python3.11) | sed 's@/bin/python3.11@@g')
PYLIB="-L${PY_PATH}/lib -lpython3.11"

SQC_COMPILE_OPTIONS="${SQC_INCS} -L${SQC_DIR}/lib -L${SQC_DIR}/lib64 ${SQC_LIBS} ${PYLIB}"
