#ifndef FARLAND_LZSS_H
#define FARLAND_LZSS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* src[0..srclen-1] -> dst[0..dstlen-1]  (IEL1 블록의 8바이트 헤더 이후를 넘긴다) */
void lzss_decompress(const uint8_t *src, uint32_t srclen,
                     uint8_t *dst, uint32_t dstlen);

#ifdef __cplusplus
}
#endif

#endif
