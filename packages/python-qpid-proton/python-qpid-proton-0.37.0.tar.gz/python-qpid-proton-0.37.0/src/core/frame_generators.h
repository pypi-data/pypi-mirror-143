
#include "proton/codec.h"
#include "buffer.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


/* DLC */
pn_bytes_t pn_amqp_encode_DLC(pn_buffer_t* buffer, uint64_t arg0, pn_data_t* arg1);
size_t pn_amqp_encode_bytes_DLC(char* bytes, size_t size, uint64_t arg0, pn_data_t* arg1);
/* DL[?DL[sSC]] */
pn_bytes_t pn_amqp_encode_DLEQDLEsSCee(pn_buffer_t* buffer, uint64_t arg0, bool arg1, uint64_t arg2, const char* arg3, const char* arg4, pn_data_t* arg5);
size_t pn_amqp_encode_bytes_DLEQDLEsSCee(char* bytes, size_t size, uint64_t arg0, bool arg1, uint64_t arg2, const char* arg3, const char* arg4, pn_data_t* arg5);
/* DL[?HIII] */
pn_bytes_t pn_amqp_encode_DLEQHIIIe(pn_buffer_t* buffer, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5);
size_t pn_amqp_encode_bytes_DLEQHIIIe(char* bytes, size_t size, uint64_t arg0, bool arg1, uint16_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5);
/* DL[?IIII?I?I?In?o] */
pn_bytes_t pn_amqp_encode_DLEQIIIIQIQIQInQoe(pn_buffer_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13);
size_t pn_amqp_encode_bytes_DLEQIIIIQIQIQInQoe(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, bool arg6, uint32_t arg7, bool arg8, uint32_t arg9, bool arg10, uint32_t arg11, bool arg12, bool arg13);
/* DL[?o?B?I?o?I] */
pn_bytes_t pn_amqp_encode_DLEQoQBQIQoQIe(pn_buffer_t* buffer, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10);
size_t pn_amqp_encode_bytes_DLEQoQBQIQoQIe(char* bytes, size_t size, uint64_t arg0, bool arg1, bool arg2, bool arg3, uint8_t arg4, bool arg5, uint32_t arg6, bool arg7, bool arg8, bool arg9, uint32_t arg10);
/* DL[@T[*s]] */
pn_bytes_t pn_amqp_encode_DLEATEjsee(pn_buffer_t* buffer, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3);
size_t pn_amqp_encode_bytes_DLEATEjsee(char* bytes, size_t size, uint64_t arg0, pn_type_t arg1, size_t arg2, char** arg3);
/* DL[Bz] */
pn_bytes_t pn_amqp_encode_DLEBze(pn_buffer_t* buffer, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3);
size_t pn_amqp_encode_bytes_DLEBze(char* bytes, size_t size, uint64_t arg0, uint8_t arg1, size_t arg2, const char* arg3);
/* DL[I?o?DL[sSC]] */
pn_bytes_t pn_amqp_encode_DLEIQoQDLEsSCee(pn_buffer_t* buffer, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, bool arg4, uint64_t arg5, const char* arg6, const char* arg7, pn_data_t* arg8);
size_t pn_amqp_encode_bytes_DLEIQoQDLEsSCee(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, bool arg2, bool arg3, bool arg4, uint64_t arg5, const char* arg6, const char* arg7, pn_data_t* arg8);
/* DL[IIzI?o?on?DLC?o?o?o] */
pn_bytes_t pn_amqp_encode_DLEIIzIQoQonQDLCQoQoQoe(pn_buffer_t* buffer, uint64_t arg0, uint32_t arg1, uint32_t arg2, size_t arg3, const char* arg4, uint32_t arg5, bool arg6, bool arg7, bool arg8, bool arg9, bool arg10, uint64_t arg11, pn_data_t* arg12, bool arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18);
size_t pn_amqp_encode_bytes_DLEIIzIQoQonQDLCQoQoQoe(char* bytes, size_t size, uint64_t arg0, uint32_t arg1, uint32_t arg2, size_t arg3, const char* arg4, uint32_t arg5, bool arg6, bool arg7, bool arg8, bool arg9, bool arg10, uint64_t arg11, pn_data_t* arg12, bool arg13, bool arg14, bool arg15, bool arg16, bool arg17, bool arg18);
/* DL[SIoBB?DL[SIsIoC?sCnCC]DL[C]nnI] */
pn_bytes_t pn_amqp_encode_DLESIoBBQDLESIsIoCQsCnCCeDLECennIe(pn_buffer_t* buffer, uint64_t arg0, const char* arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, const char* arg8, uint32_t arg9, const char* arg10, uint32_t arg11, bool arg12, pn_data_t* arg13, bool arg14, const char* arg15, pn_data_t* arg16, pn_data_t* arg17, pn_data_t* arg18, uint64_t arg19, pn_data_t* arg20, uint32_t arg21);
size_t pn_amqp_encode_bytes_DLESIoBBQDLESIsIoCQsCnCCeDLECennIe(char* bytes, size_t size, uint64_t arg0, const char* arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, const char* arg8, uint32_t arg9, const char* arg10, uint32_t arg11, bool arg12, pn_data_t* arg13, bool arg14, const char* arg15, pn_data_t* arg16, pn_data_t* arg17, pn_data_t* arg18, uint64_t arg19, pn_data_t* arg20, uint32_t arg21);
/* DL[SIoBB?DL[SIsIoC?sCnMM]?DL[SIsIoCM]nnILnnC] */
pn_bytes_t pn_amqp_encode_DLESIoBBQDLESIsIoCQsCnMMeQDLESIsIoCMennILnnCe(pn_buffer_t* buffer, uint64_t arg0, const char* arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, const char* arg8, uint32_t arg9, const char* arg10, uint32_t arg11, bool arg12, pn_data_t* arg13, bool arg14, const char* arg15, pn_data_t* arg16, pn_data_t* arg17, pn_data_t* arg18, bool arg19, uint64_t arg20, const char* arg21, uint32_t arg22, const char* arg23, uint32_t arg24, bool arg25, pn_data_t* arg26, pn_data_t* arg27, uint32_t arg28, uint64_t arg29, pn_data_t* arg30);
size_t pn_amqp_encode_bytes_DLESIoBBQDLESIsIoCQsCnMMeQDLESIsIoCMennILnnCe(char* bytes, size_t size, uint64_t arg0, const char* arg1, uint32_t arg2, bool arg3, uint8_t arg4, uint8_t arg5, bool arg6, uint64_t arg7, const char* arg8, uint32_t arg9, const char* arg10, uint32_t arg11, bool arg12, pn_data_t* arg13, bool arg14, const char* arg15, pn_data_t* arg16, pn_data_t* arg17, pn_data_t* arg18, bool arg19, uint64_t arg20, const char* arg21, uint32_t arg22, const char* arg23, uint32_t arg24, bool arg25, pn_data_t* arg26, pn_data_t* arg27, uint32_t arg28, uint64_t arg29, pn_data_t* arg30);
/* DL[SS?I?H?InnMMC] */
pn_bytes_t pn_amqp_encode_DLESSQIQHQInnMMCe(pn_buffer_t* buffer, uint64_t arg0, const char* arg1, const char* arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_data_t* arg9, pn_data_t* arg10, pn_data_t* arg11);
size_t pn_amqp_encode_bytes_DLESSQIQHQInnMMCe(char* bytes, size_t size, uint64_t arg0, const char* arg1, const char* arg2, bool arg3, uint32_t arg4, bool arg5, uint16_t arg6, bool arg7, uint32_t arg8, pn_data_t* arg9, pn_data_t* arg10, pn_data_t* arg11);
/* DL[S] */
pn_bytes_t pn_amqp_encode_DLESe(pn_buffer_t* buffer, uint64_t arg0, const char* arg1);
size_t pn_amqp_encode_bytes_DLESe(char* bytes, size_t size, uint64_t arg0, const char* arg1);
/* DL[Z] */
pn_bytes_t pn_amqp_encode_DLEZe(pn_buffer_t* buffer, uint64_t arg0, size_t arg1, const char* arg2);
size_t pn_amqp_encode_bytes_DLEZe(char* bytes, size_t size, uint64_t arg0, size_t arg1, const char* arg2);
/* DL[azSSSass?t?tS?IS] */
pn_bytes_t pn_amqp_encode_DLEazSSSassQtQtSQISe(pn_buffer_t* buffer, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, const char* arg4, const char* arg5, const char* arg6, pn_atom_t* arg7, const char* arg8, const char* arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, const char* arg14, bool arg15, uint32_t arg16, const char* arg17);
size_t pn_amqp_encode_bytes_DLEazSSSassQtQtSQISe(char* bytes, size_t size, uint64_t arg0, pn_atom_t* arg1, size_t arg2, const char* arg3, const char* arg4, const char* arg5, const char* arg6, pn_atom_t* arg7, const char* arg8, const char* arg9, bool arg10, pn_timestamp_t arg11, bool arg12, pn_timestamp_t arg13, const char* arg14, bool arg15, uint32_t arg16, const char* arg17);
/* DL[oI?I?o?DL[]] */
pn_bytes_t pn_amqp_encode_DLEoIQIQoQDLEee(pn_buffer_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8);
size_t pn_amqp_encode_bytes_DLEoIQIQoQDLEee(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, uint32_t arg4, bool arg5, bool arg6, bool arg7, uint64_t arg8);
/* DL[oIn?o?DLC] */
pn_bytes_t pn_amqp_encode_DLEoInQoQDLCe(pn_buffer_t* buffer, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, bool arg5, uint64_t arg6, pn_data_t* arg7);
size_t pn_amqp_encode_bytes_DLEoInQoQDLCe(char* bytes, size_t size, uint64_t arg0, bool arg1, uint32_t arg2, bool arg3, bool arg4, bool arg5, uint64_t arg6, pn_data_t* arg7);
/* DL[szS] */
pn_bytes_t pn_amqp_encode_DLEszSe(pn_buffer_t* buffer, uint64_t arg0, const char* arg1, size_t arg2, const char* arg3, const char* arg4);
size_t pn_amqp_encode_bytes_DLEszSe(char* bytes, size_t size, uint64_t arg0, const char* arg1, size_t arg2, const char* arg3, const char* arg4);
