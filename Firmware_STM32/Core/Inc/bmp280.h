#ifndef __BMP280_H
#define __BMP280_H

#include "main.h"
// Shifted left by 1 for 8-bit HAL functions
#define BMP280_I2C_ADDR (0x77 << 1)

// BMP280 Register addresses
#define BMP280_REG_ID           0xD0
#define BMP280_REG_RESET        0xE0
#define BMP280_REG_STATUS       0xF3
#define BMP280_REG_CTRL_MEAS    0xF4
#define BMP280_REG_CONFIG       0xF5
#define BMP280_REG_PRESS_MSB    0xF7
#define BMP280_REG_TEMP_MSB     0xFA

// Expected Chip ID
#define BMP280_CHIP_ID          0x58

uint8_t BMP280_ReadID(void);
void BMP280_Init(void);

#endif
