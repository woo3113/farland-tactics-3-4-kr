/*
 * lzss.c - ??????????3/4 (IEL1) ??? ????? *
 * FT4.EXE sub_403ACF (0x403ACF) ??????????????????? LZSS ????
 * Dreamcast(KallistiOS) ????? ???????? ?????
 *
 *   ring[4096] ??0x20(' ') ??4078?????????? r = 4078 ???????
 *   flag ?????1??= ??? 8??(LSB ???)
 *       bit=1 : ?????1????? *       bit=0 : ??? - b(????????8), c(????????4 | ???-3)
 *               off = ((c & 0xF0) << 4) | b ;  len = (c & 0x0F) + 3
 */
#include "lzss.h"

void lzss_decompress(const uint8_t *src, uint32_t srclen, uint8_t *dst, uint32_t dstlen) {
    static uint8_t ring[4096];
    uint32_t i;
    int r;
    uint32_t flags = 0;
    uint32_t in_count = 0;
    uint32_t out_count = 0;
    const uint8_t *sp = src;

    for (i = 0; i < 4096 - 18; i++) ring[i] = 0x20;
    for (; i < 4096; i++) ring[i] = 0x00;
    r = 4096 - 18;

    for (;;) {
        uint8_t b;
        if ((flags & 0x100) == 0) {
            if (in_count >= srclen) break;
            flags = 0xFF00u | *sp++;
            in_count++;
        }
        if (in_count >= srclen) break;
        b = *sp++;
        in_count++;
        if (in_count > dstlen || out_count >= dstlen) break;

        if (flags & 1) {                       /* ?????*/
            ring[r & 0xFFF] = b;
            dst[out_count++] = b;
            r++;
        } else {                               /* ??? */
            uint32_t c, off, n;
            if (in_count >= srclen) break;
            c = *sp++;
            in_count++;
            if (in_count > dstlen) break;
            off = ((c & 0xF0) << 4) | b;
            n = (c & 0x0F) + 3;
            while (n--) {
                uint8_t v = ring[off & 0xFFF];
                ring[r & 0xFFF] = v;
                dst[out_count++] = v;
                off++;
                r++;
                if (out_count >= dstlen) break;
            }
        }
        flags >>= 1;
    }
}

