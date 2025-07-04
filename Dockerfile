FROM ghcr.io/winstxnhdw/nllb-api:main

ENV SERVER_PORT=7860
ENV TRANSLATOR_THREADS=4

ENV OMP_NUM_THREADS=1
ENV CT2_USE_EXPERIMENTAL_PACKED_GEMM=1
ENV CT2_FORCE_CPU_ISA=AVX512

ENV CONSUL_SERVICE_ADDRESS=winstxnhdw-nllb-api.hf.space

EXPOSE $SERVER_PORT
