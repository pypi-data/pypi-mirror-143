
#include "proton/codec.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


/* D.C */
size_t pn_amqp_decode_DqC(pn_bytes_t bytes, pn_data_t* arg0);
/* D.[.....D..D.[.....CC]] */
size_t pn_amqp_decode_DqEqqqqqDqqDqEqqqqqCCee(pn_bytes_t bytes, pn_data_t* arg0, pn_data_t* arg1);
/* D.[.....D..D.[C]...] */
size_t pn_amqp_decode_DqEqqqqqDqqDqECeqqqe(pn_bytes_t bytes, pn_data_t* arg0);
/* D.[.....D..DL....] */
size_t pn_amqp_decode_DqEqqqqqDqqDLqqqqe(pn_bytes_t bytes, uint64_t* arg0);
/* D.[.....D.[.....C.C.CC]] */
size_t pn_amqp_decode_DqEqqqqqDqEqqqqqCqCqCCee(pn_bytes_t bytes, pn_data_t* arg0, pn_data_t* arg1, pn_data_t* arg2, pn_data_t* arg3);
/* D.[?HI] */
size_t pn_amqp_decode_DqEQHIe(pn_bytes_t bytes, bool* arg0, uint16_t* arg1, uint32_t* arg2);
/* D.[?I?L] */
size_t pn_amqp_decode_DqEQIQLe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint64_t* arg3);
/* D.[?IIII?I?II.o] */
size_t pn_amqp_decode_DqEQIIIIQIQIIqoe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, uint32_t* arg2, uint32_t* arg3, uint32_t* arg4, bool* arg5, uint32_t* arg6, bool* arg7, uint32_t* arg8, uint32_t* arg9, bool* arg10);
/* D.[?S?S?I?HI..CCC] */
size_t pn_amqp_decode_DqEQSQSQIQHIqqCCCe(pn_bytes_t bytes, bool* arg0, pn_bytes_t* arg1, bool* arg2, pn_bytes_t* arg3, bool* arg4, uint32_t* arg5, bool* arg6, uint16_t* arg7, uint32_t* arg8, pn_data_t* arg9, pn_data_t* arg10, pn_data_t* arg11);
/* D.[?o?oC] */
size_t pn_amqp_decode_DqEQoQoCe(pn_bytes_t bytes, bool* arg0, bool* arg1, bool* arg2, bool* arg3, pn_data_t* arg4);
/* D.[Bz] */
size_t pn_amqp_decode_DqEBze(pn_bytes_t bytes, uint8_t* arg0, pn_bytes_t* arg1);
/* D.[D.[sSC]] */
size_t pn_amqp_decode_DqEDqEsSCee(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_data_t* arg2);
/* D.[I?Iz.?oo.D?LRooo] */
size_t pn_amqp_decode_DqEIQIzqQooqDQLRoooe(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, uint32_t* arg2, pn_bytes_t* arg3, bool* arg4, bool* arg5, bool* arg6, bool* arg7, uint64_t* arg8, pn_bytes_t* arg9, bool* arg10, bool* arg11, bool* arg12);
/* D.[IoR] */
size_t pn_amqp_decode_DqEIoRe(pn_bytes_t bytes, uint32_t* arg0, bool* arg1, pn_bytes_t* arg2);
/* D.[R] */
size_t pn_amqp_decode_DqERe(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[SIo?B?BD.[SIsIo.s]D.[SIsIo]..IL..?C] */
size_t pn_amqp_decode_DqESIoQBQBDqESIsIoqseDqESIsIoeqqILqqQCe(pn_bytes_t bytes, pn_bytes_t* arg0, uint32_t* arg1, bool* arg2, bool* arg3, uint8_t* arg4, bool* arg5, uint8_t* arg6, pn_bytes_t* arg7, uint32_t* arg8, pn_bytes_t* arg9, uint32_t* arg10, bool* arg11, pn_bytes_t* arg12, pn_bytes_t* arg13, uint32_t* arg14, pn_bytes_t* arg15, uint32_t* arg16, bool* arg17, uint32_t* arg18, uint64_t* arg19, bool* arg20, pn_data_t* arg21);
/* D.[azSSSassttSIS] */
size_t pn_amqp_decode_DqEazSSSassttSISe(pn_bytes_t bytes, pn_atom_t* arg0, pn_bytes_t* arg1, pn_bytes_t* arg2, pn_bytes_t* arg3, pn_bytes_t* arg4, pn_atom_t* arg5, pn_bytes_t* arg6, pn_bytes_t* arg7, pn_timestamp_t* arg8, pn_timestamp_t* arg9, pn_bytes_t* arg10, uint32_t* arg11, pn_bytes_t* arg12);
/* D.[o?BIoI] */
size_t pn_amqp_decode_DqEoQBIoIe(pn_bytes_t bytes, bool* arg0, bool* arg1, uint8_t* arg2, uint32_t* arg3, bool* arg4, uint32_t* arg5);
/* D.[oI?IoR] */
size_t pn_amqp_decode_DqEoIQIoRe(pn_bytes_t bytes, bool* arg0, uint32_t* arg1, bool* arg2, uint32_t* arg3, bool* arg4, pn_bytes_t* arg5);
/* D.[sSC] */
size_t pn_amqp_decode_DqEsSCe(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1, pn_data_t* arg2);
/* D.[s] */
size_t pn_amqp_decode_DqEse(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D.[sz] */
size_t pn_amqp_decode_DqEsze(pn_bytes_t bytes, pn_bytes_t* arg0, pn_bytes_t* arg1);
/* D.[z] */
size_t pn_amqp_decode_DqEze(pn_bytes_t bytes, pn_bytes_t* arg0);
/* D?L. */
size_t pn_amqp_decode_DQLq(pn_bytes_t bytes, bool* arg0, uint64_t* arg1);
/* D?L?. */
size_t pn_amqp_decode_DQLQq(pn_bytes_t bytes, bool* arg0, uint64_t* arg1, bool* arg2);
