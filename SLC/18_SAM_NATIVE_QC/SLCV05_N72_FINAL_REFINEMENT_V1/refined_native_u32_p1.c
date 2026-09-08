#include <stdint.h>
#include <stddef.h>

static inline uint64_t sam_u32_barrett_reduce(
    uint64_t value,
    uint64_t prime,
    uint64_t reciprocal
) {
    uint64_t quotient = (uint64_t)(((__uint128_t)value * reciprocal) >> 64);
    uint64_t remainder = value - quotient * prime;
    if (remainder >= prime) {
        remainder -= prime;
    }
    return remainder;
}

#define DEFINE_U32_P1_UPDATE(NAME, INDEX_TYPE)                               \
int NAME(                                                                     \
    uint32_t * restrict product_zero,                                         \
    uint32_t * restrict product_one,                                          \
    const uint32_t * restrict factor_values,                                  \
    const INDEX_TYPE * restrict base_index,                                   \
    uint64_t row_count,                                                       \
    uint64_t point_count,                                                     \
    uint64_t eliminated_bit,                                                  \
    uint64_t prime,                                                           \
    uint64_t reciprocal                                                       \
) {                                                                           \
    if (!product_zero || !product_one || !factor_values || !base_index ||     \
        point_count != 1 || prime == 0 || prime > UINT32_MAX) {              \
        return 1;                                                              \
    }                                                                          \
    for (uint64_t row = 0; row < row_count; ++row) {                          \
        uint64_t zero_row = (uint64_t)base_index[row];                        \
        uint64_t one_row = zero_row | eliminated_bit;                         \
        uint64_t zero_value =                                                 \
            (uint64_t)product_zero[row] * (uint64_t)factor_values[zero_row];  \
        uint64_t one_value =                                                  \
            (uint64_t)product_one[row] * (uint64_t)factor_values[one_row];    \
        product_zero[row] = (uint32_t)sam_u32_barrett_reduce(                 \
            zero_value, prime, reciprocal);                                   \
        product_one[row] = (uint32_t)sam_u32_barrett_reduce(                  \
            one_value, prime, reciprocal);                                    \
    }                                                                          \
    return 0;                                                                  \
}

DEFINE_U32_P1_UPDATE(sam_u32_update_index_u8_p1, uint8_t)
DEFINE_U32_P1_UPDATE(sam_u32_update_index_u16_p1, uint16_t)
DEFINE_U32_P1_UPDATE(sam_u32_update_index_u32_p1, uint32_t)

int sam_u32_finish_products(
    uint32_t * restrict output,
    const uint32_t * restrict product_zero,
    const uint32_t * restrict product_one,
    uint64_t value_count,
    uint64_t prime
) {
    if (!output || !product_zero || !product_one || prime == 0 ||
        prime > UINT32_MAX) {
        return 1;
    }
    for (uint64_t index = 0; index < value_count; ++index) {
        uint64_t value =
            (uint64_t)product_zero[index] + (uint64_t)product_one[index];
        if (value >= prime) {
            value -= prime;
        }
        output[index] = (uint32_t)value;
    }
    return 0;
}

uint64_t sam_u32_barrett_test(
    uint64_t value,
    uint64_t prime,
    uint64_t reciprocal
) {
    return sam_u32_barrett_reduce(value, prime, reciprocal);
}
