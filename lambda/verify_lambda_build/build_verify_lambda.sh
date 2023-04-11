#!/bin/bash
export WRKDIR=$(pwd)
export OUTPUT_DIR="verify_lambda"
        
#Init Directory
rm ${WRKDIR}/verify.zip
rm -rf ${WRKDIR}/${OUTPUT_DIR}/
mkdir ${WRKDIR}/${OUTPUT_DIR}/
        
# Building zip
cd ${WRKDIR}/${OUTPUT_DIR}/
cp ${WRKDIR}/install_verify_lambda.sh ${WRKDIR}/${OUTPUT_DIR}/install_verify_lambda.sh
cp ${WRKDIR}/requirements.txt ${WRKDIR}/${OUTPUT_DIR}/requirements.txt
${WRKDIR}/${OUTPUT_DIR}/install_verify_lambda.sh
rm ${WRKDIR}/${OUTPUT_DIR}/install_verify_lambda.sh
rm ${WRKDIR}/${OUTPUT_DIR}/requirements.txt
zip -9 -r ${WRKDIR}/verify.zip .
cd ../../ && \
zip -9 -r ${WRKDIR}/verify.zip verify_code_lambda.py
